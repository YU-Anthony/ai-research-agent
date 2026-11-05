"""Choose the daily DST schedule by its trigger, not the delayed runner clock."""
from datetime import datetime, timezone
import os
from zoneinfo import ZoneInfo


def should_monitor(event, now, schedule=None):
    if event == 'workflow_dispatch':
        return True
    if event != 'schedule':
        return False
    local = now.astimezone(ZoneInfo('America/New_York'))
    expected = '0 13 * * *' if local.dst() else '0 14 * * *'
    return schedule == expected


if __name__ == '__main__':
    proceed = should_monitor(os.environ['EVENT'], datetime.now(timezone.utc), os.environ.get('SCHEDULE'))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'proceed={str(proceed).lower()}\n')
