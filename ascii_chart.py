import pandas as pd


def print_summary(data, x):
    """Vytiskne deskriptivní statistiky sloupce dataframe (min, mean, max"""
    return (f"Min: {data[x].min()} Mean: {data[x].mean().round(2)} "
            f"Max: {data[x].max()}")


def validate_inputs(data, labels, chart_type):
    """ Zkontroluje vstupy funkce ascii grafu, vrátí validitu
     a popř chybovou hlášku."""
    # 'data' se dá převést na DataFrame
    if not isinstance(data, pd.DataFrame):
        return False, "Input must be a Pandas DataFrame!"
    # 'labels' je list/tuple o délce 2
    elif not(isinstance(labels, (list, tuple))):
        return False, "'labels' argument must be a list or a tupple!"
    # 'chart_type' je validní typ grafu"
    elif chart_type not in ["bar", "hist"]:
        return False, f"'{chart_type}' is not a valid chart type!"
    else:
        return True, ""


def hist_data(col, n, binwidth, precision):
    """ Vytvoří zpracovaná data pro histogram, rozřazením vstupního sloupce
    dat do tříd (podle počtu nebo přibližné šířky)."""
    # histogram: vezmi počet tříd, nebo spočítej z šířky
    #  rozřaď pozorování do tříd, získej počty
    n = n if binwidth is None else int(
        (col.max() - col.min()) // binwidth + 1)
    return pd.cut(col, n, precision=precision).value_counts()


def sort_chart_data(chart_data, sort_by, asc):
    """ Vrátí seřazená data pro graf."""
    if sort_by == "index":
        return chart_data.sort_index(ascending=asc)
    else:
        return chart_data.sort_values(ascending=asc)


def print_chart(chart_data, labels=None, symbol='#',
                max_symbols=100):
    """"""
    if not isinstance(chart_data, pd.Series) or len(chart_data) == 0:
        return "* Invalid input!"

    if labels is None:
        labels = ['LABELS', 'VALUES']

    output = ""

    # --------------- pomocné proměnné pro správné formátování ----------------
    # hodnota na symbol
    vps = max(chart_data) // max_symbols + 1

    # šířka sloupce popisků
    # (co je delší: délka nejdelšího popisku, nebo délka textu záhlaví)
    label_col_width = \
        max(*[len(str(i)) for i in chart_data.index], len(str(labels[0])))

    # šířka sloupce hodnot
    # (co je delší: délka sloupce + délka textu popisku + mezera
    # NEBO délka textu záhlaví)
    values_col_width = max(max(chart_data) // vps +
                           len(str(max(chart_data))) + 1,
                           len(str(labels[1])))

    # separátor
    sep = (label_col_width + values_col_width + 2) * "-"

    # --------------- tisk grafu ----------------------------------------------
    # tiskni záhlaví
    #    POPISEK   |   HODNOTA
    output += (f"{str(labels[0]): ^{label_col_width}}"
               f"|{str(labels[1]): ^{values_col_width}}") + "\n"

    output += sep + "\n"
    # tiskni jednotlivé údaje do grafu
    #       popisek|****** (číslo)
    for label, value in chart_data.items():
        output += (
            f"{str(label): >{label_col_width}}|{value // vps * str(symbol)} "
            f"{str(value)}") + "\n"

    output += sep + "\n"

    return output


def ascii_chart(data, x, chart_type, n=10, binwidth=None, precision=3,
                labels=None, symbol="#", sort=True, sort_by="values",
                asc=True, max_symbols=100):
    """ vezme DataFrame a pro zvolený sloupec vypíše ascii sloupcový graf,
     nebo histogram
    :param data: Zdrojový DataFrame.
    :param x: Název sloupce dat.
    :param chart_type: Typ grafu.
        Možnosti: "bar" -> sloupcový, "hist" -> histogram
    :param n: počet tříd histogramu
    :param binwidth: přibližná šířka tříd histogramu
    :param precision: řád zaokrouhlení hranic tříd histogramu
    :param labels: List nebo tuple s nadpisy. Defaultně název sloupce a 'COUNT'
    :param symbol: Symbol, který se používá pro sloupce.
    :param sort: Jestli má být graf seřazen.
    :param sort_by: Jestli řadit podle hodnot, nebo podle indexu
        ("values"/"index")
    :param asc: Jestli se má graf řadit vzestupně.
    :param max_symbols: Maximální délka sloupce v symbolech.
    """
    # pokud nejsou na vstupu zadány poipsky, přiřaď defaultní
    output = ""

    if labels is None:
        labels = [x, 'COUNT']

    # ----- validace vstupů
    inputs_valid, err_message = validate_inputs(data, labels, chart_type)

    if not inputs_valid:
        return err_message
    else:
        # ----- zpracování dat
        chart_data = pd.Series()
        if chart_type == "bar":
            chart_data = data[x].value_counts()
        elif chart_type == "hist":
            chart_data = hist_data(data[x], n, binwidth, precision)

        # ----- seřazení dat
        if sort:
            chart_data = sort_chart_data(chart_data, sort_by, asc)

        # ----- vytvoření grafu a vypsání deskriptivních statistik
        output += print_chart(chart_data, labels, symbol, max_symbols)

        output += print_summary(data, x)

        return output
