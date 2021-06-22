from random import sample
from time import time


def play_game(global_stats):
    # generuj tajné číslo
    while True:
        secret_num = [str(item) for item in sample(range(0, 10), 4)]
        if secret_num[0] != '0':
            break

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
        counter = {"bull": 0, "cow": 0}

        guess = input(">>> ")

        # zkontroluj vstupní hodnoty
        if guess == "*":
            print("-game aborted-")
            return {}
        elif not guess.isnumeric():
            print("Guess must be a number!")
            continue
        elif not len(guess) == 4:
            print("Guessed number must be 4 digits long!")
            continue
        elif guess[0] == '0':
            print("Guessed number must not start with a 0!")
            continue
        elif sum([guess.count(dig) for dig in guess]) != 4:
            print("Each digit must be unique!")
            continue

        game_stats["n_guesses"] += 1

        # vyhodnoť tip, zapiš do počítadla
        for i, digit in enumerate(guess):
            if digit in secret_num:
                if secret_num[i] == digit:
                    counter["bull"] += 1
                else:
                    counter["cow"] += 1

        # vypiš verdikt
        verdict = ""
        for key, value in counter.items():
            verdict += f"| {value} {key} " \
                if value == 1 else f"| {value} {key}s "
        print(verdict)

        if counter["bull"] == 4:
            game_stats["time_to_win"] = round(time() - start_time, 2)
            print(f"Great Success!")
            print(f"Guesses: {game_stats['n_guesses']} "
                  f"(average: {global_stats['n_guesses'].mean().round(2)})")
            print(f"Game time: {game_stats['time_to_win']}s "
                  f"(average: {global_stats['time_to_win'].mean().round(2)}s)")

            return game_stats
