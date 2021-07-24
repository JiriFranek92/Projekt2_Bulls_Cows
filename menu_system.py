from tabulate import tabulate

# from ascii_chart import ascii_chart
# from game import play_game

from os import system, name


# clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Main:
    def __init__(self, main_menu):
        self.menu = main_menu
        self.is_selection_valid = True

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, value):
        if not isinstance(value, Menu):
            raise TypeError("'main_menu' must be a Menu class!")
        else:
            self._menu = value

    def __call__(self):
        while True:
            if self.is_selection_valid:
                clear()
                print(self.menu)
            sel = input(">>> ")
            try:
                self.menu = self.menu[sel]()
            except KeyError:
                if sel == "*":
                    break
                print(f"'{sel}' is not a valid selection!")
                self.is_selection_valid = False
            else:
                self.is_selection_valid = True


class Menu:
    def __init__(self, title="", width=30, sep_symbol="-"):
        self.title = str(title)
        self.items = {}
        self.sep_symbol = sep_symbol
        self.width = width

    @property
    def sep_symbol(self):
        return self._sep_symbol

    @sep_symbol.setter
    def sep_symbol(self, value):
        if len(str(value)) != 1:
            print("Invalid format! 'sep_symbol' must be only 1 charcter!")
        else:
            self._sep_symbol = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        # nastav zadaná šířka jen pokud je větší než délka titulku menu,
        # jinak nastav rovnou délce titulku
        self._width = len(self.title) if value < len(self.title) else value

    def add_item(self, id, name="", func=None, menu=None):
        menu = menu if menu is not None else self
        self.items[str(id)] = MenuItem(name, func, menu)

    def __str__(self):
        sep = self.sep_symbol * self.width
        out = [sep, f"{self.title: ^{self.width}}", sep]

        out += [f"{k}) {v.name}" for k, v in self.items.items()]

        return "\n".join(out)

    def __getitem__(self, key):
        return self.items[key]


class MenuItem:
    def __init__(self, name, func, menu):
        self.name = str(name)
        self.func = func
        self.menu = menu

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, value):
        if not (callable(value) or value is None):
            raise TypeError("'func' must be a function!")
        else:
            self._func = value

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, value):
        if not isinstance(value, Menu):
            raise TypeError("'menu' must be a Menu class!")
        else:
            self._menu = value

    def __call__(self):
        if self.func is not None:
            self.func()
        return self.menu


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

