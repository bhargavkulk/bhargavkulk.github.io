from io import StringIO
import os
from typing import Any
from plumbum import local
from tomllib import loads as read_toml
from mako.template import Template
from mako.runtime import Context
from collections import OrderedDict
import sass

from plumbum.path.local import shutil

DATA_PATH = 'data'
BUILD_PATH = 'docs'
TEMPLATE_PATH = 'templates'

SITE_MAP = OrderedDict([('home', '/'), ('research', '/research.html'), ('cv', '/cv.html'), ('contact', '/contact.html')])

pandoc = local['pandoc']['--no-highlight --lua-filter pygments.lua -f djot -t html'.split()]

def generate_sitemap(dir):
    template = Template(filename='templates/site_map.html')
    buffer = StringIO()
    context = Context(buffer, site_map=SITE_MAP, dir=dir)
    template.render_context(context)
    return buffer

def generate_html(filename):
    file_path = os.path.join(DATA_PATH, filename)
    data = get_frontmatter(file_path)

    html_content = pandoc(file_path)

    site_map = generate_sitemap(data['dir'])

    template = Template(filename=os.path.join(TEMPLATE_PATH, data['template']))
    buffer = StringIO()
    context = Context(buffer, site_map=site_map, content=html_content)
    template.render_context(context)

    return buffer

    with open('test.html', 'w') as file:
        file.write(buffer.getvalue())

def get_frontmatter(path: str) -> dict[str, Any]:
    with open(path, 'r') as file:
        data: list[str] = []
        for line in file:
            line = line.strip('\n ')
            if line.startswith('{%'):
                data.append(line[3:])
            elif line.endswith('%}'):
                data.append(line[:-3])
                break
            else:
                data.append(line)
    return read_toml('\n'.join(data))

sass.compile(dirname=('assets', 'docs/assets'), output_style='compressed')

for file in os.listdir(DATA_PATH):
    file_path = os.path.join(DATA_PATH, file)
    print(file, os.path.isfile(file_path))
    if os.path.isfile(file_path) and file.endswith('dj'):
        print('here')
        name, _ = os.path.splitext(file)
        buffer = generate_html(file)
        print(buffer.getvalue())
        output = os.path.join(BUILD_PATH, f'{name}.html')
        with open(output, 'w') as file:
            file.write(buffer.getvalue())
