from io import StringIO
import os
import tomllib
from typing import Any, Optional
from plumbum import local
from tomllib import loads as read_toml
from mako.template import Template
from mako.runtime import Context
from collections import OrderedDict
import sass
from datetime import datetime

DATA_PATH = 'data'
BUILD_PATH = 'docs'
TEMPLATE_PATH = 'templates'
BLOG_PATH = 'data/blog'

SITE_MAP = OrderedDict([('home', '/'), ('research', '/research.html'), ('blog', '/blog.html'), ('cv', '/cv.html'), ('contact', '/contact.html')])

pandoc = local['pandoc']['--no-highlight --lua-filter pygments.lua -f djot -t html'.split()]

def generate_sitemap(dir: str) -> StringIO:
    template = Template(filename='templates/site_map.html')
    buffer = StringIO()
    context = Context(buffer, site_map=SITE_MAP, dir=dir)
    template.render_context(context)
    return buffer

def generate_post(filename: str, date, title) -> StringIO:
    file_path = os.path.join(BLOG_PATH, filename)
    site_map = generate_sitemap('blog')
    html_content = pandoc(file_path)

    template = Template(filename=os.path.join(TEMPLATE_PATH, 'post.html'))
    buffer = StringIO()
    context = Context(buffer, site_map=site_map, title=title, date=date, content=html_content)
    template.render_context(context)
    return buffer

def generate_html(filename: str) -> StringIO:
    file_path = os.path.join(DATA_PATH, filename)
    data = get_frontmatter(file_path)
    site_map = generate_sitemap(data['dir'])

    html_content = pandoc(file_path)
    template = Template(filename=os.path.join(TEMPLATE_PATH, data['template']))
    buffer = StringIO()
    context = Context(buffer, site_map=site_map, content=html_content)
    template.render_context(context)

    return buffer

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
    if os.path.isfile(file_path) and file.endswith('dj') and (not file.startswith('index')):
        name, _ = os.path.splitext(file)
        buffer = generate_html(file)
        output = os.path.join(BUILD_PATH, f'{name}.html')
        with open(output, 'w') as file:
            file.write(buffer.getvalue())

with open(os.path.join(DATA_PATH, 'blog.toml'), 'rb') as file:
    data = tomllib.load(file)

# convert data keys into datetime objects
data = {datetime.strptime(key, "%Y-%m-%d"): value for key, value in data.items()}

# get sorted keys of dates
dates = sorted(data.keys(), reverse=True)

for file in os.listdir(BLOG_PATH):
    file_path = os.path.join(BLOG_PATH, file)
    if os.path.isfile(file_path) and file.endswith('dj'):
        name, _ = os.path.splitext(file)
        date = datetime.strptime(name, "%Y-%m-%d")
        buffer = generate_post(file, date, data[date]['title'])
        with open(os.path.join(BUILD_PATH, 'blog', f'{name}.html'), 'w') as file:
            file.write(buffer.getvalue())

site_map = generate_sitemap('blog')
template = Template(filename=os.path.join(TEMPLATE_PATH, 'blog.html'))
buffer = StringIO()
context = Context(buffer, site_map=site_map, dates=dates, data=data)
template.render_context(context)
with open(os.path.join(BUILD_PATH, 'blog.html'), 'w') as file:
    file.write(buffer.getvalue())

latest_date = dates[0]
latest_data = data[latest_date]
site_map = generate_sitemap('home')
template = Template(filename=os.path.join(TEMPLATE_PATH, 'index.html'))
buffer = StringIO()
html_content = pandoc(os.path.join(DATA_PATH, 'index.dj'))
context = Context(buffer, site_map=site_map, content=html_content, latest_date=latest_date, latest_data=latest_data)
template.render_context(context)
with open(os.path.join(BUILD_PATH, 'index.html'), 'w') as file:
    file.write(buffer.getvalue())
