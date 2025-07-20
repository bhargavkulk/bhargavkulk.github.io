<%inherit file="base.mako"/>

<%block name="content">
    <h1 class="blog">${metadata['title']}</h1>
    <div class="date">${metadata['date']}</div>
    ${content_}
</%block>
