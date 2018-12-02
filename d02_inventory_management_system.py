from collections import Counter


def checksum(box_ids: str) -> int:
    """
    Computes the checksum from the ids' list.
    The checksum is defined as
    how many ids have two of any character
    by how many ids have three of any character.

    >>> checksum([
    ...     'abcdef',  # zero of all chararcter
    ...     'bababc',  # two of a and three of b - it counts for both
    ...     'abbcde',  # two of b
    ...     'abcccd',  # three of c
    ...     'aabcdd',  # two a and two b - but it counts once
    ...     'abcdee',  # two of e
    ...     'ababab',  # three of a and three of b - but it counts once
    ... ])
    12

    :param box_ids: list of the ids
    :return: the checksum as defined above.
    """
    how_many_three = 0
    how_many_two = 0
    for box_id in box_ids:
        counter = Counter(box_id)
        if 2 in counter.values():
            how_many_two += 1
        if 3 in counter.values():
            how_many_three += 1
    return how_many_two * how_many_three


if __name__ == "__main__":
    with open("./input_d02.txt") as handle:
        box_ids = handle.readlines()

    print(checksum(box_ids))
