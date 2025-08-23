import os, re
ROOT = os.path.dirname(__file__)
TEMPLATES = os.path.join(ROOT, 'templates')
pat_block = re.compile(r"{%\s*block\b")
pat_endblock = re.compile(r"{%\s*endblock\b")
pat_open_var = re.compile(r"{{")
pat_close_var = re.compile(r"}}")
pat_extends = re.compile(r"^{%\s*extends\b")

for fn in sorted(os.listdir(TEMPLATES)):
    if not fn.endswith('.html'):
        continue
    path = os.path.join(TEMPLATES, fn)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    blocks = len(pat_block.findall(text))
    endblocks = len(pat_endblock.findall(text))
    openvars = len(pat_open_var.findall(text))
    closevars = len(pat_close_var.findall(text))
    # find first non-empty line
    first_nonempty = None
    for line in text.splitlines():
        if line.strip():
            first_nonempty = line.strip()
            break
    extends_ok = first_nonempty is not None and pat_extends.match(first_nonempty)
    print(f"{fn}: blocks={blocks} endblocks={endblocks}  {{}}s={openvars}/{closevars} extends_top={extends_ok}")
    if blocks != endblocks:
        print(f"  -> MISMATCH: {fn} has {blocks} blocks but {endblocks} endblocks")
    if openvars != closevars:
        print(f"  -> VAR MISMATCH: {fn} has {openvars} '{{{{' and {closevars} '}}}}'")
    if not extends_ok and (('block content' in text) or ('block title' in text) or blocks>0):
        print(f"  -> WARNING: {fn} has blocks but no extends at top (first non-empty line: {first_nonempty!r})")
