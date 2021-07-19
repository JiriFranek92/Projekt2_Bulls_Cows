from tabulate import tabulate

from ascii_chart import ascii_chart
from game import play_game


def print_menu(menu, width=30, symbol="-"):
    sep = width * symbol
    print(sep)
    print(f"{menu['title']: ^{width}}")
    print(sep)

    for key, item in menu["items"].items():
        print(f"{key}) {item}")

    print(sep)


def game_loop(glob_stats, stats_path):
    exit_code, stats = play_game(glob_stats)

    if exit_code == 0:
        new_stats = glob_stats.append(stats, ignore_index=True)
        stats.to_csv(stats_path, index=False, header=False, mode="a")
    else:
        new_stats = glob_stats

    print("-" * 20)
    print("Play again? (1)Yes (0)No")
    again = input(">>> ")
    return again, new_stats


# ---------------------- Funkce menu statistik --------------------------------
def raw_data(dataframe):
    return tabulate(dataframe, showindex=False, tablefmt="psql",
                    headers=("Game \nnumber", "Number of \nGuesses",
                             "Time to \nwin"))


def n_guesses_chart(dataframe):
    return ascii_chart(data=dataframe, x="n_guesses", chart_type="hist",
                       precision=0, labels=["GUESSES", "GAMES"],
                       sort_by="index")


def time_to_win_chart(dataframe):
    return ascii_chart(data=dataframe, x="time_to_win", chart_type="hist",
                       precision=-1, labels=["TIME TO WIN(s)", "GAMES"],
                       sort_by="index")


main_menu = {"title": "BULLS AND COWS",
             "items": {1: "New Game",
                       2: "Stats",
                       3: "Quit Game"}}

stats_menu = {"title": "STATS",
              "items": {1: "Raw Data",
                        2: "Number of Guesses",
                        3: "Time to win",
                        4: "Main Menu"}}

