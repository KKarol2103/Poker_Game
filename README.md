# PIPR 23Z Gra Konsolowa W Pokera 

## Treść Zadania: 
Celem projektu jest zaimplementowanie gry w pokera w odmianie Texas Hold'em.

Powinna być możliwość gry jednoosobowej przeciwko wielu graczom komputerowym. Gra komputera powinna cechować się decyzjami zwiększającymi prawdopodobieństwo wygranej komputera. Nie musi być to optymalny model decyzji, ale powinien być zauważalnie lepszy niż losowe decyzje.

## Koncepcja:
W mojej realizacji projektu postanowiłem położyć duży nacisk na programowanie obiektowe - w związku z tym przedstawiam poniżej koncepcję kilku klas które chciałbym zaimplementować w mojej grze. Ponieważ jest to jednak koncepcja, finalna wersja projektu może się delikatnie różnić w niektórych aspektach. Byłbym bardzo wdzięczny za ewentualne uwagi/sugestie odnośnie projektu.

## Wstępne opisy klas używanych w projekcie: 

1. **`Game`**
- Zawiera Interface za pomocą którego gracz będzie komunikował się z Grą. Będzie zawierać podstawowe metody typu: "play", "quit".
2. **`Player`**
- Jest podstawową reprezentacją gracza:
    - Atrybuty: Nazwa, Ilość punktów, Posiadane Karty
    - Metody: Czynności związane z grą w Pokera: fold, call, raise itd.
3. **`AIPlayer`** 
    (dziedziczy po Player)
    - Specjalizacja klasy Player dla przeciwników sterowanych przez komputer.
    -Metody: podejmowanie decyzji analizując obecny stan gry bazując na zaimplementowanych algorytmach.
     **Tutaj pojawia się jeden z moich głównych problemów - nie wiem do końca jaki powinien być stopień zaawansowania tych algorytmów i co dokładnie rozumiemy przez "algorytm zauważalnie lepszy niż losowe decyzje". W jaki sposób mógłbym testować skuteczność zaimplementowanych przeze mnie algorytmów i stwierdzić który z nich jest najlepszy i który najlepiej zaimplementować w finalnej wersji?**

4. **`Card`**
    - Reprezentacja pojedynczej karty
    - Zawiera jej kolor oraz wartość, (bądź figurę) np. Card("Jack", "Trefl") 
    - Zastanawiam się nad możliwością zawarcia tych Kolorów/figur w Enumach, dzięki czemu nie trzeba by było podawać do konstruktora Stringów oraz kod ogółem wyglądałby lepiej. Czy jest to dobre rozwiązanie?

5. **`Deck`**
    - Atrybuty: Zawiera zbiór kart używanych w grze oraz podstawowe schematy układów kart (poker, street itd.)
    - Metody: Możemy za jej pomocą tasować karty w grze a także rozdawać je graczom

6. **`Table`**
    - Reprezentuje stół - główne miejsce gdzie toczy się gra.
    - Zawiera informacje jakie karty aktualnie znajdują się na stole oraz żetony a także stawkę w obecnej grze.
    - Będzie to metoda bardzo przydatna przy wyświetlaniu na ekranie użytkownika aktualnego stanu gry.

## Ogólnie całościowo rozgrywkę wyobrażam sobie w taki sposób:
1. Najpierw tworzona jest instancja klasy game - na której wywołujemy metodę odpowiadającą za rozpoczęcie gry.
2. Użytkownik podaje liczbę graczy uczestniczących w grze - standardowe input.
3. Na podstawie danych tworzone są instancje klasy AIPlayer z którymi gracz będzie grał w pokera.
4. Potem już rozpoczyna się standardowa rozgrywka w pokera - gra trwa do tego momentu aż któryś z graczy:
    1. Nie zbankrutuje
    2. Zakończyła się ostatnia runda licytacji
    3. Wszyscy gracze poza jednym spasowali
5. Po zakończeniu rozgrywki gracz może zdecydować czy chce zagrać jeszcze raz, czy może już zakończyć grę (wywołanie metody "quit" - która będzie prawdopodobnie robiła po prostu break z jakiejś pętli)
