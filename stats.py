"""Modul pro práci se statistikami Bulls and Cows.

Stats pracuje s globálními statistikami.
StatsCounter je počítadlo pro jednotlivé hry.

    Typické použití:

    global_stats = Stats("global_stats.csv")
    game_stats = StatsCounter(global_stats)

    game_stats.start_timer()  # spuštění časovače
    game_stats.count_guess()  # započtení pokusu
    ...
    game_stats.mark_time()  # zaznamenání času

    global_stats.add(game_stats)  # přidání do globálních statistik
"""

from pathlib import Path
from time import time

from numpy import nan
import pandas as pd
from pandera import DataFrameSchema, Column, Check, errors
import pandera.errors


def _get_path(filename):
    # vrátí absolutní cestu souboru (v pracovní složce programu)
    path = Path(__file__).parent.absolute() / filename
    return path


class Stats:
    """Třída pro práci se statistikami minulých her.

    Stará se o import dat z csv souboru a jejich validaci.
    Nové statistiky se přidávají pomocí instance třídy StatsCounter

    Atributy:
        path: Absolutní cesta k csv souboru.
        valid: bool jestli je soubor nebo importovaná data validní
        errors: list stringů chyb a varování
        df: dataframe načtených dat

    Atributy třídy:
        df_columns: správné názvy sloupců dataframe
    """

    df_columns = "game_id", "n_guesses", "time_to_win"

    def __init__(self, filename):
        """Ze zadaného csv souboru načte data a zvaliduje je.

        Argumenty:
            filename:
                Název zdrojového souboru.
                Soubor musí být v pracovní složce programu
        """
        self.path = _get_path(filename)

        self.valid = True
        self.errors = []

        # načti dataframe ze souboru. Pokud se povedlo, validuj dataframe.
        # Pokud je validní, zpracuj chybné hodnoty.
        self.df = self.__import_df(self.path)
        if self.df is not None:
            self.__validate_df()
        # if self.valid:
        #     self.__manage_invalid_values()

    def __import_df(self, path):
        # Importuje dataframe pokud soubor existuje a má správný formát,
        # jinak zapíše chybu.
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
        def get_invalid_row_indices(exc: pandera.errors.SchemaErrors, *cases):
            return exc.failure_cases.loc[exc.failure_cases["check"].isin(cases),
                                         "index"].unique()

        correct_data_types = DataFrameSchema(
            {
                "game_id": Column(int, coerce=True),
                "n_guesses": Column(int, coerce=True),
                "time_to_win": Column(float, coerce=True)
            })

        correct_values = DataFrameSchema(
            {
                "game_id": Column(int, Check.greater_than(0), coerce=True),
                "n_guesses": Column(int, Check.greater_than(0), coerce=True),
                "time_to_win": Column(float, Check.greater_than(0), coerce=True)
            })

        for schema in [correct_data_types, correct_values]:
            try:
                schema.validate(self.df, lazy=True)
            except errors.SchemaErrors as e:
                if "column_in_dataframe" in e.failure_cases.check.values:
                    missing_columns = ",".join(
                        e.failure_cases.loc[e.failure_cases["check"] == "column_in_dataframe", "failure_case"])
                    self.valid = False
                    self.errors.append(
                        f"Stats validation Error!"
                        f" Column(s) '{missing_columns}' are missing!")
                    return
                elif schema == correct_data_types:
                    bad_types = get_invalid_row_indices(e, "coerce_dtype('int64')", "coerce_dtype('float64')")
                    self.errors.append(
                                f"Warning! Removed {len(bad_types)} rows "
                                f"with wrong data type from global stats")
                elif schema == correct_values:
                    bad_values = get_invalid_row_indices(e, "greater_than(0)")
                    self.errors.append(
                        f"Warning! Removed {len(bad_values)} rows "
                        f"with invalid values from global stats")
                self.df = e.data.drop(e.failure_cases["index"])

        self.df = self.df[list(Stats.df_columns)]

    def add(self, new_stats):
        """Přidá data do dataframe a zapíše do csv souboru.

        Argumenty:
            new_stats:
                Instance třídy StatsCounter.
                Nově zazanmenané herní statistiky."""

        if not isinstance(new_stats, StatsCounter):
            raise TypeError("'new_stats' must be an instance of class "
                            "StatsCounter!")
        self.df = self.df.append(new_stats.df, ignore_index=True)
        self.df.to_csv(self.path, index=False, header=False)  # , mode="a"

    def __str__(self):
        """Vypíše cestu k csv souboru a dataframe dat."""
        return (f"Filepath: '{self.path.absolute()}' \n"
                f"{self.df}")

    def __getitem__(self, col):
        """Vrátí sloupec 'col' dataframe."""
        return self.df[col]

    @property
    def empty(self):
        """Bool, jestli je dataframe prázdná."""
        return self.df.empty

    @property
    def next_id(self):
        """Integer, další volné id hry."""
        return self["game_id"].max() + 1 if not self.empty else 1


class StatsCounter:
    """ Obal počítadla pomocí slovníku pro hezčí kód.

    Atributy:
        global_stats: instance třidy Stats statistik minulých her.
        stats: slovník s počítadlem herních statistik.
        start_time: čas začátku hry"""

    def __init__(self, global_stats):
        self.global_stats = global_stats
        game_id = 0 if global_stats is None else global_stats.next_id
        self.stats = {"game_id": game_id,
                      "n_guesses": 0,
                      "time_to_win": 0.0}

        self.start_time = None

    def start_timer(self):
        """Zaznamená aktualní čas."""
        # noinspection PyAttributeOutsideInit
        self.start_time = time()

    def mark_time(self, digits=2):
        """Zazanmená a zapopočítá čas hry."""
        if self.start_time is not None:
            self.stats["time_to_win"] = round(time() - self.start_time, digits)
        else:
            self.stats["time_to_win"] = nan

    def count_guess(self):
        """Započítá hádání."""
        self.stats["n_guesses"] += 1

    @property
    def df(self):
        """Počítadlo jako dataframe."""
        return pd.DataFrame(self.stats, columns=self.global_stats.df.columns,
                            index=[0])

    def __getitem__(self, key):
        """Vrátí hodnotu vnitřího slovníku podle klíče."""
        return self.stats[key]
