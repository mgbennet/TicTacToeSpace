# TicTacToeSpace

Most books on AI mention in the first 50 pages that tic tac toe is a stupid game for babies in part because its [game tree](https://en.wikipedia.org/wiki/Game_tree) (a sort of map of possible move sets branching from a board state) is piddling in comparison to games like chess, go, or even checkers. Even ancient computers with comically limited memory can calculate the entire tree if they're a little clever about it.

But how small is the tree exactly? How many legal board states exist? I'd like to walk through how one might go about answering these questions.

#### Total unique boards
To start, let's see if we can approximate the game tree's size with some math. We can quickly calculate the total number of unique boards where each square in a 3 by 3 grid is either an X, an O, or empty. This is simply 3<sup>9</sup>, or 19683. However we can quickly realize that most of these board states will never be achieved in a game of tic tac toe, as they include boards with multiple three-in-a-row's, or where O has more spaces that X (which can't happen because X goes first).

#### Failing with factorials
Ok, so let's try some different math. On her first turn, X has 9 moves available to her. On the next, O has eight, and so on. So 9 * 8 * 7 *... * 2 * 1, or 9!, is 362880. Obviously something isn't right about this calculation.

Besides the issue of games ending early when someone wins, many of these board states are identical to others. For example:
```
X - -      X - -      X - -
- - -  =>  O - -  =>  O X -
- - -      - - -      - - -
```
has an identical board state on turn three as
```
- - -      - - -      X - -
- X -  =>  O X -  =>  O X -
- - -      - - -      - - -
```
but our naive factorial method will not merge these two paths together and we end up calculating that there are more game boards on the tree then there are unique boards.

#### Simulate play

So lets actually simulate the game and see what we see. I've made a program that calculates any available moves given a board and a player, allow