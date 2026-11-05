#!/usr/bin/env python3
"""
Convert a wget mirror of the Local WordPress site into a static site that works
at any path (domain root, a subpath, or file://).

    wget --mirror --page-requisites --adjust-extension --no-parent \
         --no-check-certificate --domains=goodshepherd.local \
         --execute robots=off https://goodshepherd.local/
    python3 demo_snapshot.py /tmp/gsm-demo/goodshepherd.local

Why this exists: a raw mirror of this build is not usable. The WebP plugin
routes images through webpc-passthru.php (so they land under filenames that
cannot be referenced), assets carry ?ver= queries, URLs are HTML-escaped, site
content links are root-absolute (they break under a subpath), and posts are
saved as flat .html files rather than pretty directories.

Order matters: files are moved to their final locations first, then every
document is rewritten using the depth it will actually be served at.
"""
import os
import re
import shutil
import sys
from urllib.parse import unquote

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gsm-demo/goodshepherd.local"
DOMAIN = "https://goodshepherd.local"
NOISE = ["&amp;nocache=1", "&nocache=1"]


def dedupe_move(src, dst):
    """Move src to dst, dropping src if dst already exists."""
    if os.path.abspath(src) == os.path.abspath(dst):
        return False
    if os.path.exists(dst):
        os.remove(src)
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    return True


# ---------------------------------------------------------------- filesystem
restored = 0
for dirpath, _dirs, files in os.walk(ROOT):
    for name in list(files):
        src = os.path.join(dirpath, name)

        # 1. webpc-passthru responses -> their real uploads path
        if "webpc-passthru.php?src=" in name:
            raw = name.split("webpc-passthru.php?src=", 1)[1]
            for suffix in NOISE:
                raw = raw.split(suffix)[0]
            raw = unquote(raw)
            if raw.startswith(DOMAIN + "/"):
                if dedupe_move(src, os.path.join(ROOT, raw[len(DOMAIN) + 1:])):
                    restored += 1
            continue

        # 2. escaped / query-suffixed asset names
        for suffix in NOISE:
            if name.endswith(suffix):
                dedupe_move(src, os.path.join(dirpath, name[: -len(suffix)]))
                break
        if "?" in name:
            dedupe_move(src, os.path.join(dirpath, name.split("?", 1)[0]))

pretty = 0
# 3. flat page.html -> page/index.html so extension-less links resolve
for dirpath, _dirs, files in os.walk(ROOT):
    for name in list(files):
        if not name.endswith(".html") or name == "index.html":
            continue
        src = os.path.join(dirpath, name)
        if os.path.getsize(src) == 0:
            os.remove(src)
            continue
        target_dir = os.path.join(dirpath, name[:-5])
        if dedupe_move(src, os.path.join(target_dir, "index.html")):
            pretty += 1

# ---------------------------------------------------------------- rewriting
PASSTHRU = re.compile(
    r"https://goodshepherd\.local/wp-content/webpc-passthru\.php\?src="
    r"(https://goodshepherd\.local/[^&\"'\s>)]+?)"
    r"(?:&amp;|&)nocache=1"
)
ROOT_ABS = re.compile(r'(?P<attr>\b(?:href|src|action)=)"/(?P<path>[^"]*)"')
# CSS url(/wp-content/...) inside a stylesheet also drops the subpath. Astra's
# local-fonts.css is the one that matters: if its @font-face srcs 404, the
# whole demo renders in a fallback sans-serif.
CSS_URL_ABS = re.compile(r'url\((?P<q>["\']?)/(?P<path>[^)"\']*)')
# The demo must not report to Google Analytics — the property is still the
# plugin's placeholder ID, and real visits would pollute client stats.
GA_BLOCK = re.compile(
    r"\s*<!-- GA Google Analytics.*?-->\s*"
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"></script>\s*'
    r"<script>.*?gtag\('config'[^;]*;.*?</script>",
    re.S,
)

changed = 0
for dirpath, _dirs, files in os.walk(ROOT):
    for name in files:
        if not name.endswith((".html", ".css", ".js")):
            continue
        path = os.path.join(dirpath, name)
        rel_dir = os.path.relpath(dirpath, ROOT)
        depth = 0 if rel_dir == "." else len(rel_dir.split(os.sep))
        prefix = "../" * depth

        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            text = fh.read()
        original = text

        text = PASSTHRU.sub(lambda m: prefix + m.group(1)[len(DOMAIN) + 1:], text)
        text = text.replace("https:\\/\\/goodshepherd.local\\/", prefix or "./")
        text = text.replace(DOMAIN + "/", prefix)
        text = text.replace(DOMAIN, prefix.rstrip("/") or ".")

        def rel_root(m):
            attr, target = m.group("attr"), m.group("path")
            if target.startswith("/"):  # protocol-relative, leave alone
                return m.group(0)
            return f'{attr}"{prefix}{target}"'

        text = ROOT_ABS.sub(rel_root, text)

        def rel_css_url(m):
            q = m.group("q")
            target = m.group("path")
            if target.startswith("/"):  # protocol-relative url(//host/...)
                return m.group(0)
            return f"url({q}{prefix}{target}{q}"

        text = CSS_URL_ABS.sub(rel_css_url, text)
        text = GA_BLOCK.sub("", text)
        for noise in ("&amp;nocache=1", "&nocache=1"):
            text = text.replace(noise, "")

        if text != original:
            with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(text)
            changed += 1

print(f"images restored : {restored}")
print(f"pages prettified: {pretty}")
print(f"files rewritten : {changed}")

left = 0
for dirpath, _dirs, files in os.walk(ROOT):
    for name in files:
        if name.endswith((".html", ".css")):
            with open(os.path.join(dirpath, name), encoding="utf-8", errors="ignore") as fh:
                if "goodshepherd.local" in fh.read():
                    left += 1
print(f"files still on .local (oEmbed refs are inert): {left}")
