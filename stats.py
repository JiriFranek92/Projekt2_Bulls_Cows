from pathlib import Path
from time import time

import pandas as pd


def _get_path(filename):
    # vrátí absolutní cestu souboru (v pracovní složce programu)
    path = Path(__file__).parent.absolute() / filename
    return path


class Stats:
    df_columns = "game_id", "n_guesses", "time_to_win"

    def __init__(self, filename):
        self.path = _get_path(filename)

        self.valid = True
        self.errors = []

        self.df = self.__import_df(self.path)
        if self.df is not None:
            self.__validate_df()
        if self.valid:
            self.__manage_invalid_values()

    def __import_df(self, path):
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            self.valid = False
            self.errors.append(
                f"Stats import failed! File '{path}' does not exist!")
        except pd.errors.ParserError:
            self.valid = False
            self.errors.append(f"Stats import failed! Bad lines in file!")
        else:
            return df

    def __validate_df(self):
        if set(Stats.df_columns).issubset(self.df.columns):
            self.df = self.df[list(Stats.df_columns)]
        else:
            self.valid = False
            missing_columns = set(Stats.df_columns) - set(self.df.columns)
            self.errors.append(
                f"Stats validation Error!"
                f" Column(s) {missing_columns} are missing!")

    def __manage_invalid_values(self):
        for col in self.df.columns:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        row_count = len(self.df)
        self.df = self.df.dropna(axis=0)
        invalid_row_count = row_count - len(self.df)
        self.errors.append(
            f"Warning! Removed {invalid_row_count} rows with wrong data type"
            f" from global stats")

        for col in ['game_id', 'n_guesses']:
            self.df[col] = self.df[col].astype(int)

        valid_rows = ((self.df["n_guesses"] > 0) & (self.df["game_id"] > 0)
                      & (self.df["time_to_win"] > 0))
        invalid_row_count = len(self.df) - sum(valid_rows)
        self.df = self.df[valid_rows]
        self.errors.append(
            f"Warning! Removed {invalid_row_count} rows with invalid values"
            f" from global stats")

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


class StatsCounter:
    """ Obal počítadla pomocí slovníku pro hezčí kód."""
    def __init__(self, global_stats):
        self.global_stats = global_stats
        game_id = 0 if global_stats is None else global_stats.next_id
        self.stats = {"game_id": game_id,
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
        return pd.DataFrame(self.stats, columns=self.global_stats.df.columns,
                            index=[0])

    def __getitem__(self, item):
        return self.stats[item]
