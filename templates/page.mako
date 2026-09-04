<%inherit file="base.mako"/>

## Generic page template used when an Org file does not choose a template.
<h1>${title}</h1>
${content | n}
