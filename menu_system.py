"""Modul na tvorbu dynamického systému menu v příkazovém řádku.

Systém tvoří tři třídy:
    - Třída Main zařizuje vypisování menu, dotazy na vstup uživatele a aktivaci
    zvolených položek.
    - Třída Menu definuje jednotlivá menu, které tvoří název a položky
    (plus znaky, které je aktivují).
    - Třída MenuItem definuje položku. Každá položka má kromě názvu funkci,
    kterou má spustit, menu do kterého má přepnout, nebo obojí.

    Menu mají pouze implicitní hiearchii. Při použití se nejprve vytvoří menu,
    poté se přidají položky, nakonec se vytvoří a spustí Main.

    Typické použítí:
    # definice menu
    main_menu = Menu("MAIN", sep_symbol="=")
    sub_menu = Menu("SUBMENU")

    # přidání položek
    main_menu.add_item(1, "Sub-Menu", menu=sub_menu)
    main_menu.add_item("q", "Quit Game", func=quit)

    sub_menu.add_item(1, "Function", func=my_function)
    sub_menu.add_item("x", "Back to Main", menu=main_menu)

    Main(main_menu)()  # spustí systém v zadaném menu
"""


from os import system, name


def clear():
    """Vyčistí konzoli."""
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac a linux
    else:
        _ = system('clear')


class Main:
    """Hlavní třída systému menu.

    Po zavolání spustí nekonečnou smyčku, která:
        - vypíše menu (pokud uživatel zadal validní volbu v minulé iteraci)
        - přijme volbu od uživatele
        - pokud byla volba validní, zavolá zvolenou položku menu a nastaví,
          které menu se má spustit při další iteraci.

    Smyčka se ukončí zadáním řetězce pro přerušení. Případně lze ukončit celý
    program vlastní funkcí zavolanou položkou v menu.

    Atributy:
        menu: menu, které se má zobrazit
        break_string: string, kterým se přeruší program.
        is_selection_valid: bool, jestli uživatel zadal validní volbu
    """

    def __init__(self, main_menu, break_string="*"):
        self.menu = main_menu
        self.break_string = break_string

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
                print(self.menu)
            sel = input(">>> ")
            try:
                self.menu = self.menu[sel]()
            except KeyError:
                if sel == self.break_string:
                    break
                print(f"'{sel}' is not a valid selection!")
                self.is_selection_valid = False
            else:
                self.is_selection_valid = True
                clear()


class Menu:
    """Menu pomocí příkazového řádku.

    Atributy:
        title: název menu
        items:
            slovník položek menu, hodnoty jsou instance třídy MenuItem,
            klíče jsou řetězce pro spuštění položky
        sep.symbol: symbol který odděluje název od položek
        width: šířka menu (ovlivňuje pouze titulek a oddělovač)
    """

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
        # šířka musí být delší než délka titulku
        self._width = len(self.title) if value < len(self.title) else value

    def add_item(self, call_string, item_name="", func=None, menu=None):
        """Vytvoří položku menu a přidá do slovníku.

        Argumenty:
            call_string: řetězec, kterým uživatel volí položku
            func: funkce, kterou má položka zavolat
            menu: menu, na které má položka přejít
        """
        menu = menu if menu is not None else self
        self.items[str(call_string)] = _MenuItem(item_name, func, menu)

    def __str__(self):
        """Vrací string pro vypsání menu.

        Menu může vypadat takto:
        ---------
           MENU
        ---------
        1) položka 1
        něco) položka 2
        #) položka 3
        """
        sep = self.sep_symbol * self.width
        out = [sep, f"{self.title: ^{self.width}}", sep]

        out += [f"{k}) {v.name}" for k, v in self.items.items()]

        return "\n".join(out)

    def __getitem__(self, key):
        """instance_menu.items["a"] -> instance_menu["a"]"""
        return self.items[key]


class _MenuItem:
    """Položka menu.

    Interní třída. Mělo by se s ní pracovat pouze pomocí metod třídy Menu.

    Atributy:
        name: název položky
        func: funkce, kterou má položka zavolat
        menu: menu, do kterého má položka přepnout
    """

    def __init__(self, item_name, func, menu):
        """Vytvoří položku menu."""
        self.name = str(item_name)
        self.func = func
        self.menu = menu

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, value):
        """Při přiřazení zajistí, že atribut func je volatelný nebo None."""
        if not (callable(value) or value is None):
            raise TypeError("'func' must be a function!")
        else:
            self._func = value

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, value):
        """Zajistí, že menu je instance třídy Menu."""
        if not isinstance(value, Menu):
            raise TypeError("'menu' must be a Menu class!")
        else:
            self._menu = value

    def __call__(self):
        """Pří zavolání instance zavolá funkci func a vrátí menu."""
        if self.func is not None:
            self.func()
        return self.menu
