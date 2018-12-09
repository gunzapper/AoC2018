"""day 6"""
from operator import itemgetter
from pprint import pprint


def parse(line: str):
    """
    parse a line and return a tuple, that reppresent a 2D point.

    >>> parse("4, 78")
    (4, 78)
    """
    return tuple(int(coord) for coord in line.split(', '))


def new_border(bubble, old_border):
    """
    compute the new border for bubble with using old_border.

    >>> new_border({(5, 5)}, {(5, 5)})
    [(4, 5), (5, 6), (6, 5), (5, 4)]
    >>> new_border(
    ...     {(5, 5), (4, 5), (5, 6), (6, 5), (5, 4)},
    ...     {(4, 5), (5, 6), (6, 5), (5, 4)}
    ... )
    [(3, 5), (4, 6), (4, 4), (4, 4), (6, 4), (5, 3), (4, 6), (5, 7), (6, 6), (6, 6), (7, 5), (6, 4)]
    """
    # tasselion
    cross = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    new_points = []
    for point in old_border:  # bubbles_borders[i]:
        for coord in cross:
            new_point = (point[0] + coord[0], point[1] + coord[1])
            if new_point not in bubble:
                new_points.append(new_point)
    return new_points


def point_contented(new_points, bubbles_borders_next):
    """
    check if a point if contented to another border
    return the list of contenetd points

    >>> point_contented(
    ...     [(5, 5), (4, 5), (5, 6), (6, 5), (5, 4)],
    ...     [{(4, 5), (5, 6)}, {(6, 5), (5, 4)}]
    ... )
    [(4, 5), (5, 6), (6, 5), (5, 4)]
    """
    contented_point = []
    for new_point in new_points:
        for each_bor in bubbles_borders_next:
            if new_point in each_bor:
                # each_bor.remove(new_point)
                contented_point.append(new_point)
                break
    return contented_point


def greatest_area(kernels) -> int:
    """
    Given a list of 2D kernel coordinate,
    find the greatest area using
    square textallation, cross incrementation
    of Voronoi's bubbles.

    >>> greatest_area([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)])
    17
    """
    # map_limits
    # bubbles can expand only among these limits
    # (crossed these there is ich sint leones of infinite expantion
    # and I need a way to avoid the infinite loop of infinite expantion)
    nord_limit = max(kernels, key=itemgetter(1))
    south_limit = min(kernels, key=itemgetter(1))
    west_limit = max(kernels, key=itemgetter(0))
    east_limit = min(kernels, key=itemgetter(0))
    # init
    # for all point in each bubble
    voronoi_bubbles = [set([coord]) for coord in kernels]
    # for bubble surfaces
    bubbles_borders = [set([coord, ]) for coord in kernels]
    is_expanded = True
    touch_the_limits = set([])
    while is_expanded:
        is_expanded = False
        # each loop add coordinates four coordinate using
        # nearest cross cell.
        covered_points = [p for b in voronoi_bubbles for p in b]
        bubbles_borders_next = []
        contented_point = set([])
        for i, bubble in enumerate(voronoi_bubbles):
            new_points = new_border(bubble, bubbles_borders[i])
            # check if points are contented
            new_contented_points, free_points = point_contented(
                new_points, bubbles_borders_next
            )

            for point in new_contented_points:
                for each_bor in bubbles_borders_next:
                    if point in each_bor:
                        each_bor.remove(point)

            # print(new_points)
            next_border = set([])
            for new_point in free_points:
                if not (
                    # the new_point should be inside the geographic limits
                    nord_limit[1] >= new_point[1] >= south_limit[1] and
                    west_limit[0] >= new_point[0] >= east_limit[0]
                ):
                    touch_the_limits.add(i)
                elif (
                    # not other bubble should have the new_point
                    new_point not in covered_points
                    # the new_point isn't contented
                    and new_point not in contented_point
                ):
                    next_border.add(new_point)
                    is_expanded = True
            bubbles_borders_next.append(next_border)
        bubbles_borders = bubbles_borders_next

        for i, bubble in enumerate(voronoi_bubbles):
            voronoi_bubbles[i] = bubble | set(bubbles_borders[i])
        # pprint(voronoi_bubbles)

    print(touch_the_limits)
    finite_bubbles = []
    for i, bubble in enumerate(voronoi_bubbles):
        if i not in touch_the_limits:
            finite_bubbles.append(bubble)

    return max([len(b) for b in finite_bubbles])


if __name__ == "__main__":
    with open("./input_d06.txt") as handle:
        kernels = [parse(line) for line in handle.readlines()]

    greatest_area(kernels)
