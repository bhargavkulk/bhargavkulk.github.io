import os
import sys
from pathlib import Path

import ninja_syntax
from utils import Folder

# TODO make ninja_syntax.py work with Path

# - Config -----------------------------------------------------------------------------------------
CONTENT = Folder('content/')
CACHE = Path('cache/')
# Maps collection name to whether it needs a rss feed
COLLECTIONS = {'blog': True}
TEMPLATES = Folder('templates/')
ASSETS = Folder('assets/')

templates = [str(file) for file in TEMPLATES.iterdir()]

# - Generator --------------------------------------------------------------------------------------
gen = ninja_syntax.Writer(open('build.ninja', 'w'))

# Regen build.ninja when this file changes
gen.rule('regen_ninja', f'{sys.executable} $in > $out')
gen.build('build.ninja', 'regen_ninja', __file__)

# Fragments & Metadata
gen.rule(
    'djot2fragment',
    'pandoc -f djot -t html --mathml --lua-filter filters/djot.lua $in -o $out',
)
gen.rule(
    'djot2mdata',
    'pandoc -f djot --lua-filter filters/djot-metadata.lua $in > $out',
)

for source in CONTENT.rglob('*.dj'):
    frag = (CACHE / source.relative_to(CONTENT)).with_suffix('.html')
    mdata = frag.with_suffix('.json')
    gen.build(
        str(frag),
        'djot2fragment',
        str(source),
        implicit='filters/djot.lua',
    )
    gen.build(
        str(mdata),
        'djot2mdata',
        str(source),
        implicit='filters/djot-metadata.lua',
    )

# Make collection indices
gen.rule(
    'collection_index',
    'uv run python scripts/generate_index.py $out $dir $in',
)

collection_indices = []
for collection in COLLECTIONS:
    dir = CONTENT / collection
    if dir.is_dir():
        cache_dir = CACHE / collection
        mdatas = [
            str((cache_dir / file.name).with_suffix('.json'))
            for file in dir.glob('*.dj')
        ]
        gen.build(
            str(CACHE / f'{collection}_index.json'),
            'collection_index',
            mdatas,
            implicit='scripts/generate_index.py',
            variables={'dir': str(cache_dir)},
        )

        collection_indices.append(str(CACHE / f'{collection}_index.json'))

# Fill templates
gen.rule(
    'fill_template',
    'uv run python scripts/fill_template.py $in templates $out $extra',
)

for source in CONTENT.rglob('*.dj'):
    frag = (CACHE / source.relative_to(CONTENT)).with_suffix('.html')
    mdata = frag.with_suffix('.json')
    page = Path('www') / source.relative_to(CONTENT).with_suffix('.html')

    gen.build(
        str(page),
        'fill_template',
        [str(frag), str(mdata)],
        implicit=[
            'scripts/fill_template.py',
            *templates,
            *collection_indices,
        ],
        variables={'extra': collection_indices},
    )

# Blog feeds
gen.rule(
    'blog_feed',
    'uv run python scripts/generate_feed.py cache/blog_index.json cache www',
)
gen.build(
    ['www/blog_index_atom.xml', 'www/blog_index_rss.xml'],
    'blog_feed',
    'cache/blog_index.json',
    implicit='scripts/generate_feed.py',
)

# Copy assets
gen.rule(
    'copy_asset',
    'mkdir -p $dir && cp $in $out',
)

for source in ASSETS.rglob('*'):
    if source.is_file():
        out = Path('www') / source.relative_to(ASSETS)
        gen.build(
            str(out),
            'copy_asset',
            str(source),
            variables={'dir': str(out.parent)},
        )

gen.close()
