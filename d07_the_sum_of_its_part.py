from collections import defaultdict
from pprint import pprint


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
    for key, values in graph.items():
        values.sort()
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
    'C'
    """
    values = set.union(*[set(v) for v in graph.values()])
    keys = set(graph.keys())
    return list(keys - values)[0]


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
    'E'
    """
    values = set.union(*[set(v) for v in graph.values()])
    keys = set(graph.keys())
    return list(values - keys)[0]


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

    correct_list = [beging]
    forks = [beging]

    while True:
        try:
            previous_value = min(forks)
        except ValueError:
            break
        else:
            forks.remove(previous_value)
            # POTENTIAL ERROR: this is working  because the stop follow
            # the alphabetical order!
            # change to do, put always stop at the end of the listes!
            if graph[previous_value][0] != stop:
                # normally - follow the links
                forks.extend(graph[previous_value])
                next_value = graph[previous_value][0]
                correct_list.append(next_value)
            else:
                # other wise fish on forks
                next_value = previous_value
                if next_value not in correct_list:
                    correct_list.append(next_value)
    correct_list.append(stop)
    return ''.join(correct_list)
