class Bishop():
    def __init__(self, color: str) -> None:
        self.color = color
        self.white_symbol = "♝"
        self.black_symbol = "♗"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row: int, col: int, board) -> None:
        self.legal_moves = []

        # Top Left
        i = 1
        while row-i >= 0 and col-i >= 0:
            self.legal_moves.append((row-i, col-i))
            if board.array_board[row-i][col-i] is not None:
                break
            i += 1

        # Bottom Left
        i = 1
        while row+i < 8 and col-i >= 0:
            self.legal_moves.append((row+i, col-i))
            if board.array_board[row+i][col-i] is not None:
                break
            i += 1

        # Top Right
        i = 1
        while row-i >= 0 and col+i < 8:
            self.legal_moves.append((row-i, col+i))
            if board.array_board[row-i][col+i] is not None:
                break
            i += 1

        # Bottom Right
        i = 1
        while row+i < 8 and col+i < 8:
            self.legal_moves.append((row+i, col+i))
            if board.array_board[row+i][col+i] is not None:
                break
            i += 1