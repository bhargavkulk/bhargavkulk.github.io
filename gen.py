import os
import sys
from pathlib import Path

import ninja_syntax
from ninja_syntax import Rule

# TODO make ninja_syntax.py work with Path

gen = ninja_syntax.Writer(open('build.ninja', 'w'))

# - General config -----------------------------------------------------------------------------------------
CONTENT = Path('content/')
CACHE = Path('cache/')
TEMPLATES = Path('templates/')
ASSETS = Path('assets/')


# - File format config -----------------------------------------------------------------------------
# Every file format must generate metadata, but some may not generate HTML fragments
FILE_FORMATS = {
    '.dj': {
        'fragment': Rule(
            gen,
            'dj_fragment',
            'pandoc -f djot -t html --mathml --lua-filter filters/djot.lua $in -o $out',
            implicit='filters/djot.lua',
        ),
        'metadata': Rule(
            gen,
            'dj_mdata',
            'pandoc -f djot --lua-filter filters/djot-metadata.lua $in > $out',
            implicit='filters/djot-metadata.lua',
        ),
    },
    '.org': {
        'fragment': Rule(
            gen,
            'org_fragment',
            'pandoc -f org+smart --shift-heading-level-by=1 -t html --mathml --lua-filter filters/org.lua $in -o $out',
            implicit='filters/org.lua',
        ),
        'metadata': Rule(
            gen,
            'org_mdata',
            'pandoc -f org+smart --lua-filter filters/org-metadata.lua $in > $out',
            implicit='filters/org-metadata.lua',
        ),
    },
    '.json': {
        'metadata': Rule(
            gen,
            'json_mdata',
            'uv run scripts/copy_file.py $in $out',
        ),
    },
}

# - Collections config -----------------------------------------------------------------------------
COLLECTIONS = {
    'blog': True,
}


# - Common data and functions ----------------------------------------------------------------------
content_files = [
    path for path in CONTENT.rglob('*') if path.is_file() and path.name != '.dir-locals.el'
]
templates = [str(path) for path in TEMPLATES.iterdir()]


# ASSUMES path.suffix is arleady in FILE_FORMATS
def is_fraggable(extn: str) -> bool:
    return 'fragment' in FILE_FORMATS[extn]


# - Build cache ------------------------------------------------------------------------------------
for source in content_files:
    if source.suffix not in FILE_FORMATS:
        raise ValueError(f'Unknown content file format {source.suffix}.')

    mdata = (CACHE / source.relative_to(CONTENT)).with_suffix('.json')
    FILE_FORMATS[source.suffix]['metadata'].build(str(mdata), str(source))

    if is_fraggable(source.suffix):
        frag = mdata.with_suffix('.html')
        FILE_FORMATS[source.suffix]['fragment'].build(str(frag), str(source))

# - Generate collection indices --------------------------------------------------------------------
gen.rule(
    'collection_index',
    'uv run python scripts/generate_index.py $out $in',
)

# ASSUMES collections are flat, i.e. no folders within a collection
collection_indices = []
for collection in COLLECTIONS:
    collection_dir = CONTENT / collection
    # If declared in config, collection folder MUST exist
    if not collection_dir.is_dir():
        raise ValueError(
            f'Collection directory {collection_dir} either does not exists or is a file.'
        )

    cache_dir = CACHE / collection
    # Collect all corresponding metadatas of the files in the collcetion
    collection_metadatas = [
        str((cache_dir / path.name).with_suffix('.json'))
        for path in collection_dir.iterdir()
        if path.is_file()
    ]
    gen.build(
        str(CACHE / f'{collection}_index.json'),
        'collection_index',
        collection_metadatas,
        implicit='scripts/generate_index.py',
    )
    collection_indices.append(str(CACHE / f'{collection}_index.json'))

# - Fill templates ---------------------------------------------------------------------------------
gen.rule(
    'fill_template',
    'uv run python scripts/fill_template.py $in templates $out $extra $fragment',
)

for source in content_files:
    mdata = (CACHE / source.relative_to(CONTENT)).with_suffix('.json')
    page = Path('www') / source.relative_to(CONTENT).with_suffix('.html')
    variables: dict[str, str | list[str] | None] = {
        'extra': collection_indices,
    }
    implicit = [
        'scripts/fill_template.py',
        'scripts/date_utils.py',
        *templates,
        *collection_indices,
    ]
    if is_fraggable(source.suffix):
        fragment = mdata.with_suffix('.html')
        variables['fragment'] = f'--fragment {fragment}'
        implicit.append(str(fragment))

    gen.build(
        str(page),
        'fill_template',
        str(mdata),
        implicit=implicit,
        variables=variables,
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
