from random import sample
from time import time


def generate_secret_num():
    """Vytvoří čtyřciferné tajné číslo, kde se žádná cifra neopakuje"""
    while True:
        num = [str(item) for item in sample(range(0, 10), 4)]
        if num[0] != 0:
            return num
        

def validate_guess(guess: str) -> int:
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


def check_guess(guess: str, secret_num: list, counter: dict):
    """Vyhodnotí hádané číslo, zapíše do počítadla"""
    for i, digit in enumerate(guess):
        if digit in secret_num:
            if secret_num[i] == digit:
                counter["bull"] += 1
            else:
                counter["cow"] += 1


def victory_message(global_stats, game_stats: dict, digits: int):
    """Pogratuluje hráči k vítězství a vypíše statistiky dohrané hry
     a srovnání s globálními průměry."""
    print(f"Success!")
    print(f"Guesses: {game_stats['n_guesses']} "
          f"(average: {global_stats['n_guesses'].mean().round(digits)})")
    print(f"Game time: {game_stats['time_to_win']}s "
          f"(average: {global_stats['time_to_win'].mean().round(digits)}s)")


def print_verdict(counter: dict):
    """Projde počítadlo, vytvoří verdikt se správnými množnými čísly,
     vypíše ho."""
    verdict = ""
    for key, value in counter.items():
        verdict += f"| {value} {key} " if value == 1 else f"| {value} {key}s "
    print(verdict)


def play_game(global_stats):
    secret_num = generate_secret_num()

    # inicializuj statistiku probíhajíci hry a zaznamenej čas začátku hry
    game_stats = {"game_id": global_stats["game_id"].max() + 1
                  if not global_stats.empty else 1,
                  "n_guesses": 0,
                  "time_to_win": 0.0}
    start_time = time()

    #
    print("Enter your guess ('*' to quit):")
    print(20 * "-")

    while True:
        guess = input(">>> ")
        err_code = validate_guess(guess)

        # pokud je chybový kód -1, přeruš hru a vrať prázdný soubor statistik
        # pokud je jiná chyba
        if err_code == -1:
            print("-game aborted-")
            return {}
        elif err_code > 0:
            continue

        game_stats["n_guesses"] += 1

        # vyhodnoť tip, vypiš verdikt
        counter = {"bull": 0, "cow": 0}
        check_guess(guess, secret_num, counter)
        print_verdict(counter)

        # pokud hráč uhodl, zapiš čas hraní, vypiš gratulaci a statistiky
        if counter["bull"] == 4:
            game_stats["time_to_win"] = round(time() - start_time, 2)
            victory_message(global_stats, game_stats, 2)

            return game_stats
