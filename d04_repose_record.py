from datetime import datetime
from operator import itemgetter
from collections import defaultdict
import re


def parse_log(line: str):
    """
    Read a log line and return a tuple of a datetime and a description.

    >>> parse_log("[1518-11-01 00:00] Guard #10 begins shift")
    (datetime.datetime(1518, 11, 1, 0, 0), 'Guard #10 begins shift')
    """
    # convert the timestamp in datetime
    time = datetime.strptime(line[1:17], "%Y-%m-%d %H:%M")
    descr = line[19:]
    return time, descr


def sleeping_guard(sorted_logs: str):
    """
    Organize logs in a dict by guard.
    The dict has as key the guard id
    and for value a list of tuples.
    Each tuple contain sleep_time, wake_time and duration of sleep.

    >>> from datetime import datetime
    >>> from pprint import pprint
    >>> logs = [
    ...     (datetime(1518, 11, 1, 0, 0), "Guard #1 begins shift"),
    ...     (datetime(1518, 11, 1, 0, 5), "falls asleep"),
    ...     (datetime(1518, 11, 1, 0, 25), "wakes up"),
    ...     (datetime(1518, 11, 1, 0, 30), "falls asleep"),
    ...     (datetime(1518, 11, 1, 0, 55), "wakes up"),
    ...     (datetime(1518, 11, 1, 23, 58), "Guard #99 begins shift"),
    ...     (datetime(1518, 11, 2, 0 ,40), "falls asleep"),
    ...     (datetime(1518, 11, 2, 0, 50), "wakes up"),
    ...     (datetime(1518, 11, 3, 0, 5), "Guard #1 begins shift"),
    ...     (datetime(1518, 11, 3, 0, 24), "falls asleep"),
    ...     (datetime(1518, 11, 3, 0, 29), "wakes up"),
    ...     (datetime(1518, 11, 4, 0, 2), "Guard #99 begins shift"),
    ...     (datetime(1518, 11, 4, 0, 36), "falls asleep"),
    ...     (datetime(1518, 11, 4, 0, 46), "wakes up"),
    ...     (datetime(1518, 11, 5, 0, 3), "Guard #99 begins shift"),
    ...     (datetime(1518, 11, 5, 0, 45), "falls asleep"),
    ...     (datetime(1518, 11, 5, 0, 55), "wakes up"),
    ... ]
    >>> pprint(sleeping_guard(logs))
    defaultdict(<class 'list'>,
                {'1': [(datetime.datetime(1518, 11, 1, 0, 5),
                        datetime.datetime(1518, 11, 1, 0, 25)),
                       (datetime.datetime(1518, 11, 1, 0, 30),
                        datetime.datetime(1518, 11, 1, 0, 55)),
                       (datetime.datetime(1518, 11, 3, 0, 24),
                        datetime.datetime(1518, 11, 3, 0, 29))],
                 '99': [(datetime.datetime(1518, 11, 2, 0, 40),
                         datetime.datetime(1518, 11, 2, 0, 50)),
                        (datetime.datetime(1518, 11, 4, 0, 36),
                         datetime.datetime(1518, 11, 4, 0, 46)),
                        (datetime.datetime(1518, 11, 5, 0, 45),
                         datetime.datetime(1518, 11, 5, 0, 55))]})
    """
    pattern = re.compile(r"(?<=^Guard #)\d+")
    by_guard = defaultdict(list)
    for log in sorted_logs:
        m = pattern.search(log[1])
        if m:
            guard_id = m.group(0)
        else:
            if log[1] == "falls asleep":
                sleep_time = log[0]
            elif log[1] == "wakes up":
                wake_time = log[0]
                by_guard[guard_id].append((
                    sleep_time,
                    wake_time,
                ))
    return by_guard


if __name__ == "__main__":
    # 0 read the logs
    with open("./input_d03.txt") as handle:
        # each log is formed by two parts date time string and description
        # use the datetime for organize a list of tuples
        # [(datetime, descriptions)]
        logs = [parse_log(line) for line in handle.readlines()]

        # 1 sort by chronological order the logs
        logs.sort(key=itemgetter(0))

        # 2 if description start with 'Guard #' i find the id
        # the bollowing logs are couple 'falls asleep' - 'wake-up'
        # for each couple compute a timedelta.
        sleeping_guard(logs)
        # sums the time delta
        # find the guard with this time greater

        # 3 for the more asleep guard find the minute
        # when he often falls asleep
