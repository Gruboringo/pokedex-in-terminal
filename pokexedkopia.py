
import requests  # Biblioteka do wysyłania żądań HTTP do API
import json  # Moduł do odczytywania i zapisywania danych w formacie JSON
from pathlib import Path  # Klasa ułatwiająca tworzenie i obsługę ścieżek plików
import sys  # Moduł dający dostęp m.in. do informacji o uruchomieniu programu


# Ustala katalog, w którym znajduje się program.
# Jeśli program jest skompilowany do pliku wykonywalnego, używa lokalizacji tego pliku.
# W przeciwnym razie używa lokalizacji pliku Pythona.
project_path = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).parent
)

# Tworzy ścieżkę do pliku przechowującego kolekcję użytkownika.
backup_path = project_path / "entries" / "backup.json"

# Tworzy brakujące katalogi nadrzędne, np. folder "entries".
# Jeśli katalog już istnieje, nie zgłasza błędu.
backup_path.parent.mkdir(parents=True, exist_ok=True)

# Wypisuje pełną ścieżkę, żeby można było sprawdzić,
# gdzie program szuka i zapisuje plik kolekcji.
print(backup_path)

# Ścieżka do osobnego pliku, w którym ma być zapisana
# lokalna biblioteka wszystkich Pokémonów pobranych z API.
# Zachowaj tutaj swoją oryginalną ścieżkę.
saving_file = project_path / "pokedex" / "dex.json"
saving_file.parent.mkdir(parents=True, exist_ok=True)

# Podstawowy adres endpointu PokeAPI dla Pokémonów.
static_url = "https://pokeapi.co/api/v2/pokemon/"


def collection():
    # Próbuje otworzyć istniejący plik z kolekcją.
    try:
        with open(backup_path, "r") as file:
            # Odczytuje zawartość JSON i zamienia ją
            # na obiekt Pythona, w tym przypadku słownik.
            backed = json.load(file)

            # Zwraca odczytaną kolekcję do miejsca wywołania funkcji.
            return backed

    # Ten blok uruchamia się, gdy plik jeszcze nie istnieje.
    except FileNotFoundError:
        print("yes")

        # Tworzy pusty słownik, czyli pustą kolekcję.
        backed = {}

        # Otwiera plik w trybie zapisu.
        # Jeśli plik nie istnieje, zostanie utworzony.
        with open(backup_path, "w") as file:
            # Zapisuje pusty słownik w formacie JSON.
            json.dump(backed, file, indent=4)

            # Zwraca pustą kolekcję.
            return backed
     # Ten blok uruchamia się, jeśli istniejący plik
        # zawiera niepoprawny JSON, np. jest pusty lub uszkodzony.
    except json.JSONDecodeError:
            print("decoding error!")
    
            # Kończy działanie programu.
            sys.exit()
def dex():
    try:
        with open(saving_file, "r") as file:
            pokedex = json.load(file)
            
            return pokedex
    except FileNotFoundError:
        print("yes")
        
        v = get_all()
        if v:
            with open(saving_file, "r") as file:
                 pokedex = json.load(file)
                 return pokedex
        else:
            print("fatal error")
        
        


                
        


    # Ten blok uruchamia się, jeśli istniejący plik
            # zawiera niepoprawny JSON, np. jest pusty lub uszkodzony.
    except json.JSONDecodeError:
                print("decoding error!")
        
                # Kończy działanie programu.
                sys.exit()


   

def get_all():
    # Przygotowuje pusty słownik na pobraną bibliotekę.
    # Kluczem będzie numer Pokémona, a wartością jego nazwa.
    alles = {}

    # Dodaje parametr limit=1025 do adresu API,
    # aby pobrać listę 1025 Pokémonów w jednym żądaniu.
    url = f"{static_url}?limit=1025"

    # Próbuje wysłać żądanie do API.
    try:
        response = requests.get(url)

    # Obsługuje błędy związane z połączeniem i żądaniem HTTP.
    except requests.exceptions.RequestException:
        print("problem z połączeniem")
        return False

    # Sprawdza, czy API zwróciło status HTTP 200,
    # czyli że żądanie zakończyło się powodzeniem.
    if response.status_code == 200:
        # Odczytuje odpowiedź JSON i zamienia ją na obiekty Pythona.
        pokemon_data = response.json()

        # Tymczasowo wyświetla listę wyników,
        # żeby można było sprawdzić strukturę otrzymanych danych.
        

        # Przechodzi przez każdy wpis z listy wyników API.
        for pokemon in pokemon_data["results"]:
            # Dzieli URL Pokémona na fragmenty przy każdym ukośniku.
            lista = pokemon["url"].split("/")

            # Wybiera przedostatni element listy.
            # Ponieważ URL kończy się ukośnikiem, jest nim identyfikator.
            v = lista[-2]

            # Dodaje do słownika parę: identyfikator i nazwa Pokémona.
            alles[v] = pokemon["name"]

        # Wyświetla przygotowany słownik biblioteki.
        

        # Zapisuje bibliotekę do pliku wskazanego przez saving_file.
        saves(alles, saving_file)
        return True
    else:
        print(f"error {response.status_code}! ")
        return False
