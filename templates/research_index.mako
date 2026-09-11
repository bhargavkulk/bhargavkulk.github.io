<%inherit file="base.mako"/>
<%!
from date_utils import parse_org_date
%>

<table>
% for entry in sorted(research_index, key=lambda entry: parse_org_date(entry['date']), reverse=True):
  <tr>
    <td>
      ${entry['conf']}
    </td>
    <td>
      <a href="${entry['link']}">${entry['title']}</a>
      <br>${entry['authors']}
    </td>
  </tr>
% endfor
</table>
