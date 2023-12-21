# PIPR 23Z Gra Konsolowa W Pokera 

## Treść Zadania: 
Celem projektu jest zaimplementowanie gry w pokera w odmianie Texas Hold'em.

Powinna być możliwość gry jednoosobowej przeciwko wielu graczom komputerowym. Gra komputera powinna cechować się decyzjami zwiększającymi prawdopodobieństwo wygranej komputera. Nie musi być to optymalny model decyzji, ale powinien być zauważalnie lepszy niż losowe decyzje.

## Wstępne opisy klas używanych w projekcie: 

1. **`Game`**
- Zawiera Interface za pomocą którego gracz będzie komunikował się z Grą. Będzie zawierać podstawowe metody typu: "graj", "Zakoncz gre". Kontroluje przebieg całej rozgrywki.
2. **`Player`**
- Jest podstawową reprezentacją gracza:
    - Atrybuty: Nazwa, Ilość punktów, Posiadane Karty
    - Metody: Używanie kart