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
                  (current_position[0] + 1, current_position[1] - 1),
                  (current_postition[0] + )]
    legal_candidates = []
    # Filter out non-valid neighbors
    for move in candidates:
        if valid_candidate(move, board_dict=board_dict, board_size=board_size):
            legal_candidates.append(move)
    return legal_candidates


# heuristic using manhattan method
def heuristic(start, goal):
    """ Admissible heuristic for current move"""
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def a_star(start, goal, board_dict, board_size):
    """ A* algorithm"""
    # Empty queues
    open_dict = {}
    closed_dict = {}
    # Initiate the starting node
    open_dict[start] = (heuristic(start, goal), 0, 'Start')

    found = False
    # While queue is non-empty
    while open_dict:
        # Sort the queue, O(n log n + n + n) = O(n log n)
        ordered_keys = sorted(open_dict, key=open_dict.__getitem__)
        candidate_key = ordered_keys[0]
        candidate = open_dict.pop(candidate_key)
        # Terminate search if we find the goal
        if candidate_key == goal:
            closed_dict[candidate_key] = candidate
            found = True
            break
        else:
            # Evaluate a move's neighbors. If it has a better f_score through this path, we reallocate
            # the scores and predecessors to the current node
            for move in find_candidates(candidate_key, board_dict, board_size):
                if move not in list(closed_dict.keys()):
                    h_score = heuristic(move, goal)
                    g_score = candidate[1] + 1
                    if move not in list(open_dict.keys()):
                        open_dict[move] = (h_score + g_score, g_score, candidate_key)
                    elif (h_score + g_score) < open_dict[move][0]:
                        open_dict[move] = (h_score + g_score, g_score, candidate_key)
            # Move the node to the closed queue
            closed_dict[candidate_key] = candidate
    # Trace the goal node through the closed queue if the goal was found
    if found:
        previous_node = closed_dict[goal][-1]
        path = []
        while previous_node != 'Start':
            path.append(previous_node)
            previous_node = closed_dict[previous_node][-1]
        return path
    else:
        return 0
