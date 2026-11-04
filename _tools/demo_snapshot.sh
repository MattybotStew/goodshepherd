#!/bin/zsh
# Build the static client demo from the Local WordPress site and publish it to
# the gh-pages branch, which GitHub Pages serves at
# https://mattybotstew.github.io/goodshepherd/
#
#   _tools/demo_snapshot.sh              # build and publish
#   _tools/demo_snapshot.sh --no-publish # build only, leaves it in $WORK
#
# A raw wget mirror of this build is not usable on its own: the WebP plugin
# routes images through webpc-passthru.php, assets carry ?ver= queries, URLs are
# HTML-escaped, content links are root-absolute, and posts save as flat .html.
# demo_snapshot.py fixes all of that; read its header before changing it.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SITE="https://goodshepherd.local"
WORK="${WORK:-/tmp/gsm-demo}"
PUBLISH=1
[[ "${1:-}" == "--no-publish" ]] && PUBLISH=0

command -v wget >/dev/null || { echo "wget missing: brew install wget" >&2; exit 1; }
curl -sk -o /dev/null "https://goodshepherd.local/" || { echo "Local site not responding" >&2; exit 1; }

echo "==> mirroring $SITE"
rm -rf "$WORK"
mkdir -p "$WORK"
cd "$WORK"

# exit 8 just means some asset 404'd; the pages themselves still mirror
wget --mirror --page-requisites --adjust-extension --no-parent \
     --no-check-certificate --domains=goodshepherd.local --execute robots=off \
     --timeout=30 --tries=3 "$SITE/" >/dev/null 2>&1 || true

# this one is consistently skipped by the main crawl
wget --mirror --page-requisites --adjust-extension --no-parent \
     --no-check-certificate --domains=goodshepherd.local --execute robots=off \
     --timeout=30 --tries=3 "$SITE/newsletters/" >/dev/null 2>&1 || true

echo "==> normalising"
python3 "$REPO/_tools/demo_snapshot.py" "$WORK/goodshepherd.local"

SNAP="$WORK/goodshepherd.local"
[[ -f "$SNAP/index.html" ]] || { echo "snapshot has no index.html" >&2; exit 1; }

PAGES=$(find "$SNAP" -name index.html | wc -l | tr -d ' ')
SIZE=$(du -sh "$SNAP" | cut -f1)
echo "==> snapshot: $PAGES pages, $SIZE"

if [[ $PUBLISH -eq 0 ]]; then
  echo "built only. view with:  python3 -m http.server 8000 --directory $SNAP"
  exit 0
fi

echo "==> publishing to gh-pages"
rm -rf "$WORK/publish"
mkdir -p "$WORK/publish"
cp -R "$SNAP/." "$WORK/publish/"
cd "$WORK/publish"

# GitHub Pages runs Jekyll unless this exists; it would drop directories and
# mangle anything that looks like Liquid.
touch .nojekyll

git init -q -b gh-pages
git add -A
git -c user.name="$(git -C "$REPO" config user.name)" \
    -c user.email="$(git -C "$REPO" config user.email)" \
    commit -q -m "Static demo snapshot $(date +%Y-%m-%d)"
git remote add origin "$(git -C "$REPO" remote get-url origin)"
git push -f origin gh-pages

echo
echo "pushed. The deploy workflow runs from main; trigger it with:"
echo "  gh workflow run pages.yml"
echo "Then check https://mattybotstew.github.io/goodshepherd/"
