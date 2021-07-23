from pathlib import Path
from time import time

import pandas as pd
from tabulate import tabulate

from ascii_chart import Histogram


class Stats:
    df_template = pd.DataFrame({"game_id": [],
                                "n_guesses": [],
                                "time_to_win": []})

    def __init__(self, filename):
        self.path = self.__get_path(filename)
        self.df = pd.read_csv(self.path)
        self.__validate_df()

    @staticmethod
    def __get_path(filename):
        # pokud soubor nemá relativní cestu, tak ji vytvoř
        path = Path(filename)
        if not path.is_absolute():
            Path(__file__).parent.absolute() / filename
        return path

    @staticmethod
    def __import(self, path):
        # TODO: co dělat pokud soubor neexistuje
        return pd.read_csv(path)

    def __validate_df(self):
        # TODO: validace importovaných statistik
        pass

    def add(self, new_stats):
        if not isinstance(new_stats, StatsCounter):
            raise TypeError("'new_stats' must be an instance of class "
                            "StatsCounter!")
        self.df = self.df.append(new_stats.df, ignore_index=True)
        self.df.to_csv(self.path, index=False, header=False, mode="a")

    def __str__(self):
        return f"Filepath: '{self.path.absolute()}' \n {self.df}"

    def __getitem__(self, item):
        return self.df[item]

    @property
    def empty(self):
        """ Vrátí jestli je dataframe prázdná."""
        return self.df.empty

    @property
    def next_id(self):
        """ Vrátí první volné id hry."""
        return self["game_id"].max() + 1 if not self.empty else 1

    @property
    def n_guesses_chart(self):
        chart = Histogram(data=self.df, x="n_guesses", precision=0)
        chart.sort_data(sort_by="index")
        chart.format(labels=["GUESSES", "GAMES"])
        return chart

    @property
    def time_to_win_chart(self):
        chart = Histogram(data=self.df, x="time_to_win", precision=-1)
        chart.sort_data(sort_by="index")
        chart.format(labels=["TIME TO WIN(s)", "GAMES"])
        return chart

    @property
    def raw_data(self):
        return tabulate(self.df, showindex=False, tablefmt="psql",
                        headers=("Game \nnumber", "Number of \nGuesses",
                                 "Time to \nwin"))


class StatsCounter:
    """ Obal počítadla pomocí slovníku pro hezčí kód."""
    def __init__(self, global_stats):
        self.global_stats = global_stats
        self.stats = {"game_id": global_stats.next_id,
                      "n_guesses": 0,
                      "time_to_win": 0.0}

    def start_timer(self):
        # noinspection PyAttributeOutsideInit
        self.start_time = time()

    def mark_time(self, digits=2):
        self.stats["time_to_win"] = round(time() - self.start_time, digits)

    def count_guess(self):
        self.stats["n_guesses"] += 1

    @property
    def df(self):
        return pd.DataFrame(self.stats, columns=self.global_stats.columns,
                            index=[0])

    def __getitem__(self, item):
        return self.stats[item]
