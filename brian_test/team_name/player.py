import numpy as np


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
        self.board_dict = {}
        self.board_size = n

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
                return "PLACE", self.board_size - 3, self.board_size - 1
            else:
                red_move = list(self.board_dict.keys())[0]
                if self.board_size - 2 >= red_move[0] >= 1 and self.board_size - 2 >= red_move[1] >= 1:
                    return "STEAL",
                else:
                    return "PLACE", self.board_size // 2, self.board_size // 2
        x = np.random.randint(0, self.board_size)
        y = np.random.randint(0, self.board_size)
        while (x, y) in self.board_dict.keys():
            x = np.random.randint(0, self.board_size)
            y = np.random.randint(0, self.board_size)
        return "PLACE", x, y

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
            self.board_dict[self.board_dict.keys()] = 'blue'
        else:
            self.board_dict[(action[1], action[2])] = player
        if player == 'red':
            self.current_player = 'blue'
        else:
            self.current_player = 'red'
        # put your code here
