"""Modul pro hru Bulls and Cows.

Vyžaduje modul 'stats'. Obsahuje jedinou třídu BullsAndCows.
Samostatně spustitelný (pouze bez použítí globálních statistik).

    Typické použití:

    game = BullsAndCows(global_stats)  # inicializace s glob. statistikami
    game.play()

    # zápis do globáních statistik
    if game.won:
        global_stats.add(game.game_stats)
"""


from random import sample

from stats import Stats, StatsCounter


class Error:
    def __init__(self, condition, message):
        self.condition = condition
        self.message = message


def _generate_secret_num():
    # Vytvoří čtyřciferné tajné číslo, kde se žádná cifra neopakuje
    while True:
        num = [str(item) for item in sample(range(0, 10), 4)]
        if num[0] != "0":
            return num


class BullsAndCows:
    """Hra Bulls and Cows

    Hráč hádá tajné čtyřciferné číslo, kde se žádná číslice neopakuje.
    Pokud hráč uhádne cifru je to 'Cow', pokud uhádne cifru i umístění je to
    'Bull'. Cílem je tedy měnit cifry a jejich umístění v hádaném čísle,
    dokud hráč neuhádne číslo celé.

    Hra si uchovává počet hádání a při výhře čas k uhodnutí. Tyto statistiky
    jsou vypsány po dohrání a pokud je k dispozici soubor se
    statistikami minulých her i globální průmery.

    Atributy:
        global_stats: instance třídy Stats se statistikami minulých her
        game_stats:
            instance třídy StatsCounter pro zaznamenávání herních statistik
        secret_num: list, náhodně vygenerované tajné číslo
        won: bool, jestli byla hra úspěšně dohrána
    """
    def __init__(self, global_stats=None):
        self.global_stats = global_stats

        self.game_stats = StatsCounter(self.global_stats)
        self.secret_num = _generate_secret_num()
        self.won = False

        # interní atributy
        self._guess = None
        self._found_errors = []
        self._abort_key = "*"
        self._bc_counter = dict(bull=0, cow=0)

    @property
    def global_stats(self):
        return self._global_stats

    @global_stats.setter
    def global_stats(self, obj):
        if obj is not None and not isinstance(obj, Stats):
            raise TypeError(
                "'global_stats' must be an instance of 'Stats' class!")
        else:
            self._global_stats = obj

    def _validate_guess(self):
        # Zkontroluje validitu hádaného čísla, zaznamená chyby
        errors = [Error(not self._guess.isnumeric(),
                        "Guess must be a number!"),
                  Error(len(self._guess) != 4,
                        "Guessed number must be 4 digits long!"),
                  Error(self._guess[0] == '0',
                        "Guessed number must not start with a 0!"),
                  Error(len(self._guess) != len(set(self._guess)),
                        "Each digit must be unique!")]

        self._found_errors = []

        for error in errors:
            if error.condition is True:
                self._found_errors.append(error)

    def _check_guess(self):
        # Vyhodnotí hádané číslo a počet 'Bulls' a 'Cows' zapíše do počítadla
        self._bc_counter = dict(bull=0, cow=0)

        for i, digit in enumerate(self._guess):
            if digit in self.secret_num:
                if digit == self.secret_num[i]:
                    self._bc_counter["bull"] += 1
                else:
                    self._bc_counter["cow"] += 1

    def _print_verdict(self):
        # Projde počítadlo, vytvoří verdikt se správnými množnými čísly,
        # vypíše ho.
        verdict = ""
        for key, val in self._bc_counter.items():
            verdict += f"| {val} {key} " if val == 1 else f"| {val} {key}s "
        print(verdict)

    def _victory_message(self, digits=2):
        # Pogratuluje hráči k vítězství a vypíše statistiky dohrané hry
        # a srovnání s globálními průměry (pokud jsou k dispozici).
        str_guesses = f"Guesses: {self.game_stats['n_guesses']}"
        str_mean_guesses = "" if self.global_stats is None else (
            f" (average: "
            f"{self.global_stats['n_guesses'].mean().round(digits)})")

        str_time = f"Game time: {self.game_stats['time_to_win']}s "
        str_mean_time = "" if self.global_stats is None else (
            f" (average: "
            f"{self.global_stats['time_to_win'].mean().round(digits)}s)")

        print(f"Success!")
        print(str_guesses + str_mean_guesses)
        print(str_time + str_mean_time)

    def play(self):
        """Spustí hru Bulls and Cows

        Po skončení jsou v atributu 'game_stats' uloženy herní statistiky a
        v atributu 'won' jestli byla hra úspěšně dohraná."""
        self.game_stats.start_timer()

        print(f"Enter your guess ('{self._abort_key}' to quit):")
        print(20 * "-")
        while True:
            self._guess = input(">>> ")

            if self._guess == self._abort_key:
                # pokud je zadán kód pro přerušení, přeruš hru
                print("-game aborted-")
                print(f"The number was {''.join(self.secret_num)}")
                self.won = False
                return
            else:
                # jinak zkontroluj validitu
                self._validate_guess()
                if self._found_errors:
                    # pokud jsou nalezeny chyby, vypiš je a pokračuj na další
                    # iteraci
                    print("\n".join(
                        [err.message for err in self._found_errors]))
                    continue
                else:
                    # jinak připočítej hádání
                    self.game_stats.count_guess()

            self._check_guess()
            self._print_verdict()

            if self._bc_counter["bull"] == 4:
                self.game_stats.mark_time()
                self._victory_message()
                self.won = True
                return


def main():
    game = BullsAndCows()
    game.play()


if __name__ == "__main__":
    main()
