"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

Sample Solution

Note: Best efforts have been made to ensure correctness, but as with all
software, there is always the possibility of an unforeseen bug/issue. 
"""

import sys
import json
from search.util import hex_neighbours, print_coordinate
from search.a_star import a_star

def compute_path(n, start_coord, goal_coord, occ_coords, f_h=lambda *_: 0):
    """
    Compute lowest cost path on Cachex board. Internally uses A*.

    Args:
        n: Board size.
        start_coord: Start coordinate (r, q).
        goal_coord: Goal coordinate (r, q).
        occ_coords: List of occupied coordinates.
        f_h: Heuristic function (reverts to UCS if not supplied).

    Returns:
        List of path coordinates, or empty list if no path exists.
    """

    # Using a set will be a lot more efficient than a list here
    occ_coords = set(occ_coords)

    # Returns true iff coord is valid (inside board bounds, not occupied)
    def valid_coord(coord):
        (r, q) = coord
        return 0 <= r < n and 0 <= q < n and (not coord in occ_coords)

    # Returns only valid neighbour coords
    def neighbours(coord):
        return filter(valid_coord, hex_neighbours(coord))

    # Run A* and return path (default empty list if no path)
    return a_star(start_coord, goal_coord, f_h, neighbours) or []

def axial_distance(coord, goal_coord):
    """
    Axial distance heuristic for use in hex-grid based A* search.

    Args:
        coord: Current node coord.
        goal_coord: Goal node coord.

    Returns:
        Cost (or underestimate of cost) from current coord to goal coord.
    """
    (a_r, a_q) = coord
    (b_r, b_q) = goal_coord
    return (abs(a_q - b_q) 
        + abs(a_q + a_r - b_q - b_r)
        + abs(a_r - b_r)) / 2

def main():
    """
    Main entry point for program.
    """
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # We are allowed to assume well-formed JSON input as per the spec...
    n = data["n"]
    start_coord = tuple(data["start"])
    goal_coord = tuple(data["goal"])
    occ_coords = [(r, q) for [_, r, q] in data["board"]]

    # Now do the actual path finding!
    path = compute_path(n, start_coord, goal_coord, occ_coords, axial_distance)

    # Output path cost, then path coords (if any)
    print(len(path))
    for (r, q) in path:
        print_coordinate(r, q)
