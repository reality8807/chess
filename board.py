from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
from pieces.pawn import Pawn


class Board:
    def __init__(self) -> None:
        self.array_board = [
            [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")],
            [Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")],
            [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]
        ]

    def print_board(self) -> None:
        num = 8
        border = '─'

        # Top Border
        print('  ┌', end='')
        print(border * 39, end='')
        print('┐')

        for i, row in enumerate(self.array_board):
            print(f'{num} │ ', end='')

            # Vertical Lines
            for column in row:
                if column is None:
                    print(" ", end='  │ ')
                else:
                    print(column.symbol, end='  │ ')
            print()

            # Horizontal Lines
            if i != len(self.array_board) - 1:
                print('  ├', end='')
                print(border * 39, end='')
                print('┤')

            num -= 1

        # Bottom Border
        print('  └', end='')
        print(border * 39, end='')
        print('┘')

        # Letters
        print('    a    b    c    d    e    f    g    h')
