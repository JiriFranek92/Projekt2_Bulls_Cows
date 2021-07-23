from random import sample

from stats import Stats, StatsCounter


class BullsAndCows:
    def __init__(self, global_stats):
        self.global_stats = global_stats

        self.game_stats = StatsCounter(self.global_stats)
        self.secret_num = self.__generate_secret_num()
        self.finished = False

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
    def __generate_secret_num():
        """Vytvoří čtyřciferné tajné číslo, kde se žádná cifra neopakuje"""
        while True:
            num = [str(item) for item in sample(range(0, 10), 4)]
            if num[0] != "0":
                return num

    @staticmethod
    def __validate_guess(guess: str) -> int:
        """Zkontroluje validitu hádaného čísla, vrátí chybový kód"""
        if guess == "*":
            return -1
        elif not guess.isnumeric():
            print("Guess must be a number!")
            return 1
        elif not len(guess) == 4:
            print("Guessed number must be 4 digits long!")
            return 2
        elif guess[0] == '0':
            print("Guessed number must not start with a 0!")
            return 3
        elif sum([guess.count(dig) for dig in guess]) != 4:
            print("Each digit must be unique!")
            return 4
        else:
            return 0

    @staticmethod
    def __check_guess(guess: str, secret_num: list, counter: dict):
        """Vyhodnotí hádané číslo, zapíše do počítadla"""
        for i, digit in enumerate(guess):
            if digit in secret_num:
                if secret_num[i] == digit:
                    counter["bull"] += 1
                else:
                    counter["cow"] += 1

    @staticmethod
    def __print_verdict(counter: dict):
        """Projde počítadlo, vytvoří verdikt se správnými množnými čísly,
         vypíše ho."""
        verdict = ""
        for key, value in counter.items():
            verdict += f"| {value} {key} " if value == 1 else f"| {value} {key}s "
        print(verdict)

    def __victory_message(self, digits=2):
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

        print("Enter your guess ('*' to quit):")
        print(20 * "-")
        while True:
            guess = input(">>> ")
            err_code = self.__validate_guess(guess)

            # pokud je chybový kód -1, přeruš hru
            # pokud je jiná chyba, znovu se zeptej na číslo
            if err_code == -1:
                print("-game aborted-")
                print(f"The number was {self.secret_num}")
                self.finished = False
                return
            elif err_code > 0:
                continue
            else:
                self.game_stats.count_guess()

            # vyhodnoť tip, vypiš verdikt
            counter = {"bull": 0, "cow": 0}
            self.__check_guess(guess, self.secret_num, counter)
            self.__print_verdict(counter)

            # pokud hráč uhodl, zapiš čas hraní, vypiš gratulaci a statistiky
            if counter["bull"] == 4:
                self.game_stats.mark_time()
                self.__victory_message()
                self.finished = True
                return
