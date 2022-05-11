import numpy as np
from n_b.a_star import *
from n_b.evaluation import *
from copy import *

# initialize alpha and beta values
min_alpha = -1000000
max_beta = 1000000


def alpha_beta(move, current_depth, max_depth, maximizer, alpha, beta, last_moves,
               board_dict, board_size, red, blue, killers):
    """Alpha-beta algorithm given the move. Given our evaluation function, the
    algorithm assumes the maximizing player is always red, and the minimizing player is always blue"""
    # return evaluation for leaf node
    if current_depth == max_depth:
        if maximizer:
            red.append(move)
            # if the move is a capture, we must record it to evaluate
            deleted = list(set(identify_capture(move, board_dict, "red")))
            if deleted:
                for element in deleted:
                    if element in blue:
                        blue.remove(element)
            # evaluation
            score = winningTeam(board_size, "red", red, blue)
            # restoring inputs to their original form
            if deleted:
                for element in deleted:
                    blue.append(element)
            red.pop(-1)
        else:
            # repeat same process for blue moves.
            blue.append(move)
            deleted = list(set(identify_capture(move, board_dict, "blue")))
            if deleted:
                for element in deleted:
                    if element in red:
                        red.remove(element)
            score = winningTeam(board_size, "blue", red, blue)
            if deleted:
                for element in deleted:
                    red.append(element)
            blue.pop(-1)
        return score
    # maximizer (red) call
    if maximizer:
        # find candidates. this is all surrounding nodes to the last two moves played along with some extra
        # nodes outer
        best_score = min_alpha
        available = find_candidates(last_moves[0], board_dict, board_size) + find_candidates(last_moves[1],
                                                                                             board_dict, board_size)
        # identify killer move for ordering
        for move in available:
            if move in killers[current_depth]:
                available.remove(move)
                available.insert(0, move)
        # identify capture move for ordering
        available = capture_ordering(available, board_dict, "red")
        for move in available:
            # add and remove move from board_dict. This and red/blue inputs reduce the amount of processing across
            # calls since the structures are similar
            red.append(move)
            board_dict[move] = "red"
            last_moves[0] = move
            # manipulate data structures for alpha_beta recursive call
            deleted = list(set(identify_capture(move, board_dict, "red")))
            if deleted:
                for element in deleted:
                    if element in blue:
                        blue.remove(element)
            # alpha_beta recursive call in child depth
            score = alpha_beta(move, current_depth + 1, max_depth, False, alpha, beta, last_moves,
                               board_dict, board_size, red, blue, killers)
            red.pop(-1)
            if deleted:
                for element in deleted:
                    blue.append(element)
            board_dict.pop(move)
            # check for alpha
            # find alpha
            if score > best_score:
                best_score = score
            alpha = max(best_score, alpha)
            # if cut-off is produced, we note the move causing it as a killer move
            if beta <= alpha:
                killers[current_depth][1] = killers[current_depth][0]
                killers[current_depth][0] = move
                break
        return best_score
    else:
        # repeat the process for minimizing
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
            deleted = list(set(identify_capture(move, board_dict, "blue")))
            if deleted:
                for element in deleted:
                    if element in red:
                        red.remove(element)
            score = alpha_beta(move, current_depth + 1, max_depth, True, alpha, beta, last_moves,
                               board_dict, board_size, red, blue, killers)
            if deleted:
                for element in deleted:
                    red.append(element)
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


def identify_capture(move, board_dict, player):
    """given the last move played, identify if it was a capture, and if it was a capture. If so
    report all the captured tiles"""
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
    """Order a list of candidate moves by moving all captures to the front"""
    captures = []
    # manually check for captures
    for i in range(0, len(candidates)):
        curr_board[candidates[i]] = player
        if identify_capture(candidates[i], curr_board, player):
            captures.append(candidates[i])
        curr_board.pop(candidates[i])
    # if found, move them
    if captures:
        for candidate in captures:
            candidates.remove(candidate)
        for candidate in captures:
            candidates.insert(0, candidate)
    return candidates


