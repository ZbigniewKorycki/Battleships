import string

def stworz_pusta_plansze(wiersze, kolumny):
    return [['~' for _ in range(kolumny)] for _ in range(wiersze)]

def wydrukuj_plansze(plansza):
    naglowki_kolumn = [' '] + [str(i) for i in range(1, len(plansza[0]) + 1)]
    print('\t'.join(naglowki_kolumn))
    for i, wiersz in enumerate(plansza):
        litera_wiersza = string.ascii_uppercase[i]
        wiersz_str = '\t'.join(wiersz)
        print(f"{litera_wiersza}\t{wiersz_str}")

def umiesc_statek(plansza, wiersz, kolumna, dlugosc_statku):
    for i in range(dlugosc_statku):
        plansza[wiersz][kolumna + i] = 'S'

def strzal(plansza, koordynaty):
    wiersz = koordynaty[0]
    kolumna = koordynaty[1]
    if plansza[wiersz][kolumna] == "S":
        print("trafiony !")
        plansza[wiersz][kolumna] = "~"
        wydrukuj_plansze(plansza)
    else:
        print("chybiony !")

def sprawdzenie_polozenia_statku(plansza, koordynaty, dlugosc_statku):
    wiersz = koordynaty[0]
    kolumna = koordynaty[1]
    if plansza[wiersz][kolumna - 1] == "S" or plansza[wiersz][kolumna + dlugosc_statku] == "S":
        print("inny statek znajduje sie za blisko")
        print(plansza[wiersz][2])
    else:
        print("ok")


plansza = stworz_pusta_plansze(10, 10)
umiesc_statek(plansza, 0, 2, 3)
wydrukuj_plansze(plansza)


sprawdzenie_polozenia_statku(plansza, (0, 2), 3)



