"""day 6"""
from operator import itemgetter
from copy import deepcopy


def parse(line: str):
    """
    parse a line and return a tuple, that reppresent a 2D point.

    >>> parse("4, 78")
    (4, 78)
    """
    return tuple(int(coord) for coord in line.split(', '))


def greatest_area(kernels) -> int:
    """
    Given a list of 2D kernel coordinate,
    find the greatest area using
    square textallation, cross incrementation
    of Voronoi's bubbles.

    >>> greatest_area([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)])
    17
    """
    # tasselion
    cross = [(-1, 0), (0, 1), (1, 0), (0, -1)]
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
    while is_expanded:
        is_expanded = False
        # each loop add coordinates four coordinate using
        # nearest cross cell.
        covered_points = [p for b in voronoi_bubbles for p in b]
        bubbles_borders_next = deepcopy(bubbles_borders)
        contented_point = set([])
        for i, bubble in enumerate(voronoi_bubbles):
            for point in bubbles_borders[i]:
                for coord in cross:
                    new_point = (point[0] + coord[0], point[1] + coord[1])
                    for each_bor in bubbles_borders_next:
                        if new_point in each_bor:
                            each_bor.remove(new_point)
                            contented_point.add(new_point)
                    if (
                        # not other bubble should have the new_point
                        new_point not in covered_points
                        # the new_point should be inside the geographic limits
                        and nord_limit[1] >= new_point[1] >= south_limit[1]
                        and west_limit[0] >= new_point[0] >= east_limit[0]
                        # the new_point isn't contented
                        and new_point not in contented_point
                        # and the new point is not already in the buble
                        # and new_point not in bubble
                    ):
                        bubbles_borders_next[i].add(new_point)
                        is_expanded = True
            bubbles_borders[i] = bubbles_borders_next[i]
            voronoi_bubbles[i] = bubble | set(bubbles_borders_next[i])

    return max([len(b) for b in voronoi_bubbles])


if __name__ == "__main__":
    with open("./input_d06.txt") as handle:
        kernels = [parse(line) for line in handle.readlines()]

    greatest_area(kernels)
