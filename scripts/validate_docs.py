"""Offline Markdown file/heading link validation, excluding historical local references."""
from pathlib import Path
from urllib.parse import unquote
import re,unicodedata
root=Path(__file__).resolve().parents[1]

def slug(text):
 return ''.join(c for c in text.strip().lower() if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ','-')

errors=[];count=0
for path in root.rglob('*.md'):
 if any(x in path.parts for x in ['.venv','.git','runs']): continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
  if '://' in target or target.startswith('mailto:'): continue
  filename,_,fragment=unquote(target).partition('#');dest=(path.parent/filename).resolve() if filename else path
  count+=1
  if not dest.exists(): errors.append(f'{path.relative_to(root)}: missing {target}');continue
  if fragment:
   anchors={slug(m.group(1)) for m in re.finditer(r'^#{1,6}\s+(.+)$',dest.read_text(),re.M)}
   if fragment not in anchors: errors.append(f'{path.relative_to(root)}: missing anchor {target}')
print(f'Checked {count} local links. '+ ('\n'.join(errors) if errors else 'All resolve.'))
raise SystemExit(bool(errors))
