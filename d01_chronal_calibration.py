from itertools import cycle


def reached_twice(changes: list) -> int:
    """
    Find the first value of the frecquency reached twice.

    >>> reached_twice([1, -1])
    0
    >>> reached_twice([3, 3, 4, -2, -4])
    10
    >>> reached_twice([-6, 3, 8, 5, -6])
    5
    >>> reached_twice([7, 7, -2, -7, -4])
    14

    :param changes: list of value commulative to add to return the frequency.
    :return: the value of the frequency first reached twice.
    """
    frequencies = [0, ]
    for change in cycle(changes):
        new_frequency = frequencies[-1] + change
        if new_frequency in frequencies:
            return new_frequency
        frequencies.append(new_frequency)


if __name__ == "__main__":
    # for the first part I have to sum all the value of the file.
    # It could be considered the frequency at at the end of
    # the list of changes.
    with open("./input_d1.txt") as handle:
        changes = [int(line) for line in handle]
        final_freq = sum(changes)
        print(final_freq)
    #  -> 466

    # for the second part I need to reach
    print(reached_twice(changes))
    #  -> 750
