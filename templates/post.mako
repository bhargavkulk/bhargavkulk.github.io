<%inherit file="base.mako"/>
<%!
from datetime import datetime
%>

<h1>${title}</h1>
% if date:
  <p><time datetime="${date}">${datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y')}</time></p>
% endif
${content | n}
