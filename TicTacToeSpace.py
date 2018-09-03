"""TicTacToeSpace.py

Creates a tree of all possible board conditions in tic tac toe.
"""

import copy

renderMap = ['-', 'X', 'O']


class Board:
    def __init__(self, board=[0]*9):
        self.board = board
        self.current_player = 1
        self.child_boards = []
        self.winner = -1       # -1 is placeholder, 0 is tie, 1 or 2 mean that player will win
        self.best_moves = []   # moves that have the best outcomes. indices of self.child_boards

    def make_move(self, i):
        """Returns a new board with the current player playing at index i"""
        if self.board[i] == 0:
            next_board = Board(copy.deepcopy(self.board))
            next_board.board[i] = self.current_player
            next_board.current_player = self.current_player % 2 + 1
            return next_board
        else:
            raise IndexError

    def all_moves(self):
        """Generates a list of board states that the current player can generate with a move"""
        result = [self.make_move(i) for i, val in enumerate(self.board) if val == 0]
        return result

    def has_winner(self):
        """Checks if a player has won"""
        if self.player_wins(1):
            return 1
        elif self.player_wins(2):
            return 2
        return 0

    def player_wins(self, player):
        """Checks if player wins on this board"""
        # horizontals
        for row in [self.board[i:i+3] for i in range(0, len(self.board), 3)]:
            if row == [player]*3:

                return True

        # verticals
        for i in range(3):
            if [self.board[j] for j in range(i, len(self.board), 3)] == [player]*3:
                return True

        # diagonals
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True

        return False

    def equivalent_to(self, other_board):
        """Checks if other_board can be rotated or flipped to match this board"""
        flipped = flip_board(other_board)
        if other_board.board == self.board \
                or rot_board_ccw(other_board).board == self.board \
                or reverse_board(other_board).board == self.board \
                or rot_board_cw(other_board).board == self.board \
                or flipped.board == self.board \
                or rot_board_ccw(flipped).board == self.board \
                or reverse_board(flipped).board == self.board \
                or rot_board_cw(flipped).board == self.board:
            return True
        return False

    def to_string(self):
        """Returns an ASCII art version of the current board"""
        result, i = '', 0
        for c in self.board:
            result += renderMap[c] + ' '
            i = (i + 1) % 3
            if i == 0:
                result += "\n"
        return result

    def key(self):
        """Generates string representing board state"""
        return ''.join(str(i) for i in self.board)

    def transform_key(self):
        """Generates string representing the board state. Boards which can be transformed into each
        other will generate the same key"""
        flipped = flip_board(self)
        equivalent_boards = [
            self.key(),
            rot_board_ccw(self).key(),
            reverse_board(self).key(),
            rot_board_cw(self).key(),
            flipped.key(),
            rot_board_ccw(flipped).key(),
            reverse_board(flipped).key(),
            rot_board_cw(flipped).key()
        ]
        return max(equivalent_boards)


class MoveTree:
    def __init__(self, check_winner=True, filter_transforms=True, num_levels=9):
        self.root = Board()
        self.tree = [{self.root.key(): self.root}]
        self.check_winner = check_winner
        self.filter_transforms = filter_transforms
        for i in range(num_levels):
            self.play_turn(i)

    def count_nodes(self):
        return sum([len(i) for i in self.tree])

    def play_turn(self, level=0):
        if len(self.tree) <= level:
            raise IndexError
        if len(self.tree) - 1 == level:
            self.tree.append({})
        for i, board in self.tree[level].items():
            if not (self.check_winner and board.has_winner()):
                moves = board.all_moves()
                child_moves = {}
                for move in moves:
                    if self.filter_transforms:
                        key = move.transform_key()
                    else:
                        key = move.key()
                    self.tree[level + 1][key] = move
                    child_moves[key] = self.tree[level + 1][key]
                board.child_boards = list(child_moves.values())


class MoveTreeNaive:
    def __init__(self, check_winner=True, num_levels=9):
        self.root = Board()
        self.tree = [[self.root]]
        self.check_winner = check_winner
        for i in range(num_levels):
            self.play_turn(i)

    def count_nodes(self):
        return sum([len(i) for i in self.tree])

    def play_turn(self, level=0):
        if len(self.tree) <= level:
            raise IndexError
        if len(self.tree) - 1 == level:
            self.tree.append([])
        for board in self.tree[level]:
            if not (self.check_winner and board.has_winner()):
                moves = board.all_moves()
                for move in moves:
                    self.tree[level + 1].append(move)
                    board.child_boards.append(move)


def rot_board_cw(b):
    """Rotates the board 90 degrees clockwise and returns a new board"""
    result = []
    for i in range(3):
        result.append(b.board[i + 6])
        result.append(b.board[i + 3])
        result.append(b.board[i])
    return Board(result)


def rot_board_ccw(b):
    """Rotates the board 90 degrees counter clockwise and returns a new board"""
    result = []
    for i in range(2, -1, -1):
        result.append(b.board[i])
        result.append(b.board[i + 3])
        result.append(b.board[i + 6])
    return Board(result)


def reverse_board(b):
    """Reverses the board listings and returns a new board. Equivalent to a 180 degree rotation"""
    return Board(b.board[::-1])


def flip_board(b):
    """Flips the board over the y axis and returns a new board"""
    rows = [b.board[i:i+3] for i in range(0, len(b.board), 3)]
    new_board = [item for sublist in rows for item in sublist[::-1]]
    return Board(new_board)


def main():
    naive_noearlyout = MoveTreeNaive(check_winner=False)
    print("Board states, naive tree, no early out: ", naive_noearlyout.count_nodes())
    print("Last turn, naive tree, no early out:", len(naive_noearlyout.tree[9]))
    naive_checkwinner = MoveTreeNaive()
    print("Board states, naive tree, check for winner: ", naive_checkwinner.count_nodes())
    print("Last turn, naive tree, check for winner:", len(naive_checkwinner.tree[9]))

    hashed_noearlyouts = MoveTree(check_winner=False, filter_transforms=False)
    print("Board states, hashed tree, uncompressed: ", hashed_noearlyouts.count_nodes())
    print("Last turn, hashed tree, uncompressed:", len(hashed_noearlyouts.tree[9]))
    hashed_checkwinner = MoveTree(check_winner=True, filter_transforms=False)
    print("Board states, hashed tree, check for winner: ", hashed_checkwinner.count_nodes())
    print("Last turn, hashed tree, check for winner:", len(hashed_checkwinner.tree[9]))
    hashed_filtertransforms = MoveTree(check_winner=False, filter_transforms=True)
    print("Board states, hashed tree, filter transforms: ", hashed_filtertransforms.count_nodes())
    print("Last turn, hashed tree, filter transforms:", len(hashed_filtertransforms.tree[9]))
    hashed_fullcompressed = MoveTree(check_winner=True, filter_transforms=True)
    print("Board states, hashed tree, fully compressed: ", hashed_fullcompressed.count_nodes())
    print("Last turn, hashed tree, fully compressed:", len(hashed_fullcompressed.tree[9]))
    # ties = [b for i, b in t.tree[9].items() if b.has_winner() == 0]
    # print("Number of ties: ", len(ties))
    # for t in ties:
    #     print(t.to_string())


if __name__ == '__main__':
    main()
