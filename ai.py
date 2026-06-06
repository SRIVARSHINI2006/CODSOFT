print("NEW AI.PY LOADED")
import math
import random


class AIPlayer:

    def __init__(self, game):
        self.game = game
        self.last_reason = ""

    def easy_move(self):
        move = random.choice(self.game.available_moves())
        self.last_reason = "Easy mode selected a random move."
        return move

    def medium_move(self):
        if random.random() < 0.5:
            move = random.choice(self.game.available_moves())
            self.last_reason = "Medium mode selected a random move."
            return move

        move = self.best_move()
        self.last_reason = "Medium mode selected the best strategic move."
        return move

    def hard_move(self):
        move = self.best_move()
        self.last_reason = "Hard mode used Minimax with Alpha-Beta Pruning."
        return move
   
    def best_move(self):

        # Check for winning move
        for move in self.game.available_moves():

            self.game.board[move] = "O"

            if self.game.check_winner("O"):
                self.game.board[move] = " "
                self.last_reason = f"AI chose cell {move + 1} to win the game."
                return move

            self.game.board[move] = " "

        # Check for blocking move
        for move in self.game.available_moves():

            self.game.board[move] = "X"

            if self.game.check_winner("X"):
                self.game.board[move] = " "
                self.last_reason = f"AI chose cell {move + 1} to block your winning move."
                return move

            self.game.board[move] = " "

        best_score = -math.inf
        best_move = None

        for move in self.game.available_moves():

            self.game.board[move] = "O"

            score = self.minimax(
                False,
                -math.inf,
                math.inf
            )

            self.game.board[move] = " "

            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            self.last_reason = (
                f"AI selected cell {best_move + 1} "
                f"to maximize future winning chances."
            )

        return best_move

    def minimax(self, maximizing, alpha, beta):

        if self.game.check_winner("O"):
            return 10

        if self.game.check_winner("X"):
            return -10

        if self.game.is_draw():
            return 0

        if maximizing:

            best_score = -math.inf

            for move in self.game.available_moves():

                self.game.board[move] = "O"

                score = self.minimax(
                    False,
                    alpha,
                    beta
                )

                self.game.board[move] = " "

                best_score = max(
                    best_score,
                    score
                )

                alpha = max(
                    alpha,
                    best_score
                )

                if beta <= alpha:
                    break

            return best_score

        else:

            best_score = math.inf

            for move in self.game.available_moves():

                self.game.board[move] = "X"

                score = self.minimax(
                    True,
                    alpha,
                    beta
                )

                self.game.board[move] = " "

                best_score = min(
                    best_score,
                    score
                )

                beta = min(
                    beta,
                    best_score
                )

                if beta <= alpha:
                    break

            return best_score

    def get_reason(self):
        return self.last_reason