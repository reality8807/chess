class Rook():
    def __init__(self, color: str) -> None:
        self.color = color
        self.white_symbol = "♜"
        self.black_symbol = "♖"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row: int, col: int, board) -> None:
        self.legal_moves = []

        # Left
        for i in range(col-1, -1, -1):
            self.legal_moves.append((row, i))
            if board.array_board[row][i] is not None:
                break

        # Right
        for i in range(col+1, 8):
            self.legal_moves.append((row, i))
            if board.array_board[row][i] is not None:
                break

        # Top
        for i in range(row-1, -1, -1):
            self.legal_moves.append((i, col))
            if board.array_board[i][col] is not None:
                break

        # Bottom
        for i in range(row+1, 8):
            self.legal_moves.append((i, col))
            if board.array_board[i][col] is not None:
                break