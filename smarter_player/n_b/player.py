import numpy as np
from n_b.a_star import *
from n_b.evaluation import *
from copy import *

# restrain depth of search. since we start with a generation of moves,
# this is actually 3-ply
max_depth = 2
min_alpha = -1000000
max_beta = 1000000


def alpha_beta(move, current_depth, maximizer, alpha, beta, last_moves,
               board_dict, board_size, red, blue, killers):
    """Alpha-beta algorithm given the move."""
    # return evaluation for leaf node
    if current_depth == max_depth:
        if maximizer:
            red.append(move)
        else:
            blue.append(move)
        return evaluation(red, blue)
    if maximizer:
        best_score = min_alpha
        available = find_candidates(last_moves[0], board_dict, board_size) + find_candidates(last_moves[1],
                                                                                             board_dict, board_size)
        for move in available:
            if move in killers[current_depth]:
                available.remove(move)
                available.insert(0, move)
        # find children
        available = capture_ordering(available, board_dict, "red")
        for move in available:
            # add and remove move from board_dict. This and red/blue inputs reduce the amount of processing across
            # calls since the structures are similar
            red.append(move)
            board_dict[move] = "red"
            last_moves[0] = move
            score = alpha_beta(move, current_depth + 1, False, alpha, beta, last_moves,
                               board_dict, board_size, red, blue, killers)
            red.remove(move)
            board_dict.pop(move)
            # check for alpha
            if score > best_score:
                best_score = score
            alpha = max(best_score, alpha)
            if beta <= alpha:
                killers[current_depth][1] = killers[current_depth][0]
                killers[current_depth][0] = move
                break
        return best_score
    else:
        best_score = max_beta
        available = find_candidates(last_moves[0], board_dict, board_size) + find_candidates(last_moves[1], board_dict,
                                                                                             board_size)
        for move in available:
            if move in killers[current_depth]:
                available.remove(move)
                available.insert(0, move)
        available = capture_ordering(available, board_dict, "blue")
        for move in available:
            blue.append(move)
            board_dict[move] = "blue"
            last_moves[1] = move
            score = alpha_beta(move, current_depth + 1, True, alpha, beta, last_moves,
                               board_dict, board_size, red, blue, killers)
            blue.remove(move)
            board_dict.pop(move)
            best_score = min(best_score, score)
            beta = min(best_score, beta)
            if beta <= alpha:
                killers[current_depth][1] = killers[current_depth][0]
                killers[current_depth][0] = move
                break
        return best_score


def generate_neighbors(current_position):
    """ Function to generate valid neighbors from a current move"""
    # Generate the six surrounding neighbors to a move
    candidates = [(current_position[0], current_position[1] + 1), (current_position[0], current_position[1] - 1),
                  (current_position[0] + 1, current_position[1]), (current_position[0] - 1, current_position[1]),
                  (current_position[0] - 1, current_position[1] + 1),
                  (current_position[0] + 1, current_position[1] - 1)]
    return candidates


def second(tile):
    """helper to facilitate evaluation"""
    return tile[1]


def evaluation(red, blue):
    """dummy evaluation"""
    red = sorted(red)
    blue = sorted(blue, key=second)
    if len(red) >= 4:
        red_score = -heuristic(red[0], red[1]) - heuristic(red[-1], red[-2])
    else:
        red_score = -heuristic(red[0], red[-1])
    if len(blue) >= 4:
        blue_score = -heuristic(blue[0], blue[1]) - heuristic(blue[-1], blue[-2])
    else:
        blue_score = -heuristic(blue[0], blue[-1])
    return red_score - blue_score


def identify_capture(move, board_dict, player):
    neighbors = generate_neighbors((move[0], move[1]))
    opponent_neighbors = []
    for key in neighbors:
        # find neighbors of the opposing color - there is always two of these in a capture
        if key in board_dict.keys():
            if board_dict[key] != player:
                opponent_neighbors.append(key)
    deleted = []
    # check if the remaining opposing cell is of the current test's color
    for tile in opponent_neighbors:
        for opposite_tile in opponent_neighbors:
            # if the cells are not opposite each other, or the same cell, we check
            if abs(tile[0] - opposite_tile[0]) % 2 != 0 or abs(tile[1] - opposite_tile[1]) % 2 != 0:
                # find opposite cell two candidate by computing offsets
                # this is just main tile + (neighboring tiles - main tiles) simplified
                candidate_check = (tile[0] + opposite_tile[0] - move[0],
                                   tile[1] + opposite_tile[1] - move[1])
                # if the cell is of the current test's color, capture has been made - record and update
                # accordingly
                if candidate_check in list(board_dict.keys()):
                    if board_dict[candidate_check] == player:
                        deleted.append(tile)
                        deleted.append(opposite_tile)
    return deleted


def capture_ordering(candidates, curr_board, player):
    captures = []
    for i in range(0, len(candidates)):
        curr_board[candidates[i]] = player
        if identify_capture(candidates[i], curr_board, player):
            captures.append(candidates[i])
        curr_board.pop(candidates[i])
    if captures:
        for candidate in captures:
            candidates.remove(candidate)
        for candidate in captures:
            candidates.insert(0, candidate)
    return candidates


