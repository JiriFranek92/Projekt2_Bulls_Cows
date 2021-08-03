"""Modul na tvorbu ASCII sloupcových grafů z dat v sloupci Pandas dataframe.

Modul obsahuje tři typy grafů. AsciiChart přímo zobrazí data ve sloupci.
BarChart je graf četností unikátních hodnot. Histogram je histogram sloupce
s numerickou proměnnou.

    Typické použití:

    chart = Histogram(df, col_name)  # inicializace
    chart.sort_data(sort_by="index")  # nastavení řazení
    chart.format(symbol="*")  # nastavení formátu
    chart.show()  # vypsání grafu
"""


import pandas as pd


def _get_col(data, x):
    # validuje dataframe inicializované instance
    # vrátí sloupec daný parametrem x
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a Pandas DataFrame!")
    else:
        try:
            return data[x]
        except KeyError:
            raise KeyError(f"No column '{x}' in '{data}' DataFrame.")


class AsciiChart:
    """Sloupcový graf vytvořený pomocí ASCII znaků.

    Atributy:
        col: Series, zdrojový sloupec dat pro graf
        chart_data:
            Series, data která má graf znázornit
            (pro základní třídu přímo zdrojová data)
        labels: list/tuple text záhlaví grafu
        symbol: symbol, kterým se mají vykreslit sloupce
        max_symbols: integer, maximální počet symbolů = max délka sloupce"""

    def __init__(self, data, x):
        """Vytvoří instanci grafu ze zadaných dat.

        Argumenty:
            data: DataFrame, zdroj dat.
            x: string, název zvoleného sloupce."""

        self.col = _get_col(data, x)
        self.chart_data = self._get_chart_data()

        self.labels = [x, 'COUNT']
        self.symbol = "#"
        self.max_symbols = 100

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError(
                "Invalid setting: 'labels' must be a list or a tuple!")
        elif len(value) != 2:
            raise TypeError("Invalid setting: 'labels' must be of length 2!")
        else:
            self._labels = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        try:
            value_str = str(value)
        except TypeError:
            raise TypeError(
                "Invalid setting: 'symbol' not convertible to a string!")
        else:
            self._symbol = value_str

    @property
    def max_symbols(self):
        return self._max_symbols

    @max_symbols.setter
    def max_symbols(self, value):
        try:
            value_int = int(value)
        except TypeError:
            raise TypeError("Invalid setting: 'max_symbols' not an integer!")
        else:
            if value_int < 1:
                raise ValueError(
                    "Invalid setting: 'max_symbols' not greater than 0!")
            else:
                self._max_symbols = value_int

    def _get_chart_data(self):
        # Vrátí data pro graf. U základní třídy přímo vybraný sloupec.
        # Funkce překrytá u potomků BarChart a Histogram.
        return self.col

    def _get_label_col_width(self):
        # vrátí šířku sloupce popisků
        # (co je delší: délka nejdelšího popisku, nebo délka textu záhlaví)
        data_labels_lens = [len(str(i)) for i in self.chart_data.index]
        labels_heading_len = len(str(self.labels[0]))
        return max(*data_labels_lens, labels_heading_len)

    def _get_values_col_width(self, vps):
        # vrátí šířku sloupce hodnot
        # (co je delší: délka sloupce + délka textu popisku + mezera
        # NEBO délka textu záhlaví)
        longest_col = max(self.chart_data)
        longest_col_length = longest_col // vps
        longest_col_label_length = len(str(longest_col))

        values_heading_len = len(str(self.labels[1]))

        return max(longest_col_length + longest_col_label_length + 1,
                   values_heading_len)

    def _print_chart(self):
        # vytiskne graf
        output = []

        # --------------- pomocné proměnné pro správné formátování ------------
        # hodnota na symbol
        vps = max(self.chart_data) // self.max_symbols + 1

        # šířky sloupců
        label_col_width = self._get_label_col_width()
        values_col_width = self._get_values_col_width(vps)

        # separátor
        sep = (label_col_width + values_col_width + 2) * "-"

        # --------------- tisk grafu ------------------------------------------
        # tiskni záhlaví
        #    POPISEK   |   HODNOTA
        output.append(f"{str(self.labels[0]): ^{label_col_width}}"
                      f"|{str(self.labels[1]): ^{values_col_width}}")

        output.append(sep)
        # tiskni jednotlivé údaje do grafu
        #       popisek|####### (číslo)
        for label, value in self.chart_data.items():
            output.append(f"{str(label): >{label_col_width}}|"
                          f"{value // vps * str(self.symbol)} {str(value)}")
        output.append(sep)

        print("\n".join(output))

    def _print_summary(self):
        # Vytiskne deskriptivní statistiky sloupce dataframe (min, mean, max)
        return (f"Min: {self.col.min()} Mean: {self.col.mean().round(2)} "
                f"Max: {self.col.max()}")

    def sort_data(self, sort_by="values", asc=True):
        """Seřadí data pro graf.

        Argumenty:
            sort_by: Pokud 'index' řaď podle indexu, jinak podle hodnot.
            asc: Bool, jesli řadit vzestupně, jinak sestupně."""
        if sort_by == "index":
            self.chart_data = self.chart_data.sort_index(ascending=asc)
        else:
            self.chart_data = self.chart_data.sort_values(ascending=asc)

    def format(self, **kwargs):
        """Změní proměnné na formátování grafu.

        Argumenty:
            kwargs: Formátovací proměnné a jejich honoty.

        Vyvolává:
            TypeError: Chybné typy formátovacích proměnných.
        """
        allowed = {"labels", "symbol", "max_symbols"}
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)

    def show(self):
        """ Vytiskne graf a deskriptivní statistiky."""
        self._print_chart()
        self._print_summary()


