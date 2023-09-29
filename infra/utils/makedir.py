import datetime
from pathlib import Path


def make_path(base_path, child_path):
    """
    create year/month/day dir
    """

    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    cur_dir = Path(base_path)
    new_dir = cur_dir / str(year) / str(month) / str(day) / child_path
    if not new_dir.exists():
        new_dir.mkdir(parents=True)
    return new_dir.as_posix()
