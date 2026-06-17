<%inherit file="base.mako"/>
<%!
from datetime import datetime
%>

<h1>Blog <a href="/blog_index_rss.xml" style="font-size: 1rem; font-weight: normal;">[rss]</a> <a href="/blog_index_atom.xml" style="font-size: 1rem; font-weight: normal;">[atom]</a></h1>

${content | n}

<table>
% for entry in sorted(blog_index, key=lambda entry: entry.get('date', ''), reverse=True):
  <tr>
    <td>
      % if entry.get('date'):
        <time datetime="${entry['date']}">${datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d, %Y')}</time>
      % endif
    </td>
    <td><a href="${entry['link']}">${entry['title']}</a></td>
  </tr>
% endfor
</table>