class BarChart(AsciiChart):
    """Sloupcový graf počtu hodnot vytvořený pomocí ASCII znaků.

    Atributy:
        Viz rodičovská třída AsciiChart."""
    def _get_chart_data(self):
        # Vrátí data pro graf:
        # Unikátní hodnoty ve zdrojovém sloupci a jejich počet
        self.chart_data = self.col.value_counts()


class Histogram(AsciiChart):
    """Histogram vytvořený pomocí ASCII znaků.

    Atributy:
        col, labels, symbol, max_symbols:
            Viz rodičovská třída AsciiChart.
        chart_data:
            Series, data která má graf znázornit
            (pro histogram zdrojová data rozdělená do tříd a jejich počet)
        n: Integer, počet tříd
        binwidth: Šířka třídy (přibližná)
        precision:
            Počet míst na které se mají hranice tříd zaokrouhlit.
            Záporný počet zančí zaokrouhlování na desítky, stovky ...
        """

    def __init__(self, data, x, n=10, binwidth=None, precision=3):
        """Inicializuje jako u základní třídy + parametry pro histogram."""
        self.n = n
        self.binwidth = binwidth
        self.precision = precision
        
        AsciiChart.__init__(self, data, x)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        try:
            value_int = int(value)
        except TypeError:
            raise TypeError("'n' must be an Integer!")
        else:
            if value_int < 1:
                raise ValueError("'n' must be greater than 0!")
            else:
                self._n = value_int

    @property
    def binwidth(self):
        return self._binwidth

    @binwidth.setter
    def binwidth(self, value):
        try:
            value_float = float(value)
        except TypeError:
            raise TypeError("'binwidth' must be a number!")
        else:
            if value_float < 1:
                raise ValueError("'binwidth' must be greater than 0!")
            else:
                self._binwidth = value_float

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        try:
            int(value)
        except TypeError:
            raise TypeError("'precision' must be an Integer.")
        else:
            self._precision = int(value)

    def _get_chart_data(self):
        # Vrátí data pro graf:
        # hodnoty zdrojového sloupce rozdělené do 'n' tříd,
        # nebo podle (přibližné) šíře 'binwidth'.
        # Hranice tříd jou zaokrouhleny podle zadané přesnosti."""
        if self.binwidth is not None:
            data_range = self.col.max() - self.col.min()
            self.n = (1 if self.binwidth >= data_range
                      else data_range // self.binwidth + 1)
        return pd.cut(self.col, self.n, precision=self.precision).\
            value_counts()
