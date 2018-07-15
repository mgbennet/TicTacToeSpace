# TicTacToeSpace

This project started because nearly every book on AI mentions in the first 50 pages that tic tac toe is a dumb game for babies in part because its [game tree](https://en.wikipedia.org/wiki/Game_tree) (a sort of map of possible move sets branching from a board state) is piddling in comparison to games like chess, go, or even checkers.

So I wanted to know how big that tree actually is. And it turns out that it sort of depends on how you calculate it.

#### What the hell I'm trying to look at here

I'm trying

Each node on the game tree is a board state that can be achieved through legal play of the game. The root node an empty board. A node's branches are the board states that the current player's move can result in.

The rules of tic tac toe imply several things about the tree. The game can only last a maximum of 9 moves, and steadily progresses towards either a win for either player, or a tie.

#### Total possible unique boards

To start, let's see if we can approximate the game tree's size with some math. We can quickly calculate the total number of unique boards where each square in a 3 by 3 grid is either an X, an O, or empty. This is simply 3<sup>9</sup>, or 19683. However we can quickly realize that most of these board states will never be achieved in a game of tic tac toe, as they include boards with multiple three-in-a-row's, or where O has more spaces that X (which can't happen because X goes first).

#### Failing with factorials
Ok, so let's try some different math. On her first turn, X has 9 moves available to her. On the next, O has eight, and so on. On the 9th turn, it's 9 * 8 * 7 *... * 2 * 1, or 9!, is 362880. So the total number of nodes in the tree is 9 + 9 * 8 + 9 * 8 * 7 + ... + 9!, plus one more for the initial board state, for a total of 986410. Now this is many times the number of possible states we calculated in the previous step.

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

So let's actually simulate the game and see what we see. The TicTacToeSpace.py script can generate a game tree in several ways. The simplest is just to