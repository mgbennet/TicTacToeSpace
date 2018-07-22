"""TicTacToeSpace.py

Creates a tree of all possible board conditions in tic tac toe.
"""

import copy

renderMap = ['-', 'X', 'O']


class Board:
    def __init__(self, board=[0]*9):
        self.board = board
        self.current_player = 1
        self.winner = -1
        self.best_moves = []

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
        result = [self.make_move(i) for i, val in enumerate(self.board) if val == 0]
        return result

    def has_winner(self):
        if self.player_wins(1):
            return 1
        elif self.player_wins(2):
            return 2
        return 0

    def player_wins(self, player):
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
        result, i = '', 0
        for c in self.board:
            result += renderMap[c] + ' '
            i = (i + 1) % 3
            if i == 0:
                result += "\n"
        return result

    def to_key(self):
        return ''.join(str(i) for i in self.board)


class MoveTree:
    def __init__(self):
        self.root = Board()
        self.tree = [{self.root.to_key(): self.root}]

    def count_nodes(self):
        return sum([len(i) for i in self.tree])

    def play_turn(self, level=0, check_winner=True, filter_transforms=True):
        if len(self.tree) <= level:
            raise IndexError
        if len(self.tree) - 1 == level:
            self.tree.append({})
        for i, board in self.tree[level].items():
            if not (check_winner and board.has_winner()):
                moves = board.all_moves()
                for move in moves:
                    key = move.to_key()
                    if key not in self.tree[level + 1]:
                        if filter_transforms:
                            is_unique = True
                            for j, other_board in self.tree[level + 1].items():
                                if move.equivalent_to(other_board):
                                    is_unique = False
                                    break
                            if is_unique:
                                self.tree[level + 1][key] = move
                        else:
                            self.tree[level + 1][key] = move

    def play_full_game(self, check_winner=True, filter_transforms=True):
        for i in range(9):
            self.play_turn(i, check_winner, filter_transforms)


class MoveTreeNaive:
    def __init__(self):
        self.root = Board()
        self.tree = [[self.root]]

    def count_nodes(self):
        return sum([len(i) for i in self.tree])

    def play_turn(self, level=0, check_winner=True):
        if len(self.tree) <= level:
            raise IndexError
        if len(self.tree) - 1 == level:
            self.tree.append([])
        for board in self.tree[level]:
            if not (check_winner and board.has_winner()):
                moves = board.all_moves()
                for move in moves:
                    self.tree[level + 1].append(move)

    def play_full_game(self, check_winner=True):
        for i in range(9):
            self.play_turn(i, check_winner)


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


def test():
    naive_noearlyout = MoveTreeNaive()
    naive_noearlyout.play_full_game(check_winner=False)
    print("Board states, naive tree, no early out: ", naive_noearlyout.count_nodes())
    print("Last turn, naive tree, no early out:", len(naive_noearlyout.tree[9]))
    naive_checkwinner = MoveTreeNaive()
    naive_checkwinner.play_full_game()
    print("Board states, naive tree, check for winner: ", naive_checkwinner.count_nodes())
    print("Last turn, naive tree, check for winner:", len(naive_checkwinner.tree[9]))

    hashed_noearlyouts = MoveTree()
    hashed_noearlyouts.play_full_game(check_winner=False, filter_transforms=False)
    print("Board states, hashed tree, uncompressed: ", hashed_noearlyouts.count_nodes())
    print("Last turn, hashed tree, uncompressed:", len(hashed_noearlyouts.tree[9]))
    hashed_checkwinner = MoveTree()
    hashed_checkwinner.play_full_game(check_winner=True, filter_transforms=False)
    print("Board states, hashed tree, check for winner: ", hashed_checkwinner.count_nodes())
    print("Last turn, hashed tree, check for winner:", len(hashed_checkwinner.tree[9]))
    hashed_filtertransforms = MoveTree()
    hashed_filtertransforms.play_full_game(check_winner=False, filter_transforms=True)
    print("Board states, hashed tree, filter transforms: ", hashed_filtertransforms.count_nodes())
    print("Last turn, hashed tree, filter transforms:", len(hashed_filtertransforms.tree[9]))
    hashed_fullcompressed = MoveTree()
    hashed_fullcompressed.play_full_game(check_winner=True, filter_transforms=True)
    print("Board states, hashed tree, fully compressed: ", hashed_fullcompressed.count_nodes())
    print("Last turn, hashed tree, fully compressed:", len(hashed_fullcompressed.tree[9]))
    # ties = [b for i, b in t.tree[9].items() if b.has_winner() == 0]
    # print("Number of ties: ", len(ties))
    # for t in ties:
    #     print(t.to_string())


test()
