"""Create a deterministic preview artifact; no framework or bundler required."""
import argparse
import json
import re
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--sha', required=True)
args = parser.parse_args()
if not re.fullmatch(r'[0-9a-f]{40}', args.sha):
    parser.error('--sha must be a full Git commit SHA')
root = Path(__file__).resolve().parents[1]
out = root / 'dist'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ('index.html', 'styles.css', 'app.js'):
    shutil.copy2(root / name, out / name)
shutil.copytree(root / 'assets', out / 'assets', ignore=shutil.ignore_patterns('old'))
html = (out / 'index.html').read_text(encoding='utf-8')
html = html.replace('content="index,follow"', 'content="noindex,nofollow"')
(out / 'index.html').write_text(html, encoding='utf-8')
(out / '.nojekyll').touch()
(out / 'version.json').write_text(json.dumps({'source_repository': 'heroprint/heroprint-page', 'source_commit': args.sha}, indent=2) + '\n', encoding='utf-8')
print(f'Preview built from {args.sha}: {out}')
