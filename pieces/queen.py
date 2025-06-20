from pieces.rook import Rook
from pieces.bishop import Bishop


class Queen():
    def __init__(self, color: str) -> None:
        self.color = color
        self.white_symbol = "♛"
        self.black_symbol = "♕"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row: int, col: int, board) -> None:
        self.legal_moves = []

        # Rook logic
        temp_rook = Rook(self.color)
        temp_rook.get_legal_moves(row, col, board)
        self.legal_moves.extend(temp_rook.legal_moves)

        # Bishop logic
        temp_bishop = Bishop(self.color)
        temp_bishop.get_legal_moves(row, col, board)
        self.legal_moves.extend(temp_bishop.legal_moves)
