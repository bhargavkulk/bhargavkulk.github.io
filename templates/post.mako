<%inherit file="base.mako"/>
<%!
from date_utils import format_date_attr, parse_org_date
%>

<h1>${title}</h1>
% if date:
  <p><time datetime="${format_date_attr(date)}">${parse_org_date(date).strftime('%b %d, %Y')}</time></p>
% endif
${content | n}
