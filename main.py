from pathlib import Path

import pandas as pd

from menus import *


# načti herní statistiky do dataframe, pro sichr použij absolutní cestu
stats_path = Path(__file__).parent.absolute() / "global_game_stats.csv"
global_stats = pd.read_csv(stats_path)

# ---------- STRUKTURA PROGRAMU ----------
# MAIN MENU
#  |- NEW GAME
#  |- STATS
#      | - RAW DATA
#      | - NUMBER OF GUESSES
#      | - TIME TO WIN
#      | <- MAIN MENU
#  |- QUIT

# inicializace validity volby
selection_invalid = False

while True:
    # MAIN MENU
    if not selection_invalid:
        print_menu(main_menu)
    main_menu_selection = input(">>> ")

    if main_menu_selection in ["1", "2", "3", "4"]:
        selection_invalid = False
        # 1) NEW GAME
        # opakovaně hraj hru dokud to uživatele neomrzí
        while main_menu_selection == "1":
            play_again, global_stats = game_loop(global_stats, stats_path)
            if play_again != "1":
                break
        # 2) STATS
        while main_menu_selection == "2":
            if not selection_invalid:
                print_menu(stats_menu)
            stat_menu_selection = input(">>> ")

            if stat_menu_selection in ["1", "2", "3", "4"]:
                selection_invalid = False
                if stat_menu_selection == "1":
                    print(raw_data(global_stats))
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
