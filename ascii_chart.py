import pandas as pd


def ascii_chart(data, x, chart_type, n=10, binwidth=None, precision=3,
                labels=None, symbol="*", sort=True, sort_by="values",
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
    :param asc: Jestli se má graf řadit vzestupně.
    :param max_symbols: Maximální délka sloupce v symbolech.
    """

    # --------------- kontrola vstupních dat ----------------------------------
    # 'data' je DataFrame
    if not isinstance(data, pd.DataFrame):
        print("Input must be a Pandas DataFrame!")
        return

    # 'labels' je list/tuple o délce 2
    # (nejprve přiřaď defaultní hodnoty)
    if labels is None:
        labels = [x, 'COUNT']

    if not any((isinstance(labels, list), isinstance(labels, tuple)) or len(
            labels) == 2):
        print("'labels' argument must be a list or a tupple of lenght 2!")
        return

    # --------------- zpracování dat ------------------------------------------
    if chart_type == "bar":
        # sloupcový: získej počty jednotlivých tříd
        chart_data = data[x].value_counts()
    elif chart_type == "hist":
        # histogram: vezmi počet tříd, nebo spočítej z šířky
        #  rozřaď pozorování do tříd, získej počty
        n = n if binwidth is None else int(
            (data[x].max() - data[x].min()) // binwidth + 1)
        chart_data = (pd.cut(data[x], n, precision=precision)
                        .value_counts())
    else:
        print(f"'{chart_type}' is not a valid chart type!")
        return

    # seřaď data
    if sort:
        if sort_by == "index":
            chart_data = chart_data.sort_index(ascending=asc)
        else:
            chart_data.sort_values(ascending=asc)

    # --------------- pomocné proměnné pro správné formátování ----------------
    # hodnota na symbol
    vps = max(chart_data) // max_symbols + 1

    # šířka sloupce popisků
    # (co je delší: délka nejdelšího popisku, nebo délka textu záhlaví)
    label_col_width = \
        max(max([len(str(i)) for i in chart_data.index]),
            len(str(labels[0])))

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
    # (margin_label_l)POPISEK(margin_label_r)|(margin_value)HODNOTA
    margin_label_l = ((label_col_width - len(str(labels[0]))) // 2)
    margin_label_r = (
            label_col_width - len(str(labels[0])) - margin_label_l)
    margin_value = ((values_col_width - len(str(labels[1]))) // 2)
    print(f"{margin_label_l * ' '}{str(labels[0])}{margin_label_r * ' '}"
          f"|{margin_value * ' '}{str(labels[1])}")

    print(sep)
    # tiskni jednotlivé údaje do grafu
    # (margin_label)popisek|****** (číslo)
    for label, value in chart_data.items():
        margin_label = (label_col_width - len(str(label))) * " "
        print(
            f"{margin_label}{str(label)}|{value // vps * str(symbol)} "
            f"{str(value)}")

    # tiskni deskriptivní statistiky
    print(sep)
    # print(f"observations: {data.count()}")
    print(f"Min: {data[x].min()} Mean: {data[x].mean().round(2)} "
          f"Max: {data[x].max()}")
