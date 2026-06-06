import json
import os
from datetime import datetime


class Statistics:

    FILE_PATH = "data/stats.json"

    def __init__(self):

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.FILE_PATH):

            self.data = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "games_played": 0,
                "history": []
            }

            self.save()

        else:

            with open(self.FILE_PATH, "r") as file:
                self.data = json.load(file)

    def save(self):

        with open(self.FILE_PATH, "w") as file:
            json.dump(
                self.data,
                file,
                indent=4
            )

    def record_result(self, result):

        self.data["games_played"] += 1

        if result == "Win":
            self.data["wins"] += 1

        elif result == "Loss":
            self.data["losses"] += 1

        elif result == "Draw":
            self.data["draws"] += 1

        self.data["history"].append({
            "result": result,
            "time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        })

        self.save()

    def get_stats(self):
        return self.data

    def get_history(self):
        return self.data["history"]

    def reset_stats(self):

        self.data = {
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "games_played": 0,
            "history": []
        }

        self.save()

    def win_rate(self):

        total = self.data["games_played"]

        if total == 0:
            return 0

        return round(
            (self.data["wins"] / total) * 100,
            2
        )