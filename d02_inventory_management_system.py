from collections import Counter
from difflib import get_close_matches, ndiff


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


def in_common(box_ids: str) -> str:
    """
    Search ids that differ by one letter
    and returns characters in commons.

    >>> in_common([
    ... 'abcde',  # differ of 2 to the 5 - too much
    ... 'fghij',  # differ of 1 to the 4
    ... 'klmno',
    ... 'pqrst',
    ... 'fguij',
    ... 'axcye',
    ... 'wvxyz',
    ... ])
    'fgij'

    :param box_ids: list of the ids
    :return: the characters in commons of the sequences that differ by one.
    """
    for i, sequence in enumerate(box_ids[:-1]):
        closed = get_close_matches(sequence, box_ids[i+1:], n=1, cutoff=0.8)
        if len(closed) == 1:
            closest = closed[0]
            in_common = ''.join(
                [li[2] for li in ndiff(sequence, closest) if li[0] == ' ']
            )
            if len(in_common) == len(sequence) - 1:
                return(in_common)


if __name__ == "__main__":
    with open("./input_d02.txt") as handle:
        box_ids = handle.readlines()

    print(checksum(box_ids))  # -> 6723
    print(in_common(box_ids))  # -> prtkqyluiusocwvaezjmhmfgx
