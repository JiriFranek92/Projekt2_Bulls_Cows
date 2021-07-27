import sys

from tabulate import tabulate

from menu_system import Main, Menu, clear
from stats import Stats
from ascii_chart import Histogram
from game import BullsAndCows


def n_guesses_chart():
    chart = Histogram(data=global_stats.df, x="n_guesses", precision=0)
    chart.sort_data(sort_by="index")
    chart.format(labels=["GUESSES", "GAMES"])
    chart.show()
    input("...")


def time_to_win_chart():
    chart = Histogram(data=global_stats.df, x="time_to_win", precision=-1)
    chart.sort_data(sort_by="index")
    chart.format(labels=["TIME TO WIN(s)", "GAMES"])
    chart.show()
    input("...")


def raw_data():
    print(tabulate(global_stats.df, showindex=False, tablefmt="psql",
                   headers=("Game \nnumber", "Number of \nGuesses",
                            "Time to \nwin")))
    input("...")


def quit_game():
    print("Thanks for playing")
    sys.exit(0)


def game_loop():
    while True:
        clear()
        game = BullsAndCows(global_stats if global_stats.valid else None)
        game.play()

        if game.finished and global_stats.valid:
            global_stats.add(game.game_stats)

        print("-" * 20)
        print("Play again? (1)Yes (0)No")
        again = input(">>> ")
        if again != "1":
            break


def create_menus():
    main_menu = Menu("BULLS AND COWS", sep_symbol="=")
    stats_menu = Menu("STATISTICS")

    main_menu.add_item(1, "New Game", func=game_loop)
    main_menu.add_item(2, "Stats", menu=stats_menu)
    main_menu.add_item(3, "Quit Game", func=quit_game)
    # main_menu.show()

    stats_menu.add_item(1, "Raw Data", func=raw_data)
    stats_menu.add_item(2, "Number of Guesses", func=n_guesses_chart)
    stats_menu.add_item(3, "Time to win", func=time_to_win_chart)
    stats_menu.add_item(4, "Main Menu", menu=main_menu)

    return main_menu, stats_menu


def main():
    main_menu, stats_menu = create_menus()

    # noinspection PyGlobalUndefined
    global global_stats
    global_stats = Stats("bad_stats.csv")
    if global_stats.errors:
        print("\n".join(global_stats.errors))

    Main(main_menu)()


if __name__ == "__main__":
    main()
