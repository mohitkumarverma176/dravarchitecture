import sys
import os
import traceback
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

tpl = sys.argv[1] if len(sys.argv) > 1 else 'services.html'
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
try:
    env.get_template(tpl)
    print('OK: template parsed:', tpl)
except TemplateSyntaxError as e:
    print('TEMPLATE SYNTAX ERROR')
    print('template:', e.filename)
    print('lineno:', e.lineno)
    print('message:', e.message)
    traceback.print_exc()
except Exception as e:
    print('OTHER ERROR')
    traceback.print_exc()
