from random import sample

from stats import Stats, StatsCounter


class Error:
    def __init__(self, condition, message):
        self.condition = condition
        self.message = message


class BullsAndCows:
    def __init__(self, global_stats):
        self.global_stats = global_stats

        self.game_stats = StatsCounter(self.global_stats)
        self.secret_num = self._generate_secret_num()
        self.finished = False

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
        if not isinstance(obj, Stats):
            raise TypeError(
                "'global_stats' must be an instance of 'Stats' class!")
        else:
            self._global_stats = obj

    @staticmethod
    def _generate_secret_num():
        """Vytvoří čtyřciferné tajné číslo, kde se žádná cifra neopakuje"""
        while True:
            num = [str(item) for item in sample(range(0, 10), 4)]
            if num[0] != "0":
                return num

    def _validate_guess(self):
        """Zkontroluje validitu hádaného čísla, zaznamená chyby"""
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
        """Vyhodnotí hádané číslo, zapíše do počítadla"""
        self._bc_counter = dict(bull=0, cow=0)

        for i, digit in enumerate(self._guess):
            if digit in self.secret_num:
                if digit == self.secret_num[i]:
                    self._bc_counter["bull"] += 1
                else:
                    self._bc_counter["cow"] += 1

    def _print_verdict(self):
        """Projde počítadlo, vytvoří verdikt se správnými množnými čísly,
         vypíše ho."""
        verdict = ""
        for key, val in self._bc_counter.items():
            verdict += f"| {val} {key} " if val == 1 else f"| {val} {key}s "
        print(verdict)

    def _victory_message(self, digits=2):
        """Pogratuluje hráči k vítězství a vypíše statistiky dohrané hry
         a srovnání s globálními průměry."""
        print(f"Success!")
        print(f"Guesses: {self.game_stats['n_guesses']} "
              f"(average: "
              f"{self.global_stats['n_guesses'].mean().round(digits)})")
        print(f"Game time: {self.game_stats['time_to_win']}s "
              f"(average: "
              f"{self.global_stats['time_to_win'].mean().round(digits)}s)")

    def play(self):
        self.game_stats.start_timer()

        print(f"Enter your guess ('{self._abort_key}' to quit):")
        print(20 * "-")
        while True:
            self._guess = input(">>> ")

            if self._guess == self._abort_key:
                # pokud je zadán kód pro přerušení, přeruš hru
                print("-game aborted-")
                print(f"The number was {self.secret_num}")
                self.finished = False
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

            # vyhodnoť tip, vypiš verdikt
            self._check_guess()
            self._print_verdict()

            # pokud hráč uhodl, zapiš čas hraní, vypiš gratulaci a statistiky
            if self._bc_counter["bull"] == 4:
                self.game_stats.mark_time()
                self._victory_message()
                self.finished = True
                return