def count(col):
    # Liczy elementy w słowniku kolekcji.
    colen = len(col)

    # Oblicza, ile Pokémonów brakuje do przyjętej liczby 1025.
    how_many_left = 1025 - colen

    # Wyświetla liczbę zebranych Pokémonów i pozostałych do zebrania.
    print(f"{colen} pokemon. {how_many_left} left to get em all!")


def sort(col):
    # Tworzy nowy słownik na podstawie posortowanych elementów.
    # col.items() udostępnia pary (klucz, wartość).
    # lambda wybiera klucz sortowania.
    # int(item[0]) zamienia klucz na liczbę, aby np. "10"
    # nie znalazło się przed "2" tylko dlatego, że to tekst.
    sortedo = {
        k: v
        for k, v in sorted(
            col.items(),
            key=lambda item: int(item[0])
        )
    }

    # Zamienia posortowany słownik na tekst w formacie JSON.
    save = json.dumps(sortedo)

    # Otwiera plik kolekcji w trybie zapisu.
    # Tryb "w" nadpisuje jego dotychczasową zawartość.
    with open(backup_path, "w") as file:
        # Zapisuje przygotowany tekst JSON do pliku.
        file.write(save)


def show(col):
    # Pobiera widok par klucz–wartość ze słownika.
    showed = col.items()

    # Wyświetla nagłówek listy.
    print("Your pokemon: ")

    # Przechodzi przez każdą parę: numer i nazwa Pokémona.
    for k, v in showed:
        # Formatuje numer do minimum trzech cyfr, np. 1 jako 001.
        print(f"#{int(k):03d} - {v}")


def help_me():
    # Wyświetla nagłówek listy komend.
    print("List of commands:")

    # Lista nazw komend wraz z krótkimi opisami.
    # Nazwa zmiennej "commmands" jest zachowana z Twojego kodu.
    commmands = [
        "show - shows all collected pokemon",
        "delete - deletes pokemon of your choosing",
        "count - counts how many pokemon you have, and how many you need to get all",
        "sort - sorts pokemon in dictonary ",
        "exit - exits from the aplication",
        "poke - looks for pokemon from your collection",
        "help - help, duhhh"
    ]  # Możesz później zmienić opisy lub usunąć komendę sort.

    # Wyświetla kolejno każdy opis z listy.
    for v in commmands:
        print(v)


def saves(content, path):
    # Otwiera wskazany plik w trybie zapisu.
    # Argument "path" pozwala wskazać różne pliki,
    # a "content" określa dane, które mają zostać zapisane.
    with open(path, "w") as file:
        # Zapisuje dane jako JSON z wcięciami ułatwiającymi odczyt.
        json.dump(content, file, indent=4)

def nine_exceptions(value):
     lista = ["ho-oh", "porygon-z", "jangmo-o", "hakamo-o", "type-null", "kommo-o", "ting-lu", "chien-pao", "wo-chien", "chi-yu" ]
    
     if value in lista:
               
               return value
     else:
          splited = value.split("-")
          hi = splited[0]
          
          return hi
               
     
def poke(col):
    # Pętla pozwala wyszukiwać wiele Pokémonów,
    # dopóki użytkownik nie wpisze "back".
    while True:
        # Na początku każdego wyszukiwania zakładamy,
        # że Pokémon nie został jeszcze znaleziony.
        founde = False

        # Pobiera wpis użytkownika, usuwa białe znaki
        # z początku i końca oraz zamienia tekst na małe litery.
        sack = input(f"What pokemon are you looking for?: ").lower().strip()

        # Kończy pętlę wyszukiwania, gdy użytkownik wpisze "back".
        if sack == "back":
            break

        # Jeśli wpis zawiera same cyfry, normalizuje numer.
        # Np. "001" zostaje zamienione na "1".
        if sack.isdigit():
            sack = str(int(sack))

        # Przeszukuje pary numer–nazwa w kolekcji.
        for k, v in col.items():
            # Sprawdza, czy wpis pasuje do numeru albo nazwy.
            if sack == k or sack == v:
                founde = True

                # Wyświetla znalezionego Pokémona.
                print(f"#{int(k):03d} - {v} found!")

                # Kończy przeszukiwanie po znalezieniu dopasowania.
                break

        # Jeśli po przejrzeniu kolekcji nie było dopasowania,
        # wyświetla komunikat o braku wyniku.
        if not founde:
            print("pokemon not found!")


