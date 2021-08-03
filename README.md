# Projekt2_Bulls_Cows

Hra Bulls and Cows vytvořená v Pythonu a hraná pomocí příkazové řádky.

Hráč v ní hádá tajné čtyřciferné číslo, kde se žádná číslice neopakuje.
Pokud hráč uhádne cifru je to 'Cow', pokud uhádne cifru i umístění je to
'Bull'. Cílem je tedy měnit cifry a jejich umístění v hádaném čísle,
dokud hráč neuhádne číslo celé.

Hra si uchovává počet hádání a čas potřebný k dohrání jednotlivých her. 
Tyto globální statistiky jsou uchovávány v csv souboru. Tyto statistiky
si lze zobrazit v tabulce nebo ve formě ASCII grafů.

Vyžaduje insatlaci modulů pandas, numpy a tabulate viz requirements.txt

Struktura programu:
- main.py: hlavní modul
- menu-system.py: modul pro tvorbu systému menu
- game.py: modul pro samotnou hru
- stats.py: modul pro práci se statistikami
- ascii_chart.py: modul pro tvorbu ASCII grafů
- global_game_stats.csv: soubor pro uchování statistik minulých her
