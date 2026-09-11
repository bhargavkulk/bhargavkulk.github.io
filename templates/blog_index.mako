<%inherit file="base.mako"/>
<%!
from datetime import datetime

from date_utils import format_date_attr, parse_org_date
%>

<div class="subtitle">
    <a href="/blog_index_rss.xml" style="font-family: monospace">[rss]</a>
    <a href="/blog_index_atom.xml" style="font-family: monospace">[atom]</a>
</div>

<table>
% for entry in sorted(blog_index, key=lambda entry: parse_org_date(entry['date']) if entry.get('date') else datetime.min, reverse=True):
  <tr>
    <td>
      % if entry.get('date'):
        <time datetime="${format_date_attr(entry['date'])}">${parse_org_date(entry['date']).strftime('%b %d, %Y')}</time>
      % endif
    </td>
    <td><a href="${entry['link']}">${entry['title']}</a></td>
  </tr>
% endfor
</table>
