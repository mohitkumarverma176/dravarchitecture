import os
import re

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
pattern_block = re.compile(r"\{%-?\s*block\b")
pattern_end = re.compile(r"\{%-?\s*endblock\b")

errors = []
for root, dirs, files in os.walk(TEMPLATES_DIR):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        txt = open(path, 'r', encoding='utf-8').read()
        blocks = len(pattern_block.findall(txt))
        ends = len(pattern_end.findall(txt))
        if blocks != ends:
            errors.append((os.path.relpath(path, TEMPLATES_DIR), blocks, ends))

if not errors:
    print('OK: block/endblock counts match in all templates')
else:
    print('MISMATCH in templates:')
    for fn, b, e in errors:
        print(f'- {fn}: block={b}, endblock={e}')
    raise SystemExit(1)
