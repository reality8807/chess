class Pawn():
    def __init__(self, color: str) -> None:
        self.first_time = True

        self.color = color
        self.white_symbol = "♟︎"
        self.black_symbol = "♙"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row: int, col: int, board) -> None:
        self.legal_moves = []
        if self.color == "white":
            if row == 6 and board.array_board[4][col] is None and board.array_board[3][col] is None:
                self.legal_moves.append((4, col))
            if row != 0:
                if board.array_board[row-1][col] is None:
                    self.legal_moves.append((row-1, col))
                if col > 0 and board.array_board[row-1][col-1] is not None:
                    self.legal_moves.append((row-1, col-1))
                if col < 7 and board.array_board[row-1][col+1] is not None:
                    self.legal_moves.append((row-1, col+1))
        else:
            if row == 1 and board.array_board[3][col] is None and board.array_board[2][col] is None:
                self.legal_moves.append((3, col))
            if row != 7:
                if board.array_board[row+1][col] is None:
                    self.legal_moves.append((row+1, col))
                if col > 0 and board.array_board[row+1][col-1] is not None:
                    self.legal_moves.append((row+1, col-1))
                if col < 7 and board.array_board[row+1][col+1] is not None:
                    self.legal_moves.append((row+1, col+1))