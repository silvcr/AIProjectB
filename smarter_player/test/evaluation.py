import numpy as np


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



# Heuristic using manhattan method changed for hex graphs *** taken from text book must ref **
def heuristic(start, goal):
    """ Admissible heuristic for current move"""

    dx = start[0] - goal[0]
    dy = start[1] - goal[1]

    if np.sign(dx) == np.sign(dy):
        abs(dx + dy)
    else:
        max(abs(dx), abs(dy))
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])



# A_star returns shortest distance between two given points ** been adjusted from Proj A so you can overlap with
# same colour

def a_star(start, goal, board_dict, board_size,player):
    """ A* algorithm"""

    # Newly added distance is how many moves are needed to reach end goal from the start goal
    distance = 0

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

                # Changed from not in list to not in list OR in list and is test colour

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
            distance+=1
            previous_node = closed_dict[previous_node][-1]
        print(len(path) + 1)
        for i in range(-1, -len(path) - 1, -1):
            print(path[i])
        print(goal)
    else:
        print("No solution? (was 0) ")

    print(f"minimum moves from {start} to {goal } is ")
    print(distance)

    return distance

""" Finds how many blocks test is from winning """
# The use of  A star in this function is used assuming
# 1. You can include already placed blocks (same colour) (we need to fix this part)
# 2. Calculates how many moves is needed from start to goal (already done with "distance")
# To do: A* doesn't consider already placed blocks --> We need to implement this in this function through using A* to compare

def findDist(board_dict,n,player):
    distance = 0
    wallDist = n
    minDist = n

    # All commented because I need to fix A* to include already placed blocks (of test colour)

    # Finds tile closest to a wall

    #for element in board_dict:
        #if (board_dict[element] == test):
            # if placed tile has closer distance to wall than other  , replace
            #if (a_star(element,closestWall,board_dict,n,test) < wallDist:
            # minDist = a_star(element,board_dict,n,test)
            # minTile = element

    # Finding winning path * I actually have to fix this but for now A* will manage it and calc winning test

    #for element in board_dict:
        #if (board_dict[element] == test):
            #a_star(minTile, element, board_dict,n) < minDist
            # minDist = a_star(minTile, element, board_dict,n)

    return distance

""" Gives list of tiles on each end not blocked for given test colour  """

# Might have to do two lists for each side but should'nt need to
# Is used to find goal point for the chain

def wall(board_dict,n,player):

    wall = {}
    i = 0
    # Adding wall values for  test
    if player == "b":
        while i in range(n):
            # if wall is not taken by red then add to wall dictionary
            if board_dict[(0,i)] != "r":
                wall[(0,i)] = "b"

            if board_dict[(n,i)] != "r":
                wall[(n,i)] = "b"
            i+=1

    # Adding wall values for red test
    else:
        while i in range(n):
            # if wall is not taken by blue then add to wall dictionary
            if board_dict[(i, 0)] != "b":
                wall[(i, 0)] = "b"

            if board_dict[(i, n)] != "b":
                wall[(i, n)] = "b"
            i += 1
    return wall

""" Gives final evaluation of winning team """

def winningTeam(board_dict,n,currPlayer):

    if currPlayer == "b":
        opponent = "r"
    else:
        opponent = "b"

    # Find distance currplayer is from winning
    currDist = findDist(board_dict,n,currPlayer)
    # Find distance opponent is from winning
    opponentDist = findDist(board_dict,n,opponent)

    # Returns difference of how far each test is from winning and returns winning team
    score = currDist - opponentDist

    if (score < 0):
        print(f"Player {currPlayer} is winning with {currDist} moves away\n")
        return currPlayer

    elif (score > 0):
        print(f"Player {opponent} is winning with {opponentDist} moves away\n")
        return opponent

    else:
        print("Draw\n")
        return "draw"