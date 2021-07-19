import pandas as pd


class AsciiChart:
    def __init__(self, data, x):
        self.col = self._get_col(data, x)
        self.chart_data = self._get_chart_data()

        # self.default_values = {"labels": ['LABELS', 'VALUES'],
        #                        "symbol": "#",
        #                        "max_symbols": 100}
        # self.__dict__.update(self.default_values)
        self.labels = [x, 'COUNT']
        self.symbol = "#"
        self.max_symbols = 100

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        if not isinstance(value, (list, tuple)):
            print("Warning: 'labels' must be a list or a tuple!")
        elif len(value) != 2:
            print("Warning: 'labels' must be of length 2!")
        else:
            self._labels = value
    #
    # @property
    # def symbol(self):
    #     return self._symbol
    #
    # @symbol.setter
    # def symbol(self, value):
    #     try:
    #         str(value)
    #     except TypeError:
    #         print("Warning: 'symbol' must be convertible to a string!")
    #     else:
    #         self._symbol = value
    #
    # @property
    # def max_symbols(self):
    #     return self._max_symbols
    #
    # @max_symbols.setter
    # def max_symbols(self, value):
    #     try:
    #         value = int(value)
    #     except TypeError:
    #         print("Warning: 'symbol' must be convertible to a string!")
    #     else:
    #         if value < 1:
    #             print("Warning: Max sybols value must be greater than 0!")
    #         else:
    #             self._max_symbols = value

    @staticmethod
    def _get_col(data, x):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a Pandas DataFrame!")
        else:
            try:
                return data[x]
            except KeyError:
                raise KeyError(f"No column '{x}' in '{data}' DataFrame.")

    def _get_chart_data(self):
        return self.col

    def _print_chart(self):
        # vytiskne graf

        output = ""

        # --------------- pomocné proměnné pro správné formátování ------------
        # hodnota na symbol
        vps = max(self.chart_data) // self.max_symbols + 1

        # šířka sloupce popisků
        # (co je delší: délka nejdelšího popisku, nebo délka textu záhlaví)
        label_col_width = \
            max(*[len(str(i)) for i in self.chart_data.index],
                len(str(self.labels[0])))

        # šířka sloupce hodnot
        # (co je delší: délka sloupce + délka textu popisku + mezera
        # NEBO délka textu záhlaví)
        values_col_width = max(max(self.chart_data) // vps +
                               len(str(max(self.chart_data))) + 1,
                               len(str(self.labels[1])))

        # separátor
        sep = (label_col_width + values_col_width + 2) * "-"

        # --------------- tisk grafu ------------------------------------------
        # tiskni záhlaví
        #    POPISEK   |   HODNOTA
        output += (f"{str(self.labels[0]): ^{label_col_width}}"
                   f"|{str(self.labels[1]): ^{values_col_width}}") + "\n"

        output += sep + "\n"
        # tiskni jednotlivé údaje do grafu
        #       popisek|****** (číslo)
        for label, value in self.chart_data.items():
            output += (f"{str(label): >{label_col_width}}|"
                       f"{value // vps * str(self.symbol)} {str(value)} \n")

        output += sep + "\n"

        print(output)

    def _print_summary(self):
        # Vytiskne deskriptivní statistiky sloupce dataframe (min, mean, max)
        return (f"Min: {self.col.min()} Mean: {self.col.mean().round(2)} "
                f"Max: {self.col.max()}")

    def sort_data(self, sort_by="values", asc=True):
        """ Seřadí data pro graf."""
        if sort_by == "index":
            self.chart_data = self.chart_data.sort_index(ascending=asc)
        else:
            self.chart_data = self.chart_data.sort_values(ascending=asc)

        return self

    def format(self, **kwargs):
        """ Změní proměnné na formátování grafu """
        allowed = {"labels", "symbol", "max_symbols"}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed)
        return self

    def print(self):
        self._print_chart()
        self._print_summary()


class BarChart(AsciiChart):
    def _get_chart_data(self):
        self.chart_data = self.col.value_counts()


class Histogram(AsciiChart):
    def __init__(self, data, x, n=10, binwidth=None, precision=3):
        self.n = n
        self.binwidth = binwidth
        self.precision = precision
        
        AsciiChart.__init__(self, data, x)

    def _get_chart_data(self):
        if self.binwidth is not None:
            self.n = int((self.col.max() - self.col.min()) //
                         self.binwidth + 1)
        return pd.cut(self.col, self.n, precision=self.precision).\
            value_counts()