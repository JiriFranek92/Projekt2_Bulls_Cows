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
        if self.valid:
            self.__manage_invalid_values()

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
        # Vybere správné sloupce z nahrané dtaframe,
        # pokud některý chybí tak ho/je zapíše do chyb
        if set(Stats.df_columns).issubset(self.df.columns):
            self.df = self.df[list(Stats.df_columns)]
        else:
            self.valid = False
            missing_columns = set(Stats.df_columns) - set(self.df.columns)
            self.errors.append(
                f"Stats validation Error!"
                f" Column(s) {missing_columns} are missing!")

    def __manage_invalid_values(self):
        # odstraní data špatného typu a hodnot
        # poznámka: pokud nějaké jsou, pouze se zapíše varování,
        # dataframe jako taková se stále považuje za validní
        self.__remove_wrong_datatypes()
        self.__remove_invalid_values()

    def __remove_wrong_datatypes(self):
        # pokusí se převést data na čísla, hodnoty chybného typu převede na nan
        # pokud jsou řádky s nan, odstraní je a počet zapíše do varování
        # nakonec převede sloupce id a počtu hádání na int
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

    def __remove_invalid_values(self):
        # odstraní řádky, kde některá z hodnot je záporná
        # jejich případný počet zapíše do varování
        valid_rows = ((self.df["n_guesses"] > 0) & (self.df["game_id"] > 0)
                      & (self.df["time_to_win"] > 0))
        invalid_row_count = len(self.df) - sum(valid_rows)
        self.df = self.df[valid_rows]
        self.errors.append(
            f"Warning! Removed {invalid_row_count} rows with invalid values"
            f" from global stats")

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
        self.df.to_csv(self.path, index=False, header=False, mode="a")

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
