from datetime import datetime
from operator import itemgetter
from collections import defaultdict
import re
from pprint import pprint


def parse_log(line: str):
    """
    Read a log line and return a tuple of a datetime and a description.

    >>> parse_log("[1518-11-01 00:00] Guard #10 begins shift")
    (datetime.datetime(1518, 11, 1, 0, 0), 'Guard #10 begins shift')
    """
    # convert the timestamp in datetime
    time = datetime.strptime(line[1:17], "%Y-%m-%d %H:%M")
    descr = (line[19:]).strip()
    return time, descr


def sleeping_guard(sorted_logs: str):
    """
    Organize logs in a dict by guard.
    The dict has as key the guard id
    and for value a list of tuples.
    Each tuple contains wake_time and duration of sleep.

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
        elif log[1] == "falls asleep":
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
    with open("./input_d04.txt") as handle:
        # each log is formed by two parts date time string and description
        # use the datetime for organize a list of tuples
        # [(datetime, descriptions)]
        logs = [parse_log(line) for line in handle.readlines()]

    # 1 sort by chronological order the logs
    logs.sort(key=itemgetter(0))

    # 2 if description start with 'Guard #' i find the id
    # the following logs are couple 'falls asleep' - 'wake-up'
    time_by_guard = sleeping_guard(logs)
    # pprint(time_by_guard)
    # for each couple compute a timedelta
    durations_by_guard = defaultdict(int)
    for guard_id, sleep_time in time_by_guard.items():
        for asleep, awake in sleep_time:
            durations_by_guard[guard_id] += (awake.minute - asleep.minute)
    # pprint(durations_by_guard)

    # and sums the timedeltas.
    guard_by_duration = {
        durations: guard_id
        for guard_id, durations in durations_by_guard.items()
    }
    # pprint(guard_by_sleep_sum)

    # find the guard with this time greater
    longest_sleep_sum = max(guard_by_duration.keys())
    napster = guard_by_duration[longest_sleep_sum]
    print(f"the guard who often falls asleep is {napster}")

    # 3 for the more asleep guard
    napster_times = time_by_guard[napster]

    # collect of often per minute he felt asleep.
    sleep_by_minute = defaultdict(int)
    for asleep, awake in napster_times:
        start_minute = asleep.minute
        end_minute = awake.minute
        for minute in range(start_minute, end_minute):
            sleep_by_minute[minute] += 1
    # pprint(sleep_by_minute)

    # and find the minute when often he felt asleep
    sleep_by_minute = {
        freq: minute for minute, freq in sleep_by_minute.items()
    }
    max_freq = max(sleep_by_minute.keys())
    more_often_minute = sleep_by_minute[max_freq]
    print(
        "the minute after 00:00 when more often sleep is ",
        more_often_minute
    )
    print("The product is ", more_often_minute * int(napster))
