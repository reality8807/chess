class King():
    def __init__(self, color):
        self.color = color
        self.white_symbol = "♚"
        self.black_symbol = "♔"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
        self.legal_moves = []
        moves = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]

        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:
                self.legal_moves.append((r, c))
