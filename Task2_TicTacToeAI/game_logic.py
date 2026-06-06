class GameLogic:

    WIN_PATTERNS = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [" "] * 9

    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False

    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == " "]

    def check_winner(self, player):
        for pattern in self.WIN_PATTERNS:
            if all(self.board[i] == player for i in pattern):
                return True
        return False

    def is_draw(self):
        return " " not in self.board

    def get_board(self):
        return self.board
