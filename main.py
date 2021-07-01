from pathlib import Path

import pandas as pd

from ascii_chart import ascii_chart
from game import play_game


def add_game_stats(game_stats, glob_stats):
    return glob_stats.append(pd.DataFrame(
        game_stats, columns=global_stats.columns, index=[0]),
        ignore_index=True)


def n_guesses_chart(dataframe):
    return ascii_chart(data=dataframe, x="n_guesses", chart_type="hist",
                       precision=0, labels=["GUESSES", "GAMES"],
                       sort_by="index")


def time_to_win_chart(dataframe):
    return ascii_chart(data=dataframe, x="time_to_win", chart_type="hist",
                       precision=-1, labels=["TIME TO WIN(s)", "GAMES"],
                       sort_by="index")

# ---------- STRUKTURA PROGRAMU ----------
# MAIN MENU
#  |- NEW GAME
#  |- STATS
#      | - RAW DATA
#      | - NUMBER OF GUESSES
#      | - TIME TO WIN
#      | <- MAIN MENU
#  |- QUIT


# načti herní statistiky do dataframe, pro sichr použij absolutní cestu
stats_path = Path(__file__).parent.absolute() / "global_game_stats.csv"
global_stats = pd.read_csv(stats_path)

MAIN_MENU_TEXT = """
----------------------------
       BULLS AND COWS
----------------------------       
1) New Game
2) Stats
3) Quit Game
----------------------------"""

STAT_MENU_TEXT = """
       STATS
----------------------------       
1) Raw Data
2) Number of Guesses
3) Time to win
4) Main Menu"""

# inicializace validity volby
selection_invalid = False

while True:
    # MAIN MENU
    if not selection_invalid:
        print(MAIN_MENU_TEXT)
    main_menu_selection = input(">>> ")

    if main_menu_selection in ["1", "2", "3", "4"]:
        selection_invalid = False
        # 1) NEW GAME
        # opakovaně hraj hru dokud to uživatele neomrzí
        while main_menu_selection == "1":
            stats = play_game(global_stats)

            if stats:
                global_stats = add_game_stats(stats, global_stats)

            print("-" * 20)
            print("Play again? (1)Yes (0)No")
            if play_again := input(">>> ") != "1":
                global_stats.to_csv(stats_path, index=False)
                break
        # 2) STATS
        while main_menu_selection == "2":
            if not selection_invalid:
                print(STAT_MENU_TEXT)
            stat_menu_selection = input(">>> ")

            if stat_menu_selection in ["1", "2", "3", "4"]:
                selection_invalid = False
                if stat_menu_selection == "1":
                    print(global_stats)
                elif stat_menu_selection == "2":
                    print(n_guesses_chart(global_stats))
                elif stat_menu_selection == "3":
                    print(time_to_win_chart(global_stats))
                elif stat_menu_selection == "4":
                    break
                print(20 * "-")
            else:
                print("Invalid Selection!")
                selection_invalid = True
        # 3) QUIT
        if main_menu_selection == "3":
            print("Goodbye!")
            break
    else:
        print("Invalid Selection!")
        selection_invalid = True
