"""day 6"""
from operator import itemgetter
from itertools import product
from pprint import pprint


def parse(line: str):
    """
    parse a line and return a tuple, that reppresent a 2D point.

    >>> parse("4, 78")
    (4, 78)
    """
    return tuple(int(coord) for coord in line.split(', '))


def find_borders(kernels):
    """
    return the borders of our simulation matrix.
    Over these these is infinite growth.

    >>> find_borders({(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)})
    (1, 9, 1, 8)
    """
    north_limit = min(kernels, key=itemgetter(1))[1]
    south_limit = max(kernels, key=itemgetter(1))[1]
    west_limit = min(kernels, key=itemgetter(0))[0]
    east_limit = max(kernels, key=itemgetter(0))[0]
    return north_limit, south_limit, west_limit, east_limit


def distance(p, q) -> int:
    """
    Return the Manhattan distance between two points.

    >>> distance((1, 2), (3, 4))
    4

    :param p: first 2d point
    :param q: other 2d point
    :return: distance
    """
    return sum(abs(comp_p - comp_q) for comp_p, comp_q in zip(p, q))


def greatest_area_around_a_kernel(kernels) -> int:
    """
    Given a list of 2D kernel coordinate,
    find the greatest area using
    manhattan distance

    >>> greatest_area_around_a_kernel(
    ...     [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    ... )
    17
    """
    # map_limits
    north_limit, south_limit, west_limit, east_limit = find_borders(kernels)

    areas = [set([k, ]) for k in kernels]
    contented = []
    # generate all points of the matrix
    all_points = product(
        range(west_limit - 1, east_limit + 2),
        range(north_limit - 1, south_limit + 2)
    )
    # find all distances, and group point on lowest distance to kernerls
    for p in all_points:
        distances = [distance(k, p) for k in kernels]
        min_dist = min(distances)
        if distances.count(min_dist) > 1:
            contented.append(p)
        else:
            i = distances.index(min_dist)
            areas[i].add(p)

    # remove points that touch any borders.
    to_remove = []
    finite_areas = []
    for i, area in enumerate(areas):
        n, s, w, e = find_borders(area)
        if any([
            n == north_limit - 1,
            s == south_limit + 1,
            w == west_limit - 1,
            e == east_limit + 1
        ]):
            to_remove.append(i)
            continue
        else:
            finite_areas.append(area)

    return max([len(a) for a in finite_areas])


def greatest_area_between_kernels(kernels, max_total_distance) -> int:
    """
    Given a list of 2D kernel coordinate,
    find the greatest area between kernels
    with a total distance between then equal to
    max_total_distance.
    Distances are computed using manhattan.

    >>> greatest_area_between_kernels(
    ...     [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)],
    ...     32
    ... )
    16
    """
    # map_limits
    north_limit, south_limit, west_limit, east_limit = find_borders(kernels)

    area = []
    # generate all points of the matrix
    all_points = product(
        range(west_limit - 1, east_limit + 2),
        range(north_limit - 1, south_limit + 2)
    )
    # find the points between kernels
    for p in all_points:
        tot_distance = sum([distance(k, p) for k in kernels])
        if tot_distance < max_total_distance:
            area.append(p)

    return len(area)


if __name__ == "__main__":
    with open("./input_d06.txt") as handle:
        kernels = [parse(line) for line in handle.readlines()]

    print(greatest_area_around_a_kernel(kernels))
    print(greatest_area_between_kernels(kernels, 10_000))
