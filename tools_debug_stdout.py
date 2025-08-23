import os
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
ROOT = os.path.dirname(__file__)
TEMPLATES = os.path.join(ROOT, 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES))
for fn in sorted(os.listdir(TEMPLATES)):
    if not fn.endswith('.html'):
        continue
    try:
        env.get_template(fn)
        print(f"OK: {fn}")
    except TemplateSyntaxError as e:
        print(f"ERROR: {fn} at {e.lineno}: {e.message}")
    except Exception as e:
        print(f"EXC: {fn}: {type(e).__name__}: {e}")