class Player:
    def __init__(self, player, n):
        """Initialization"""
        self.current_player = player
        # maintain game state dictionary similar to part A, form move: test
        self.board_dict = {}
        self.board_size = n
        # maintain list of open tiles that can be used
        self.available = []
        # maintain all available moves
        for i in range(0, n):
            for j in range(0, n):
                self.available.append((i, j))
        # maintain separate lists of moves
        self.last_red_move = ()
        self.last_blue_move = ()
        self.red = []
        self.blue = []
        # the max_depth of the search is reduced if the board is too large.
        if n < 10:
            self.max_depth = 2
        else:
            self.max_depth = 1

    def action(self):
        """Action call"""
        # a turn is noted as after both red and blue has moved.
        turn_count = len(self.board_dict.keys()) // 2
        # opening book move
        if turn_count == 0:
            if self.current_player == 'red':
                # if the board is sufficiently large, we play book moves on the edge of the board
                # for an equal game
                if len(self.board_dict.keys()) == 0 and self.board_size > 5:
                    openers = [(self.board_size - 3, self.board_size - 1),
                               (self.board_size - 2, self.board_size - 2),
                               (self.board_size - 1, self.board_size - 3)]
                    move = openers[np.random.randint(0, len(openers))]
                    return "PLACE", move[0], move[1]
                else:
                    # but opening theory falls apart for small board, so we play in the
                    # middle of the edge column
                    return "PLACE", self.board_size // 2, self.board_size - 1
            else:
                # steal moves if they are central, and play our own central move otherwise.
                red_move = list(self.board_dict.keys())[0]
                if self.board_size - 2 >= red_move[0] >= 1 and self.board_size - 2 >= red_move[1] >= 1:
                    return "STEAL",
                else:
                    return "PLACE", self.board_size // 2, self.board_size // 2
        else:
            # middle + endgame
            red = deepcopy(self.red)
            blue = deepcopy(self.blue)
            curr_board = deepcopy(self.board_dict)
            # begin generating candidates
            candidates = find_candidates(self.last_red_move,
                                         curr_board, self.board_size) + find_candidates(self.last_blue_move,
                                                                                        curr_board, self.board_size)
            # fail-safe in case move generation did not work.
            if not candidates:
                move = self.available[np.random.randint(0, len(self.available))]
                return "PLACE", move[0], move[1]
            # initialize last moves played and killer tracker
            killers = [[(), ()] for i in range(self.max_depth + 1)]
            last_moves = [deepcopy(self.last_red_move), deepcopy(self.last_blue_move)]
            # play a greedy search if the board is not third-full. The algorithm
            # struggles to perform when a board is not well filled, but speeds up when there is filling.
            if len(self.board_dict) * 3 < (self.board_size ** 2):
                best_move = self.available[0]
                if self.current_player == "red":
                    # simply searches all moves for the one with the best evaluation score.
                    best_score = min_alpha
                    for move in self.available:
                        red.append(move)
                        deleted = list(set(identify_capture(move, curr_board, "red")))
                        if deleted:
                            for element in deleted:
                                blue.remove(element)
                        score = winningTeam(self.board_size, "red", red, blue)
                        if deleted:
                            for element in deleted:
                                blue.append(element)
                        if score > best_score:
                            best_score = score
                            best_move = move
                        red.pop(-1)
                else:
                    # same repetition for blue
                    best_score = max_beta
                    for move in self.available:
                        blue.append(move)
                        deleted = list(set(identify_capture(move, curr_board, "blue")))
                        if deleted:
                            for element in deleted:
                                red.remove(element)
                        score = winningTeam(self.board_size, "red", red, blue)
                        if deleted:
                            for element in deleted:
                                red.append(element)
                        if score < best_score:
                            best_score = score
                            best_move = move
                        blue.pop(-1)
                return "PLACE", best_move[0], best_move[1]
            else:
                if self.current_player == "red":
                    # generate a list of candidate moves. For now, these are only the immediately surrounding moves
                    # to the game.
                    # candidates = find_candidates(self.last_red_move, self.board_dict, self.board_size)
                    # if there are not surrounding moves, get from the list of remaining available moves.
                    # if not candidates:
                    # run alpha beta on each candidate, and get one where the best score is guaranteed
                    best_score = min_alpha
                    best_move = candidates[0]
                    # maintain capture ordering
                    candidates = capture_ordering(candidates, curr_board, "red")
                    for candidate in candidates:
                        # update data structures
                        curr_board[candidate] = "red"
                        last_moves[0] = candidate
                        red.append(candidate)
                        deleted = list(set(identify_capture(candidate, curr_board, "red")))
                        if deleted:
                            for element in deleted:
                                blue.remove(element)
                        # run alpha beta on each node
                        score = alpha_beta(candidate, 0, self.max_depth, False, min_alpha, max_beta,
                                           last_moves, curr_board, self.board_size, red, blue, killers)
                        curr_board.pop(candidate)
                        if deleted:
                            for element in deleted:
                                blue.append(element)
                        red.pop(-1)
                        if score > best_score:
                            if candidate in self.available:
                                best_score = score
                                best_move = candidate
                else:
                    # repeat process for blue
                    best_score = max_beta
                    best_move = candidates[0]
                    candidates = capture_ordering(candidates, curr_board, "blue")
                    for candidate in candidates:
                        curr_board[candidate] = "blue"
                        last_moves[1] = candidate
                        blue.append(candidate)
                        deleted = list(set(identify_capture(candidate, curr_board, "blue")))
                        if deleted:
                            for element in deleted:
                                if element in red:
                                    red.remove(element)
                        score = alpha_beta(candidate, 0, self.max_depth, True, min_alpha, max_beta,
                                           last_moves, curr_board, self.board_size, red, blue, killers)
                        if deleted:
                            for element in deleted:
                                red.append(element)
                        blue.pop(-1)
                        curr_board.pop(candidate)
                        if score < best_score:
                            if candidate in self.available:
                                best_score = score
                                best_move = candidate
                return "PLACE", best_move[0], best_move[1]

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
        # update for steals
        if action[0] == "STEAL":
            # switch the move played to its reflection, update board dict and available
            move = list(self.board_dict.keys())[0]
            self.board_dict[move[1], move[0]] = 'blue'
            self.available.remove((move[1], move[0]))
            self.available.append(move)
            self.last_blue_move = move[1], move[0]
            self.blue.append((move[1], move[0]))
        else:
            # update the moves
            if player == 'red':
                self.last_red_move = action[1], action[2]
                self.red.append((action[1], action[2]))
            else:
                self.last_blue_move = action[1], action[2]
                self.blue.append((action[1], action[2]))
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
                    if key in self.red:
                        self.red.remove(key)
                    else:
                        self.blue.remove(key)
        if player == 'red':
            self.current_player = 'blue'
        else:
            self.current_player = 'red'
