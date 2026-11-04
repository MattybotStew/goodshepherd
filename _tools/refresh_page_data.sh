#!/bin/zsh
# Regenerate _tools/page_data.json from src/data/*.js.
#
# The data modules are plain ES modules with extension-less relative imports,
# which Node cannot resolve directly, so they are copied to a scratch dir with
# the imports rewritten before being imported.
#
#   ./_tools/refresh_page_data.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRATCH="${TMPDIR:-/tmp}/gsm_page_data"

rm -rf "$SCRATCH"
mkdir -p "$SCRATCH"
cp "$ROOT"/src/data/*.js "$SCRATCH"/

python3 - "$SCRATCH" <<'PY'
import glob, re, sys
for path in glob.glob(sys.argv[1] + "/*.js"):
    src = open(path).read()
    src = re.sub(r"from '\./([A-Za-z0-9_-]+)'", r"from './\1.js'", src)
    open(path, "w").write(src)
PY

node --input-type=module -e "
import fs from 'node:fs';
const dir = '${SCRATCH}';
const out = {};
for (const name of ['programs', 'health', 'careers', 'site', 'endowment', 'news']) {
  try {
    const mod = await import(dir + '/' + name + '.js');
    out[name] = Object.fromEntries(Object.entries(mod));
  } catch (e) {
    console.error('skip ' + name + ': ' + e.message);
  }
}
fs.writeFileSync('$ROOT/_tools/page_data.json', JSON.stringify(out));
console.log('wrote _tools/page_data.json  (' + Object.keys(out).join(', ') + ')');
"
