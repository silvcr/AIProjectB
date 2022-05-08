import numpy as np
from team_name.a_star import *


max_depth = 2
min_alpha = -1000000
max_beta = 1000000


def alpha_beta(values, current_depth, branching_factor, index, maximizer, alpha, beta):
    if current_depth == max_depth:
        return values[index]
    if maximizer:
        best_score = min_alpha
        for i in range(0, branching_factor):
            score = alpha_beta(values, current_depth + 1, branching_factor,
                               index * branching_factor + i, False, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(best_score, alpha)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = max_beta
        for i in range(0, branching_factor):
            score = alpha_beta(values, current_depth + 1, branching_factor,
                               index * branching_factor + i, True, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
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
    return tile[1]


def evaluation(red, blue, board_dict, board_size):
    red = sorted(red)
    blue = sorted(blue, key=second)
    red_path = a_star(red[0], red[-1], board_dict, board_size)
    blue_path = a_star(blue[0], red[-1], board_dict, board_size)
    if blue_path:
        blue_score = len(blue_path)
        for element in blue_path:
            if element in blue:
                blue_score -= 1
        if blue_score == 0:
            return -100000
    else:
        blue_score = 0
    if red_path:
        red_score = len(red_path)
        for element in red_path:
            if element in red:
                red_score -= 1
        if red_score == 0:
            return 100000
    else:
        red_score = 0
    return red_score - blue_score



class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        # put your code here
        self.current_player = player
        # maintain game state dictionary similar to part A, form move: player
        self.board_dict = {}
        self.board_size = n
        # maintain list of open tiles that can be used
        self.available = []
        for i in range(0, n):
            for j in range(0, n):
                self.available.append((i, j))

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
                    return "PLACE", self.board_size - 3, self.board_size - 1
            else:
                red_move = list(self.board_dict.keys())[0]
                if self.board_size - 2 >= red_move[0] >= 1 and self.board_size - 2 >= red_move[1] >= 1:
                    return "STEAL",
                else:
                    return "PLACE", self.board_size // 2, self.board_size // 2
        else:
            eval_board = self.board_dict
            red = []
            blue = []
            for key in list(eval_board.keys()):
                if eval_board[key] == 'red':
                    red.append(key)
                else:
                    blue.append(key)
            scores = []

            for move in self.available:
                for returning_move in self.available:
                    if move != returning_move:
                        eval_board[move] = self.current_player
                        red.append(move)
                        if self.current_player == 'red':
                            eval_board[returning_move] = 'blue'
                            blue.append(move)
                        scores.append(evaluation(red, blue, eval_board, self.board_size))
            print(scores)
            best_score = alpha_beta(scores, 0, len(self.available) - 2, 0, True, min_alpha, max_beta)
            for i in range(0, len(scores)):
                if scores[i] == best_score:
                    move = self.available[i // (len(self.available) - 1)]
                    return "PLACE", move[0], move[1]
        # if outside opening, generate random move from list of available ones
        random_move = self.available[np.random.randint(0, len(self.available))]

        return "PLACE", random_move[0], random_move[1]

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """

        if action[0] == "STEAL":
            # switch the move played to its reflection, update board dict and available
            move = list(self.board_dict.keys())[0]
            self.board_dict[move[1], move[0]] = 'blue'
            self.available.remove((move[1], move[0]))
            self.available.append(move)
        else:
            # update the moves
            self.board_dict[(action[1], action[2])] = player
            self.available.remove((action[1], action[2]))
            # find neighboring moves and begin check for capture
            neighbors = generate_neighbors((action[1], action[2]))
            opponent_neighbors = []
            for key in neighbors:
                # find neighbors of the opposing color - there is always two of these in a capture
                if key in self.board_dict.keys():
                    if self.board_dict[key] != player:
                        opponent_neighbors.append(key)
            deleted = []
            # check if the remaining opposing cell is of the current player's color
            for tile in opponent_neighbors:
                for opposite_tile in opponent_neighbors:
                    # if the cells are not opposite each other, or the same cell, we check
                    if abs(tile[0] - opposite_tile[0]) % 2 != 0 or abs(tile[1] - opposite_tile[1]) % 2 != 0:
                        # find opposite cell two candidate by computing offsets
                        # this is just main tile + (neighboring tiles - main tiles) simplified
                        candidate_check = (tile[0] + opposite_tile[0] - action[1],
                                           tile[1] + opposite_tile[1] - action[2])
                        # if the cell is of the current player's color, capture has been made - record and update
                        # accordingly
                        if candidate_check in list(self.board_dict.keys()):
                            if self.board_dict[candidate_check] == player:
                                deleted.append(tile)
                                deleted.append(opposite_tile)
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


