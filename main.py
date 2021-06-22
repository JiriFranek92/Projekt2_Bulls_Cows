from pathlib import Path

import pandas as pd

from ascii_chart import ascii_chart
from game import play_game

# načti herní statistiky do dataframe, pro sichr použij absolutní cestu
file_path = Path(__file__).parent.absolute()
global_stats = pd.read_csv(file_path / "global_game_stats.csv")

# ---------- STRUKTURA PROGRAMU ----------
# MAIN MENU
#  |- NEW GAME
#  |- STATS
#      | - RAW DATA
#      | - NUMBER OF GUESSES
#      | - TIME TO WIN
#      | <- MAIN MENU
#  |- QUIT

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
4) Main Menu2"""

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
        if main_menu_selection == "1":
            # opakovaně hraj hru dokud to uživatele neomrzí
            while True:
                stats = play_game(global_stats)

                if stats:
                    global_stats = global_stats.append(pd.DataFrame(
                        stats, columns=global_stats.columns, index=[0]),
                        ignore_index=True)

                print("-" * 20)
                print("Play again? (1)Yes (0)No")
                if play_again := input(">>> ") != "1":
                    global_stats.to_csv(file_path / "global_game_stats.csv",
                                        index=False)
        # 2) STATS
        elif main_menu_selection == "2":
            while True:
                if not selection_invalid:
                    print(STAT_MENU_TEXT)
                stat_menu_selection = input(">>> ")
                if stat_menu_selection in ["1", "2", "3", "4"]:
                    selection_invalid = False
                    if stat_menu_selection == "1":
                        print(global_stats)
                    elif stat_menu_selection == "2":
                        ascii_chart(data=global_stats, x="n_guesses",
                                    chart_type="hist",
                                    precision=0, labels=["GUESSES", "GAMES"],
                                    sort_by="index")
                    elif stat_menu_selection == "3":
                        ascii_chart(data=global_stats, x="time_to_win",
                                    chart_type="hist",
                                    precision=-1,
                                    labels=["TIME TO WIN(s)", "GAMES"],
                                    sort_by="index")
                    elif stat_menu_selection == "4":
                        break
                    print(20 * "-")
                else:
                    print("Invalid Selection!")
                    selection_invalid = True
        # 3) QUIT
        elif main_menu_selection == "3":
            print("Goodbye!")
            break
    else:
        print("Invalid Selection!")
        selection_invalid = True