class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this test.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your test will
        play as Red, or the string "blue" if your test will play
        as Blue.
        """
        # put your code here
        self.current_player = player
        # maintain game state dictionary similar to part A, form move: test
        self.board_dict = {}
        self.board_size = n
        # maintain list of open tiles that can be used
        self.available = []
        for i in range(0, n):
            for j in range(0, n):
                self.available.append((i, j))
        self.last_red_move = ()
        self.last_blue_move = ()

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # put your code here
        # a turn is noted as after both red and blue has moved.
        turn_count = len(self.board_dict.keys()) // 2
        # opening book move, mostly applicable for n >= 8 as to make the game equal (avoid swap)
        # work in progress
        if turn_count == 0:
            if self.current_player == 'red':
                if len(self.board_dict.keys()) == 0:
                    openers = [(self.board_size - 1, self.board_size - 1), (0, 0),
                               (self.board_size - 2, self.board_size - 1), (0, 1),
                               (self.board_size - 1, self.board_size - 2), (1, 0)]
                    move = openers[np.random.randint(0, len(openers))]
                    return "PLACE", move[0], move[1]
            else:
                red_move = list(self.board_dict.keys())[0]
                if self.board_size - 2 >= red_move[0] >= 1 and self.board_size - 2 >= red_move[1] >= 1:
                    return "STEAL",
                else:
                    return "PLACE", self.board_size // 2, self.board_size // 2
        else:
            # middle + endgame
            red = []
            blue = []
            # create red, and blue lists for red and blue moves to facilitate evaluation
            for key in list(self.board_dict.keys()):
                if self.board_dict[key] == 'red':
                    red.append(key)
                else:
                    blue.append(key)
            curr_board = deepcopy(self.board_dict)
            candidates = find_candidates(self.last_red_move,
                                         curr_board, self.board_size) + find_candidates(self.last_blue_move,
                                                                                        curr_board, self.board_size)
            killers = [[(), ()] for i in range(0, max_depth + 1)]
            last_moves = [deepcopy(self.last_red_move), deepcopy(self.last_blue_move)]
            if self.current_player == "red":
                # generate a list of candidate moves. For now, these are only the immediately surrounding moves
                # to the game.
                # candidates = find_candidates(self.last_red_move, self.board_dict, self.board_size)
                # if there are not surrounding moves, get from the list of remaining available moves.
                # if not candidates:
                # run alpha beta on each candidate, and get one where the best score is guaranteed
                best_score = min_alpha
                best_move = candidates[0]
                candidates = capture_ordering(candidates, curr_board, "red")
                for candidate in candidates:
                    curr_board[candidate] = "red"
                    last_moves[0] = candidate
                    score = alpha_beta(candidate, 0, False, min_alpha, max_beta,
                                       last_moves, curr_board, self.board_size, red, blue, killers)
                    curr_board.pop(candidate)
                    if score > best_score:
                        best_score = score
                        best_move = candidate
            else:
                # candidates = find_candidates(self.last_blue_move, self.board_dict, self.board_size)
                # if not candidates:
                best_score = max_beta
                best_move = candidates[0]
                candidates = capture_ordering(candidates, curr_board, "blue")
                for candidate in candidates:
                    curr_board[candidate] = "blue"
                    last_moves[1] = candidate
                    score = alpha_beta(candidate, 0, True, min_alpha, max_beta,
                                       last_moves, curr_board, self.board_size, red, blue, killers)
                    curr_board.pop(candidate)
                    if score < best_score:
                        best_score = score
                        best_move = candidate
            return "PLACE", best_move[0], best_move[1]
            # if outside opening, generate random move from list of available ones

    def turn(self, player, action):
        """
        Called at the end of each test's turn to inform this test of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your test's turn, the action parameter is
        the same as what your test returned from the action method
        above. However, the referee has validated it at this point.
        """

        if action[0] == "STEAL":
            # switch the move played to its reflection, update board dict and available
            move = list(self.board_dict.keys())[0]
            self.board_dict[move[1], move[0]] = 'blue'
            self.available.remove((move[1], move[0]))
            self.available.append(move)
            self.last_blue_move = move[1], move[0]
        else:
            # update the moves
            if player == 'red':
                self.last_red_move = action[1], action[2]
            else:
                self.last_blue_move = action[1], action[2]
            self.board_dict[(action[1], action[2])] = player
            self.available.remove((action[1], action[2]))
            # find neighboring moves and begin check for capture
            # check if the remaining opposing cell is of the current test's color
            deleted = identify_capture((action[1], action[2]), deepcopy(self.board_dict), player)
            if deleted:
                deleted = list(dict.fromkeys(deleted))
                for key in deleted:
                    self.board_dict.pop(key)
                    self.available.append(key)
        if player == 'red':
            self.current_player = 'blue'
        else:
            self.current_player = 'red'

        # put your code here
