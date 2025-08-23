import os
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError


def main():
    tpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(tpl_dir))
    errors = []
    for root, dirs, files in os.walk(tpl_dir):
        for f in files:
            if not f.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(root, f), tpl_dir)
            try:
                env.get_template(rel)
            except TemplateSyntaxError as e:
                errors.append((rel, str(e)))
    if errors:
        print('FOUND TemplateSyntaxErrors:')
        for r, msg in errors:
            print('-', r + ':', msg)
        raise SystemExit(1)
    print('OK: no Jinja2 TemplateSyntaxError found')


if __name__ == '__main__':
    main()
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

errors = []
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for f in files:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), TEMPLATES_DIR)
            try:
                env.get_template(rel)
            except TemplateSyntaxError as e:
                errors.append((rel, str(e)))

if not errors:
    print('OK: no Jinja2 TemplateSyntaxError found')
else:
    print('FOUND TemplateSyntaxErrors:')
    for fn, msg in errors:
        print(f"- {fn}: {msg}")
    raise SystemExit(1)
