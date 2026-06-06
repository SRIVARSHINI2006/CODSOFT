import tkinter as tk
from tkinter import ttk, messagebox

from game_logic import GameLogic
from ai import AIPlayer
from statistics import Statistics
from themes import ThemeManager


class TicTacToeApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced AI Tic Tac Toe")
        self.root.geometry("500x650")

        self.game = GameLogic()
        self.ai = AIPlayer(self.game)
        self.stats = Statistics()
        self.theme_manager = ThemeManager()

        self.difficulty = tk.StringVar(value="Hard")

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="AI Tic Tac Toe",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()

        tk.Label(
            difficulty_frame,
            text="Difficulty:"
        ).pack(side=tk.LEFT)

        ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty,
            values=["Easy", "Medium", "Hard"],
            width=10,
            state="readonly"
        ).pack(side=tk.LEFT)

        self.theme_btn = tk.Button(
            self.root,
            text="Switch Theme",
            command=self.switch_theme
        )
        self.theme_btn.pack(pady=5)

        self.buttons = []

        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=15)

        for i in range(9):

            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24),
                width=4,
                height=2,
                command=lambda i=i: self.player_move(i)
            )

            btn.grid(
                row=i // 3,
                column=i % 3,
                padx=2,
                pady=2
            )

            self.buttons.append(btn)

        self.reason_label = tk.Label(
            self.root,
            text="AI explanation will appear here.",
            wraplength=400
        )
        self.reason_label.pack(pady=10)

        self.stats_label = tk.Label(
            self.root,
            text=""
        )
        self.stats_label.pack()

        self.update_stats_display()

        tk.Button(
            self.root,
            text="New Game",
            command=self.reset_game
        ).pack(pady=5)

    def player_move(self, pos):

        if not self.game.make_move(pos, "X"):
            return

        self.buttons[pos]["text"] = "X"

        if self.check_game_end():
            return

        self.root.after(300, self.ai_move)

    def ai_move(self):

        level = self.difficulty.get()

        if level == "Easy":
            move = self.ai.easy_move()

        elif level == "Medium":
            move = self.ai.medium_move()

        else:
            move = self.ai.hard_move()

        self.game.make_move(move, "O")

        self.buttons[move]["text"] = "O"

        self.reason_label.config(
            text=self.ai.get_reason()
        )

        self.check_game_end()

    def check_game_end(self):

        if self.game.check_winner("X"):

            self.stats.record_result("Win")

            self.update_stats_display()

            messagebox.showinfo(
                "Result",
                "You Win!"
            )

            self.reset_game()

            return True

        if self.game.check_winner("O"):

            self.stats.record_result("Loss")

            self.update_stats_display()

            messagebox.showinfo(
                "Result",
                "AI Wins!"
            )

            self.reset_game()

            return True

        if self.game.is_draw():

            self.stats.record_result("Draw")

            self.update_stats_display()

            messagebox.showinfo(
                "Result",
                "Draw!"
            )

            self.reset_game()

            return True

        return False

    def update_stats_display(self):

        s = self.stats.get_stats()

        self.stats_label.config(
            text=f"Wins: {s['wins']}   "
                 f"Losses: {s['losses']}   "
                 f"Draws: {s['draws']}"
        )

    def reset_game(self):

        self.game.reset()

        for btn in self.buttons:
            btn.config(text="")

        self.reason_label.config(
            text="AI explanation will appear here."
        )

    def switch_theme(self):

        theme = self.theme_manager.toggle_theme()

        self.root.configure(bg=theme["bg"])

    def apply_theme(self):

        theme = self.theme_manager.get_theme()

        self.root.configure(bg=theme["bg"])


root = tk.Tk()

app = TicTacToeApp(root)

root.mainloop()
