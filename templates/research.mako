<%inherit file="base.mako"/>

<dl>
  <dt>Authors</dt>
  <dd>${authors}</dd>
  <dt>Conference</dt>
  <dd>${conf}</dd>
  % if doi:
    <dt>DOI</dt>
    <dd><a href="https://doi.org/${doi}">${doi}</a></dd>
  % endif
  % if arxiv:
    <dt>arXiv</dt>
    <dd><a href="https://arxiv.org/abs/${arxiv}">${arxiv}</a></dd>
  % endif
  % if slides:
    <dt>Slides</dt>
    <dd><a href="${slides}">${slides}</a></dd>
  % endif
</dl>

${content | n}