def delete(col):
    # Pozwala usuwać wiele Pokémonów w jednej sesji.
    while True:
        # Informacja, czy udało się znaleźć wpis do usunięcia.
        founde = False

        # Wyświetla aktualną kolekcję przed wyborem wpisu.
        show(col)

        # Pobiera nazwę lub numer Pokémona do usunięcia.
        sack = input(
            "What pokemon do you wish to delete? "
        ).lower().strip()

        # Wpisanie "back" kończy działanie tej pętli.
        if sack == "back":
            break


        
        # Normalizuje numer wpisany jako tekst.
        if sack.isdigit():
            sack = str(int(sack))

        # Przeszukuje kolekcję w poszukiwaniu numeru lub nazwy.
        for k, v in col.items():
            if sack == k or sack == v:
                founde = True

                # Usuwa element o znalezionym kluczu ze słownika.
                del col[k]

                # Zapisuje zmodyfikowaną kolekcję do pliku.
                saves(col, backup_path)

                # Kończy przeszukiwanie po usunięciu wpisu.
                break

        # Jeśli niczego nie znaleziono, informuje o tym użytkownika.
        if not founde:
            print("pokemon not found!")



        


def info():
    # Główna pętla programu: czeka na kolejne komendy użytkownika.
    while True:
        # Pobiera komendę, usuwa zbędne białe znaki
        # i normalizuje litery do małych.
        pokemon = input("Pokemon?: ").lower().strip()

        # Wczytuje aktualną kolekcję z pliku JSON.
        col = collection()

        # Sortuje kolekcję i zapisuje jej uporządkowaną wersję do pliku.
        
        sort(col)

        # Kończy główną pętlę, jeśli użytkownik wpisze "exit".
        if pokemon == "exit":
            break

        elif pokemon == "":
                    print("nothing entered!")
                    continue
        elif pokemon == "dex":
            dex()

        elif pokemon == "nine_exceptions":
             nine_exceptions()
       

        # Wyświetla liczbę Pokémonów w kolekcji.
        elif pokemon == "count":
            count(col)

        # Wyświetla kolekcję.
        elif pokemon == "show":
            show(col)

        # Uruchamia usuwanie Pokémonów.
        elif pokemon == "delete":
            delete(col)

        # Uruchamia wyszukiwanie w kolekcji.
        elif pokemon == "poke":
            poke(col)

        # Zapisuje kolekcję do pliku backup.json.
        elif pokemon == "save":
            saves(col, backup_path)

        # Pobiera listę wszystkich Pokémonów i zapisuje ją osobno.
        elif pokemon == "getall":
            get_all()

        else:
            # Jeśli użytkownik wpisał numer, normalizuje go do tekstu
            # bez niepotrzebnych zer na początku.
            pokedex = dex()
            if pokemon.isdigit():
                pokemon = str(int(pokemon))
                if int(pokemon) < 1026 and int(pokemon) >= 1:
                    if pokemon not in col:
                                  
                                 col[pokemon] = nine_exceptions(pokedex[pokemon])

                                 
                                 saves(col, backup_path)
                                 print(f"#{int(pokemon):03d} - {col[pokemon]} added")
                                 sort(col)
                                 
                    else: 
                        print(f"{pokedex[pokemon]} already in your collection!")
                else:
                    print("This pokemon does't exist!")
            
            else:
                     
                     papi = False
                     for k, v in pokedex.items():
                         v = nine_exceptions(v)
                         
                         if pokemon == v:
                             papi = True
                             if k not in col:
                                 
                                 col[k] = v
                                 
                                 saves(col, backup_path)
                                 print(f"#{int(k):03d} - {v} added")
                                 sort(col)
                                
                                 break
                             else: 
                                 print(f"{v} already in your collection!") 
                                 
                     if papi == False:
                                     print("This pokemon does't exist!")
                                     


          


# Uruchamia główną funkcję programu.
info()




  