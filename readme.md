# TicTacToeSpace

A [game tree](https://en.wikipedia.org/wiki/Game_tree) can be a brute force method of creating game AI. A game tree graphs the connections between the game states that are possible to achieve through play. Thinking a few turns ahead in a game, like "If I move to A, then my opponent can do X, Y, or Z, but she'll probably play Y, in which case I'll play B...", is basically creating a partial game tree in your mind. A complete game tree starts from the initial board state and includes every achievable board state. And once you have a complete game tree, you can "solve" a game (determine perfect play from any position) using a [minamax](https://en.wikipedia.org/wiki/Minimax) decision algorithm.

I was curious about the nature of tic-tac-toe's game tree, since nearly every book on AI mentions that it is trivial to solve in comparison to a real game like chess or go. After all, go has more possible board states in the first three moves then tic-tac-toe does in the entire tree. But there are some lessons to be learned by calculating game trees, especially regarding data structure efficiency.

#### The naive approach
Let's try to get an idea about the overall size of the tree before we simulate it. From the initial board state, player 1 (we'll say X goes first) has 9 possible moves. Each of these board states gives the second player 8 possible moves, for a total of 9 * 8 or 72 board states possible on turn two. Then each of those board states has 7 possible replies, for 9 * 8 * 7 = 504 possible states. Continuing this pattern, and ignoring branches ending early from a win, this means we will have 9 + 9 * 8 + 9 * 8 * 7 + ... + 9!, plus one more for the initial board state, for a total of 986410 nodes in our game tree. Even on 30 year old hardware that's not an unmanageable number of board states, but it is a fairly large tree.

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
but our naive method builds two separate but identical branches for each.

So let's use dictionaries, using a string derived from the board state as the board's key. I keep a list of dictionaries, one for each turn, and as new moves are calculated, I add them to that turn's dictionary, assuming it isn't in there already. This gives a tree with 5478 nodes, or 6046 if we don't check for winners and play all the way until the board is full. Much, much better! Additionally this tree is built in a fraction of the time.

#### Check for equivalent boards

But there's another thing that can help reduce the size of the tree. Many board states are equivalent to each other, as they are rotations or flips of other boards. For example, each of the following board states are equivalent to each other:
```
X - -      - - -      - O X     - - X
O - -      O - -      - - -     - - O
- - -      X - -      - - -     - - -
```
So instead of 9 moves on the first turn, the first player is effectively choosing from 3 moves: a corner space, a side space, or the middle space. With this method and the dictionary method above, we can get the game tree down to a mere 765 nodes.

#### Total board states

For a naively generated tree:

|                  | Don't filter transforms | Filter transforms |
| ---------------- | -----------------------:| -----------------:|
| No winner check  |                  986410 |            101648 |
| Check for winner |                  549946 |             58524 |

For a tree with no redundant board states:

|                  | Don't filter transforms | Filter transforms |
| ---------------- | -----------------------:| -----------------:|
| No winner check  |                    6046 |               850 |
| Check for winner |                    5478 |               765 |
