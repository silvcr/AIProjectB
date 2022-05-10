def valid_candidate(candidate, board_dict, board_size):
    """ Function to check if a candidate move is valid"""
    # check if move is in board and not on a forbidden hex
    if 0 <= candidate[0] < board_size and 0 <= candidate[1] < board_size and candidate not in board_dict.keys():
        return True
    else:
        return False


def find_candidates(current_position, board_dict, board_size):
    """ Function to generate valid neighbors from a current move"""
    # Generate the six surrounding neighbors to a move
    candidates = [(current_position[0], current_position[1] + 1), (current_position[0], current_position[1] - 1),
                  (current_position[0] + 1, current_position[1]), (current_position[0] - 1, current_position[1]),
                  (current_position[0] - 1, current_position[1] + 1),
                  (current_position[0] + 1, current_position[1] - 1)]
    legal_candidates = []
    # Filter out non-valid neighbors
    for move in candidates:
        if valid_candidate(move, board_dict=board_dict, board_size=board_size):
            legal_candidates.append(move)
    return legal_candidates

"""
Altered version of a_star from sample solution in Project A in COMP30024 Sem 1 2022
"""

from math import inf
from queue import PriorityQueue

def compute_path(n, start_coord, goal_coord, opp_coords, f_h=lambda *_: 0):
    """
    Compute lowest cost path on Cachex board. Internally uses A*.

        f_h: Heuristic function (reverts to UCS if not supplied).

    Returns:
        List of path coordinates, or empty list if no path exists.
    """

    # Using a set will be a lot more efficient than a list here
    opp_coords = set(opp_coords)

    # Returns true iff coord is valid (inside board bounds, not occupied)
    # changed so its not occupied by OPPONENT

    def valid_coord(coord):
        (r, q) = coord
        return 0 <= r < n and 0 <= q < n and (not coord in opp_coords)

    # Returns only valid neighbour coords
    def neighbours(coord):
        return filter(valid_coord, hex_neighbours(coord))

    # Run A* and return path (default empty list if no path)
    return a_star(start_coord, goal_coord, f_h, neighbours) or []


""" Will have to be changed to another heuristic --> Perhaps the manhattan for teleporters with 
    start and end as chain of hexs """

def axial_distance(coord, goal_coord):
    """
    Axial distance heuristic for use in hex-grid based A* search.
    Returns cost (or underestimate of cost) from current coord to goal coord.
    """
    (a_r, a_q) = coord
    (b_r, b_q) = goal_coord
    return (abs(a_q - b_q)
        + abs(a_q + a_r - b_q - b_r)
        + abs(a_r - b_r)) / 2

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
    Perform an A* search given start and end node objects and return path if found
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

def add_coords(a, b):

    return (a[0] + b[0], a[1] + b[1])

def hex_neighbours(coord):
    """
    Utility function to compute neighbours of a given hex coord.

    Args:
        coord: Coord tuple (r, q).

    Returns:
        List of neighbour coordinate tuples [(r, q)].
    """
    return [add_coords(coord, offset) for offset in \
        [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]]


# Will calculate cost of a new path removing those already placed
def blocksMoved(player_coords,path):
    blocksMoved = len(path)
    for (r, q) in path:
        if (r,q) in player_coords:
            blocksMoved-=1
    return blocksMoved
