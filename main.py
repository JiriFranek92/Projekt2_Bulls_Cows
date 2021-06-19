from random import sample
from time import time
import pandas as pd

# načti herní statistiky do dataframe
game_stats = pd.read_csv("game_stats.csv")

# generuj tajné číslo
while True:
    secret_num = [str(item) for item in sample(range(0, 10), 4)]
    if secret_num[0] != '0':
        break

# inicializuj statistiku probíhajíci hry a zaznamenej čas začátku hry
# current_stats = pd.Series({"game_id": 0, "n_guesses": 0, "time_to_win": 0.0})
current_stats = {"game_id": game_stats["game_id"].max() + 1
                 if not game_stats.empty else 1,
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
        break
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

    current_stats["n_guesses"] += 1

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
        verdict += f"| {value} {key} " if value == 1 else f"| {value} {key}s "
    print(verdict)

    if counter["bull"] == 4:
        current_stats["time_to_win"] = round(time() - start_time, 2)
        print(f"Great Success!")
        print(f"Guesses: {current_stats['n_guesses']} "
              f"( average: {game_stats['n_guesses'].mean().round(2)} )")
        print(f"Game time: {current_stats['time_to_win']}s "
              f"( average: {game_stats['time_to_win'].mean().round(2)}s )")

        # přidej statistiky poslední hry do DataFrame, ulož do csv
        # poznámka: Pokud se přidá slovník přímo,
        # Pandas převede všechny sloupce int na float,
        # převedením slovníku na Dataframe se tomu zabrání.
        # Není to pěkné, ale funguje to...
        game_stats = game_stats.append(pd.DataFrame(
            current_stats, columns=game_stats.columns, index=[0]),
            ignore_index=True)
        game_stats.to_csv("game_stats.csv", index=False)
        break
