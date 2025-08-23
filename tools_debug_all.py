import os
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

ROOT = os.path.dirname(__file__)
TEMPLATES = os.path.join(ROOT, 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES))
results = []
for fn in sorted(os.listdir(TEMPLATES)):
    if not fn.endswith('.html'):
        continue
    try:
        env.get_template(fn)
        results.append(f"OK: {fn}")
    except TemplateSyntaxError as e:
        results.append(f"ERROR: {fn} | lineno={e.lineno} | message={e.message}")
    except Exception as e:
        results.append(f"EXC: {fn} | {type(e).__name__}: {e}")

outf = os.path.join(ROOT, 'debug_results.txt')
with open(outf, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
print('Wrote', outf)
