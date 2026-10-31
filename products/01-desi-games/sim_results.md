# Simulation results (generated)

## Cricket Dhamaka

```
[[["0", "0", "1", "1", "1", "2"], ["0", "0", "1", "1", "1", "2"], ["0", "2", "2", "2", "2", "2"]], [["0", "0", "1", "1", "2", "4"], ["0", "2", "4", "4", "4", "4"], ["0", "0", "0", "0", "2", "W"]], [["0", "1", "1", "4", "6", "W"], ["1", "4", "6", "W", "W", "W"], ["0", "0", "6", "6", "6", "W"]]]
equilibrium batter mix [0.34, 0.34, 0.32] bowler mix [0.46, 0.22, 0.32]
mean 2-over score 16.8, all-out rate 32%, dominated strategy: False
```

## Ganit Ladder

| Players | Answer accuracy | Mean turns per player | 90th percentile | First-player win rate (fair = 1/players) |
|---|---|---|---|---|
| 2 | 50% | 35.0 | 62 | 50.6% (fair 50.0%) |
| 2 | 80% | 29.9 | 52 | 50.8% (fair 50.0%) |
| 2 | 100% | 26.6 | 46 | 51.1% (fair 50.0%) |
| 3 | 50% | 28.3 | 47 | 33.9% (fair 33.3%) |
| 3 | 80% | 24.0 | 39 | 34.0% (fair 33.3%) |
| 3 | 100% | 21.7 | 36 | 33.5% (fair 33.3%) |
| 4 | 50% | 24.4 | 39 | 25.0% (fair 25.0%) |
| 4 | 80% | 21.0 | 33 | 26.4% (fair 25.0%) |
| 4 | 100% | 19.1 | 30 | 26.2% (fair 25.0%) |

Head to head, 90 % accurate vs 50 % accurate player (first move alternated): the better mathematician wins 58.8% of games.

PASS : game length 18-45 turns, first-player advantage < 6 points, and the better mathematician wins 58-78 %

## Sabzi Mandi

House rule: once per sale the shopkeeper may break one note at the bank. With it, change could not be made in 2.7% of 20,000 simulated sales in shifts of 12 (the bank rule was needed in 1.1% of sales) with the starting till (Rs 20 x1, 10 x3, 5 x6, 2 x10, 1 x12); purchases are capped at Rs 45 and customers pay with the smallest note of 5/10/20/50 that covers the bill.
PASS : change failure rate < 5 %

## Unit economics

| Game | Price Rs | BOM guess Rs | Contribution Rs | Margin | Margin if BOM +30 % |
|---|---|---|---|---|---|
| Cricket Dhamaka (card game) | 499 | 90 | 228 | 48% | 41% |
| Ganit Ladder (board + table cards) | 799 | 150 | 375 | 49% | 42% |
| India Yatra (quiz cards, 3 language decks) | 599 | 110 | 284 | 50% | 43% |
| Sabzi Mandi (items + money + tray) | 799 | 180 | 340 | 45% | 36% |
