# TicTacToeSpace

A [game tree](https://en.wikipedia.org/wiki/Game_tree) can be a brute force method of creating game AI. A game tree graphs the connections between the game states that are possible to achieve through play. If you've ever played a game and though ahead a few turns, like "If I move to A, then my opponent can do X, Y, or Z, but she'll probably play Y, in which case I'll play B...", you've constructed a mental partial game tree. A complete game tree starts from the initial board state and includes every achievable board state. And once you have a complete game tree, you can "solve" a game by determining perfect play from any position.

I was curious about the nature of tic-tac-toe's game tree, since nearly every book on AI mentions that it is trivial to solve in compraison to a real game like chess or go. And it's true, go has more permutations in the first three moves then tic-tac-toe does in the entire tree. But there are some lessons to be learned about calculating game trees, and I'd like to share them here.

#### The naive approach
Let's try to get an idea about the overall size of the tree before we simulate it. From the intial board state, player 1 (we'll say X goes first) has 9 possible moves. Each of these board states gives the second player 8 possible moves, for a total of 9 * 8 or 72 board states possible on turn two. Then each of those board states has 7 possible replies, for 9 * 8 * 7 = 504 possible states. Continuing this pattern, and ignoring branches ending early from a win, this means we will have 9 + 9 * 8 + 9 * 8 * 7 + ... + 9!, plus one more for the initial board state, for a total of 986410 nodes in our game tree. Even on 20 year old hardware that's not an unmanagable number of board states, but it is a fairly large tree.

And even when we simulate out the game tree using the code in this repo and check for winners, the tree still has 549946 nodes.

#### Total possible unique boards

But wait a minute, let's do a little more math. We can quickly calculate the total number of unique boards where each square in a 3 by 3 grid is either an X, an O, or empty: 3<sup>9</sup>, or 19683. And this is another over estimate, since it will include board states that can never be achieved legally in a game, like boards with 6 or more X's or where O has more squares than X (which can't happen because X goes first).

#### Smarter structure

So clearly we're repeating ourselves a lot with the naive method. For example:
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
but our naive method builds two seperate but identical branches for each.

So let's use dictionaries, like a good pythonista. I keep a list of dictionaries, one for each turn, and as calculate new moves, I add them to the appropriate dictionary, assuming it isn't in there already. This gives a tree with 5478 nodes, or 6046 if we don't check for winners and play all the way until the board is full. Much, much better! Additionally this tree calculates in a fraction of the time.

#### Check for equivilent boards

But there's another thing that can help reduce the size of the tree. Many board states are equivilent to each other, as they are rotations or flips of other boards. For example, on the first move, playing in the upper left is equivilent to playing in any other corner. So instead of 9 moves on the first turn, the first player is effectively choosing from 3 moves: a corner space, a side space, or the middle space.

|                 | Dont filter transforms | Filter transforms |
| --------------- | ----------------------:| -----------------:|
| No check winner |                   6046 |               850 |
| Check winner    |                   5478 |               765 |
