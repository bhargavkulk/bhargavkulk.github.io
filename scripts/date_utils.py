from datetime import datetime
import re


_ORG_TIMESTAMP = re.compile(
    r'^[\[<](\d{4}-\d{2}-\d{2})(?:\s+\w{3})?(?:\s+(\d{2}:\d{2}))?.*[\]>]$'
)


def parse_org_date(value: str) -> datetime:
    """Parse an ISO date or Org timestamp; assumes a YYYY-MM-DD date."""
    match = _ORG_TIMESTAMP.fullmatch(value)
    if match:
        date, time = match.groups()
        return datetime.strptime(f'{date} {time or "00:00"}', '%Y-%m-%d %H:%M')
    return datetime.strptime(value, '%Y-%m-%d')


def format_date_attr(value: str) -> str:
    """Format a date for HTML; assumes `value` is accepted by parse_org_date."""
    match = _ORG_TIMESTAMP.fullmatch(value)
    parsed = parse_org_date(value)
    if match and match.group(2):
        return parsed.isoformat(timespec='minutes')
    return parsed.date().isoformat()
