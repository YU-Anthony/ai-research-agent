"""DST-aware guard for the pair of GitHub UTC schedules (standard library only)."""
from datetime import datetime, timezone
import os
from zoneinfo import ZoneInfo


def should_monitor(event, now):
    local = now.astimezone(ZoneInfo('America/New_York'))
    return event == 'workflow_dispatch' or (local.weekday() == 0 and local.hour == 9)


if __name__ == '__main__':
    proceed = should_monitor(os.environ['EVENT'], datetime.now(timezone.utc))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'proceed={str(proceed).lower()}\n')
