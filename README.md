# Program do automatyzacji analizy logów z symulatora jazdy

Ten program służy do automatyzacji analizy danych pochodzących z badań przeprowadzanych w symulatorze jazdy. Wyniki dotyczą pomiaru czasu reakcji kierowcy przy różnych zdarzeniach, m.in. przeszkodach na drodze czy obecności reklam LED.

## Jak używać 

1. **Pobierz repozytorium**  
    Sklonuj repozytorium na swój komputer za pomocą polecenia:  
    ```bash
    git clone <URL_REPOZYTORIUM>
    cd <NAZWA_FOLDERU_REPOZYTORIUM>
    ```

2. **Zainstaluj wymagane zależności**  
    Upewnij się, że masz zainstalowanego Pythona (wersja 3.7 lub nowsza). Następnie zainstaluj wymagane pakiety:  
    ```bash
    pip install -r requirements.txt
    ```

3. **Uruchom analizę**  
    Wykonaj skrypt `report_maker.py`:  
    ```bash
    python report_maker.py
    ```
    Wybierz plik do analizy i miejsce zapisu wyników.

4. **Sprawdź wyniki**  
    Po zakończeniu działania programu, wyniki analizy zostaną zapisane w pliku `raport.csv` w wybranym folderze.


## Jak działa
1. W pliku *report_maker.py* wczytywany jest log (np. *test2.txt*) i pomijane są pierwsze linie informacji ogólnych (np. data, opis trasy).
2. Następnie, program analizuje wpisy czasowe w formacie `hh:mm:ssSSS` (np. `0:10:453`) i na ich podstawie wylicza czasy reakcji (funkcje `time_to_ms` oraz `time_diff`).
3. Program wyłapuje w logach zdarzenia, takie jak:
   - **Znak ograniczenie predkosci** i **Znak konca ograniczenia predkosci**  
   - **Przekroczona predkosc**  
   - **Przeszkoda** (np. *Pies*, *Pieszy*, *Pilka na ziemi*)  
   - **Kolizja** (np. *- otoczenie*, *- przeszkoda*)  
   - **Hamowanie** przekraczające próg i **Skrecenie kierownicy** przekraczające próg  
   - **LED ON Reklama** lub **LED OFF**  
4. Na koniec, tworzone jest podsumowanie (zliczane są kolizje, wyliczany jest całkowity czas przejazdu) i generowany jest raport pokazujący, jak poszczególne zdarzenia wpływały na czasy reakcji, w tym zdarzenia związane z reklamami LED.

## Przyład utworzonego raporu

PODSUMOWANIE WYNIKÓW SYMULACJI

czas reakcji [ms],rodzaj przeszkody,grupa reklam,rodzaj reakcji,kolizja z przeszkodą
700,Przeszkoda Pieszy w miejscu,-,Hamowanie przekroczylo prog,nie
800,Przeszkoda Pies w miejscu,-,Hamowanie przekroczylo prog,nie
1049,Przeszkoda Pies w miejscu,D,Hamowanie przekroczylo prog,nie
833,Przeszkoda Pilka na ziemi,-,Hamowanie przekroczylo prog,nie
966,Przeszkoda Pies w miejscu,C,Skrecenie kierownicy przekroczylo prog,nie
983,Przeszkoda Pieszy w miejscu,C,Skrecenie kierownicy przekroczylo prog,nie
983,Przeszkoda Pies w miejscu,B,Skrecenie kierownicy przekroczylo prog,tak
866,Przeszkoda Pies w miejscu,A,Skrecenie kierownicy przekroczylo prog,nie
750,Przeszkoda Pieszy w miejscu,-,Hamowanie przekroczylo prog,nie

czas przejazdu [ms]:,316168
liczba kolizji z przeszkodą:,1
liczba kolizji z otoczeniem:,1
liczba przekroczeń prędkości:,9

