from collections import defaultdict
from copy import copy


def lines2graph(lines):
    """
    From the lines describing
    how part is prerequisite for another,
    return a dictionary the describe the graph.

    >>> lines2graph([
    ...     "Step C must be finished before step A can begin.",
    ...     "Step C must be finished before step F can begin.",
    ...     "Step A must be finished before step B can begin.",
    ...     "Step A must be finished before step D can begin.",
    ...     "Step B must be finished before step E can begin.",
    ...     "Step D must be finished before step E can begin.",
    ...     "Step F must be finished before step E can begin.",
    ... ])
    defaultdict(<class 'list'>, {'C': ['A', 'F'], 'A': ['B', 'D'], 'B': ['E'], 'D': ['E'], 'F': ['E']})
    """
    graph = defaultdict(list)
    for line in lines:
        start_node = line[5]
        end_node = line[36]
        graph[start_node].append(end_node)
    # format the graph
    # orderd values - with stop always at end
    stop = find_stop(graph)
    for key, values in graph.items():
        values.sort()
        if stop in values:
            values.remove(stop)
            values.append(stop)
    return graph


def find_begin(graph):
    """
    Searching begin of the graph as key not in values list.

    >>> find_begin({
    ...     'C': ['A', 'F'],
    ...     'A': ['B', 'D'],
    ...     'B': ['E'],
    ...     'D': ['E'],
    ...     'F': ['E'],
    ... })
    {'C'}
    """
    values = set.union(*[set(v) for v in graph.values()])
    keys = set(graph.keys())
    return keys - values


def find_stop(graph):
    """
    Searching stop of the graph as value not in keys.

    >>> find_stop({
    ...     'C': ['A', 'F'],
    ...     'A': ['B', 'D'],
    ...     'B': ['E'],
    ...     'D': ['E'],
    ...     'F': ['E'],
    ... })
    {'E'}
    """
    values = set.union(*[set(v) for v in graph.values()])
    keys = set(graph.keys())
    return values - keys


def correct_order(lines):
    """
    from lines get the correct order of istructions.

    >>> correct_order([
    ...     "Step C must be finished before step A can begin.",
    ...     "Step C must be finished before step F can begin.",
    ...     "Step A must be finished before step B can begin.",
    ...     "Step A must be finished before step D can begin.",
    ...     "Step B must be finished before step E can begin.",
    ...     "Step D must be finished before step E can begin.",
    ...     "Step F must be finished before step E can begin.",
    ... ])
    'CABDFE'
    """
    graph = lines2graph(lines)

    beging = find_begin(graph)
    stop = find_stop(graph)

    correct_list = []
    forks = copy(beging)

    while True:
        try:
            previous_value = min(forks)
            if previous_value not in correct_list:
                correct_list.append(previous_value)
        except ValueError:
            break
        else:
            forks -= {previous_value}
            if graph[previous_value][0] not in stop:
                # normally - follow the links
                forks = forks.union(set(graph[previous_value]))
                forks -= stop
                # next values will be no already in correct_list
                for candidate in graph[previous_value]:
                    if candidate not in correct_list:
                        next_value = candidate
                        correct_list.append(next_value)
                        break
    correct_list.append(list(stop)[0])
    return ''.join(correct_list)


if __name__ == "__main__":

    with open("./input_d07.txt", "r") as handle:
        lines = handle.readlines()

    print(correct_order(lines))
