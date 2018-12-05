"""day 3"""

import re
from itertools import product
from collections import defaultdict


class Rect:

    def __init__(self, _id, x, y, lenght_x, lenght_y):
        self._id = _id
        self.x = x
        self.y = y
        self.lenght_x = lenght_x
        self.lenght_y = lenght_y

    def __str__(self) -> str:
        return (f"Rect({self._id}, {self.x}, {self.y},"
                f" {self.lenght_x}, {self.lenght_y})")

    # TODO: use __set__ instead
    def to_set(self):
        """
        Cast to set of points.

        >>> Rect(3, 5, 5, 2, 2).to_set()
        {(5, 6), (5, 5), (6, 5), (6, 6)}
        """
        end_x = self.x + self.lenght_x
        end_y = self.y + self.lenght_y
        return set(p for p in product(
            list(range(self.x, end_x)),
            list(range(self.y, end_y)),
        ))

    # TODO: use __contains__ instead
    def has_inside(self, x: int, y: int) -> bool:
        """
        Determine if a point is inside a Rect.

        >>> rect1 = Rect(1, 1, 3, 4, 4)
        >>> rect1.has_inside(2, 4)
        True
        >>> rect1.has_inside(0, 0)
        False
        """
        end_x = self.x + self.lenght_x
        end_y = self.y + self.lenght_y

        return (
            x in list(range(self.x, end_x)) and
            y in list(range(self.y, end_y))
        )


pattern = re.compile(
    r"^#(?P<_id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):"
    r"\s(?P<lenght_x>\d+)x(?P<lenght_y>\d+)$"
)


def parse(claim: str) -> Rect:
    """
    from clam raw string to the list of attribute.

    >>> r1 = parse("#1 @ 1,3: 4x4")
    >>> print(r1)
    Rect(1, 1, 3, 4, 4)
    >>> r2 = parse("#2 @ 3,1: 4x4")
    >>> print(r2)
    Rect(2, 3, 1, 4, 4)
    >>> r3 = parse("#3 @ 5,5: 2x2")
    >>> print(r3)
    Rect(3, 5, 5, 2, 2)
    """
    m = pattern.match(claim)
    kwargs = m.groupdict()
    for k, v in kwargs.items():
        kwargs[k] = int(v)
    return Rect(**kwargs)


def total_intersect_walking_ant(rects):
    """
    Walking pixel by pixel determine the total intersect.
    >>> total_intersect_walking_ant([
    ...     Rect(1, 1, 3, 4, 4), Rect(2, 1, 3, 4, 4), Rect(3, 1, 3, 4, 4)
    ... ])
    16
    >>> total_intersect_walking_ant([
    ...     Rect(1, 1, 3, 4, 4), Rect(2, 3, 1, 4, 4), Rect(3, 5, 5, 2, 2)
    ... ])
    4
    >>> total_intersect_walking_ant([
    ...     Rect(1, 1, 3, 4, 4),
    ...     Rect(2, 3, 1, 4, 4),
    ...     Rect(3, 5, 5, 2, 2),
    ...     Rect(4, 3, 3, 2, 2),
    ... ])
    4
    """
    point_map = defaultdict(set)
    # The ant is smart and jumps from a rectanges to another
    for i, rect1 in enumerate(rects[:-1]):
        end_x = rect1.x + rect1.lenght_x
        end_y = rect1.y + rect1.lenght_y
        for p in product(
            list(range(rect1.x, end_x)),
            list(range(rect1.y, end_y)),
        ):
            point_map[p].add(rect1._id)
            for rect2 in rects[i + 1:]:
                if rect2.has_inside(*p):
                    point_map[p].add(rect2._id)
                    break
    return sum([
        1 for catalog in point_map.values() if len(catalog) > 1
    ])


def total_intersect(rects):
    """
    Walking determine the total intersect using sets.
    >>> total_intersect([
    ...     Rect(1, 1, 3, 4, 4), Rect(2, 1, 3, 4, 4), Rect(3, 1, 3, 4, 4)
    ... ])
    16
    >>> total_intersect([
    ...     Rect(1, 1, 3, 4, 4), Rect(2, 3, 1, 4, 4), Rect(3, 5, 5, 2, 2)
    ... ])
    4
    >>> total_intersect([
    ...     Rect(1, 1, 3, 4, 4),
    ...     Rect(2, 3, 1, 4, 4),
    ...     Rect(3, 5, 5, 2, 2),
    ...     Rect(4, 3, 3, 2, 2),
    ... ])
    4
    """
    total = []
    for i, rect in enumerate(rects):
        others = rects[:i] + rects[i + 1:]
        union_others = set.union(*[r.to_set() for r in others])
        rect_intersect = union_others.intersection(rect.to_set())
        total.append(rect_intersect)
    return len(list(set.union(*total)))


def with_no_intersect(rects):
    """
    find rect that has no intersections.

    >>> print(with_no_intersect([
    ...     Rect(1, 1, 3, 4, 4), Rect(2, 3, 1, 4, 4), Rect(3, 5, 5, 2, 2)
    ... ]))
    Rect(3, 5, 5, 2, 2)
    """
    for i, rect in enumerate(rects):
        all_other_rects = rects[:i] + rects[i+1:]
        all_other_points = set.union(*[r.to_set() for r in all_other_rects])
        if not rect.to_set() & all_other_points:
            return rect


if __name__ == "__main__":
    with open("./input_d03.txt") as handle:
        rects = [parse(line) for line in handle.readlines()]

    print(total_intersect(rects))
    print(with_no_intersect(rects))
