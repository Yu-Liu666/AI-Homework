"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now).
See Courseworks for detailed instructions.

@author: Yu Liu (yl3957)
"""

import time


def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped.
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]

    new_state = []
    for row in range(len(state)):
        new_row = []
        for column in range(len(state[row])):
            if row == i1 and column == j1:
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else:
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions.
    The result should be a list containing (Action, state) tuples.
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))),
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))]
    """

    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable.
    x = 0
    flag = False
    for row in state:
        y = 0
        for num in row:
            if num == 0:
                flag = True
                break
            y = y + 1
        if flag:
            break

        x = x + 1
    if y + 1 < len(state[0]):
        child_states.append(("Left", swap_cells(state, x, y, x, y + 1)))
    if y - 1 >= 0:
        child_states.append(("Right", swap_cells(state, x, y, x, y - 1)))
    if x + 1 < len(state):
        child_states.append(("Up", swap_cells(state, x, y, x + 1, y)))
    if x - 1 >= 0:
        child_states.append(("Down", swap_cells(state, x, y, x - 1, y)))

    return child_states


def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise.
    """

    n = 0
    for row in state:
        for num in row:
            if n != num:
                return False
            n = n + 1
    return True  # Replace this


def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0
    solution = []
    final = None
    fringe = []
    closed = set()
    parents = {}
    # YOUR CODE HERE
    fringe.append(state)
    flag = False
    while len(fringe) > 0:
        max_fringe = max(max_fringe, len(fringe))
        s = fringe.pop(0)
        if s in closed:
            continue
        closed.add(s)
        if goal_test(s):
            final = s
            flag = True
            break
        # if s not in closed:
        states_expanded = states_expanded + 1
        for successor in get_successors(s):
            if successor[1] not in closed:
                parents[successor[1]] = [s, successor[0]]
                fringe.append(successor[1])
        if flag:
            break
    if flag:
        while final in parents:
            solution.insert(0, parents[final][1])
            final = parents[final][0]
        return solution, states_expanded, max_fringe
    else:
        return None, states_expanded, max_fringe  # No solution found


def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0
    solution = []
    final = None
    fringe = []
    closed = set()
    parents = {}
    # YOUR CODE HERE
    fringe.append(state)
    flag = False
    while len(fringe) > 0:
        max_fringe = max(max_fringe, len(fringe))
        s = fringe.pop()
        if s in closed:
            continue
        closed.add(s)
        if goal_test(s):
            final = s
            flag = True
            break
        # if s not in closed:
        states_expanded = states_expanded + 1
        for successor in get_successors(s):
            if successor[1] not in closed:
                parents[successor[1]] = [s, successor[0]]
                fringe.append(successor[1])
        if flag:
            break
    if flag:
        while final in parents:
            solution.insert(0, parents[final][1])
            final = parents[final][0]

        return solution, states_expanded, max_fringe
    else:
        return None, states_expanded, max_fringe  # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """
    count = 0
    n = 0
    for row in state:
        for num in row:
            if n != num:
                count = count + 1
            n = n + 1
    return count


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """
    dis = 0
    x = 0
    for row in state:
        y = 0
        for num in row:
            dis = dis + abs(num // 3 - x) + abs(num % 3 - y)
            y = y + 1
        x = x + 1
    return dis

def best_first(state, heuristic):
    """
    Best first search.
    Returns three value s: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0
    solution = []
    final = None
    fringe = []
    closed = set()
    parents = {}
    heappush(fringe, (heuristic(state), state))
    flag = False
    while len(fringe) > 0:
        max_fringe = max(max_fringe, len(fringe))
        s = heappop(fringe)
        if s[1] in closed:
            continue
        closed.add(s[1])
        if goal_test(s[1]):
            final = s[1]
            flag = True
            break
        states_expanded = states_expanded + 1
        for successor in get_successors(s[1]):
            if successor[1] not in closed:
                parents[successor[1]] = [s[1], successor[0]]
                heappush(fringe, (heuristic(successor[1]), successor[1]))
        if flag:
            break
    if flag:
        while final in parents:
            solution.insert(0, parents[final][1])
            final = parents[final][0]
        return solution, states_expanded, max_fringe
    else:
        return None, states_expanded, max_fringe  # No solution found


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0
    solution = []
    final = None
    fringe = []
    closed = set()
    parents = {}
    cost = {}
    cost[state] = 0
    # YOUR CODE HERE
    heappush(fringe, (heuristic(state) + cost[state], state))
    flag = False
    while len(fringe) > 0:
        max_fringe = max(max_fringe, len(fringe))
        s = heappop(fringe)
        if s[1] in closed:
            continue
        closed.add(s[1])
        if goal_test(s[1]):
            final = s[1]
            flag = True
            break
        # if s not in closed:
        states_expanded = states_expanded + 1
        for successor in get_successors(s[1]):
            if successor[1] not in closed:
                parents[successor[1]] = [s[1], successor[0]]
                c = cost[s[1]]
                cost[successor[1]] = c + 1
                heappush(fringe, (heuristic(successor[1]) + cost[successor[1]], successor[1]))
        if flag:
            break
    if flag:
        while final in parents:
            solution.insert(0, parents[final][1])
            final = parents[final][0]
        return solution, states_expanded, max_fringe
    else:
        return None, states_expanded, max_fringe  # No solution found


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output.
    """
    if solution is None:
        print("No solution found.")
    else:
        print("Solution has {} actions.".format(len(solution)))
    print(solution)
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))


if __name__ == "__main__":

    # Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8),
                  (3, 6, 7))
    # print(goal_test(((0, 1, 2), (3, 4, 5), (6, 7, 8))))
    # More difficult test case
    # test_state = ((7, 2, 4),
    #               (5, 0, 6),
    #               (8, 3, 1))
    # test_state = ((1, 0, 2), (3, 4, 5), (6, 7, 8))

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state)  #
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end - start))

    print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

