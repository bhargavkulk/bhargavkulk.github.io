<%!
from datetime import datetime
def fmt_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%b %d, %Y")
    except Exception:
        return date_str
%>

<%inherit file="base.mako"/>

<%block name="content">
    ${content_}
    <h2>Recent Posts</h2>
    % for post in metadata['blog_index'][:5]:
        <div class="test-entry">
            <div class="test-date">${fmt_date(post['date'])}</div>
            <div class="test-content">
                <div class="test-title"><a href="${post['url']}" class="blogtitle">${post['title']}</a></div>
                <div class="test-summary">${post['summary']}</div>
            </div>
        </div>
    % endfor
</%block>
