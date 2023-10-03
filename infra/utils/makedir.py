import datetime
from pathlib import Path


def make_path(base_path, child_path):
    """
    create year/month/day dir
    """

    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    month = f'0{month}' if month < 10 else str(month)
    day = f'0{day}' if day < 10 else str(day)
    cur_dir = Path(base_path)
    new_dir = cur_dir / str(year) / month / day / child_path
    if not new_dir.exists():
        new_dir.mkdir(parents=True)
    return new_dir.as_posix()
