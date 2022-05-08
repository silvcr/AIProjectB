"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

Sample Solution

Note: Best efforts have been made to ensure correctness, but as with all
software, there is always the possibility of an unforeseen bug/issue. 
"""

from math import inf
from queue import PriorityQueue

def backtrace_path(goal_node, start_node, came_from):
    """
    Compute minimal cost path from the goal node to the start node given 
    a dictionary of "came from" node mappings. 

    Args:
        goal_node: Goal node object (path end).
        start_node: Start node object (path start).
        came_from: Dictionary from given node to previous node in path.

    Returns:
        List of nodes denoting path from start to goal.
    """
    path = []
    curr_node = goal_node
    while curr_node != start_node:
        path.append(curr_node)
        curr_node = came_from[curr_node]
    path.append(start_node)
    path.reverse()
    return path

def a_star(start_node, goal_node, f_h, f_n, f_w=lambda *_: 1):
    """
    Perform an A* search given start and end node objects, and functions
    to compute problem-domain-specific values. As long as nodes are hashable
    objects, this implementation should work correctly for any search graph.

    In this solution we also handle ties in f(x) by using the isolated 
    heuristic value h(x) as a tiebreaker. This can result in significant 
    speedups in graphs where there are many paths with the same cost.

    Args:
        start_node: Start node object.
        goal_node: Goal node object.
        f_h: Heuristic function   ~ node, goal_node => est. cost
        f_n: Neighbour function   ~ node => [neighbour nodes]
        f_w: Edge-weight function ~ node_a, node_b => edge weight (Default 1)

    Returns:
        List of path nodes if path exists, else None.
    """
    open_nodes = PriorityQueue()
    open_nodes.put((0, 0, start_node))
    closed_nodes = set()
    came_from = {}
    g = { start_node: 0 }

    while not open_nodes.empty():
        # Get lowest f(x) cost node, or lowest h(x) in case of ties
        *_, curr_node = open_nodes.get()
        closed_nodes.add(curr_node)

        # Check if we reached goal
        if curr_node == goal_node:
            return backtrace_path(goal_node, start_node, came_from)

        # Expand and add neighbours to queue
        for neighbour_node in f_n(curr_node):
            # Compute neighbour g(x) and ensure it is not in closed set
            neighbour_g = g[curr_node] + f_w(curr_node, neighbour_node)
            is_lowest_cost_so_far = neighbour_g < g.get(neighbour_node, inf)
            closed_node = neighbour_node in closed_nodes

            if not closed_node and is_lowest_cost_so_far:
                # Update g/parent values for this neighbour node
                g[neighbour_node] = neighbour_g
                came_from[neighbour_node] = curr_node

                # Add to queue with priority by f(x), then h(x) (for ties)
                neighbour_h = f_h(neighbour_node, goal_node)
                neighbour_f = neighbour_g + neighbour_h
                open_nodes.put((neighbour_f, neighbour_h, neighbour_node))

    # No path found if we reach this point
    return None
