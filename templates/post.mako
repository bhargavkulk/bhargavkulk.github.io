<%inherit file="base.mako"/>
<%!
from date_utils import format_date_attr, parse_org_date
%>

<%block name="head_extra">
    <meta name="description" content="${description}">
    <meta property="og:title" content="${title}">
    <meta property="og:description" content="${description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://bhargavkulk.github.io${link}">
</%block>

<div class="subtitle"><time datetime="${format_date_attr(date)}">${parse_org_date(date).strftime('%b %d, %Y')}</time> <a href="/blog_index_rss.xml" style="font-family: monospace">[rss]</a> <a href="/blog_index_atom.xml" style="font-family: monospace">[atom]</a></div>
${content | n}
