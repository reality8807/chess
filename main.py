class Game:
    def __init__(self):
        self.board = Board()
        self.board.print_board()

        self.letter_conversion = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        self.white_pieces = ["♟︎", "♜", "♞", "♝", "♛", "♚"]
        self.black_pieces = ["♙", "♖", "♘", "♗", "♕", "♔"]

        self.turn = "white"
        self.choosable_pieces = self.white_pieces

    def logic(self):
        while True:
            # Initial Input
            self.get_initial_input()

            if self.initial_selected_piece is None:
                print("Invalid Input, select a piece\n")
                continue
            elif self.initial_selected_piece.symbol not in self.choosable_pieces:
                print(f"Select a {self.turn} piece\n")
                continue

            # Final Input
            self.get_final_input()
            if self.final_selected_piece is not None:
                if self.final_selected_piece.symbol in self.choosable_pieces:
                    print("You cannot attack you own piece.\n")
                    continue

            self.initial_selected_piece.get_legal_moves(self.initial_row, self.initial_col, self.board)

            if self.final_selected_pos not in self.initial_selected_piece.legal_moves:
                print("Illegal move, try again")
                continue

            if self.is_check():
                continue

            self.board.print_board()
            self.switch_player()

    def get_initial_input(self):
        initial_move = input("Enter Initial Move: ")
        if initial_move == "exit":
            exit()
        try:
            self.initial_row = 8-int(initial_move[1])
            self.initial_col = self.letter_conversion.get(initial_move[0])

            self.initial_selected_pos = (self.initial_row, self.initial_col) 
            self.initial_selected_piece = self.board.array_board[self.initial_row][self.initial_col]
        except:
            print("Invalid Move\n")
            self.get_initial_input()

    def get_final_input(self):
        final_move = input("Enter Final Move: ")
        if final_move == "exit":
            exit()
        try:
            self.final_row = 8-int(final_move[1])
            self.final_col = self.letter_conversion.get(final_move[0])

            self.final_selected_pos = (self.final_row, self.final_col)
            self.final_selected_piece = self.board.array_board[self.final_row][self.final_col]
        except:
            print("Invalid Move\n")
            self.get_final_input()

    def switch_player(self):
        if self.turn == "white":
            self.turn = "black"
            self.choosable_pieces = self.black_pieces
        else:
            self.turn = "white"
            self.choosable_pieces = self.white_pieces

    def is_check(self):
        temp_final_piece = self.board.array_board[self.final_row][self.final_col]

        # Make the move made by user
        self.board.array_board[self.initial_row][self.initial_col] = None
        self.board.array_board[self.final_row][self.final_col] = self.initial_selected_piece

        # Find own king's position
        for row in range(0, 8):
            for piece in range(0, 8):
                if self.board.array_board[row][piece] is not None:
                    if self.turn == "white":
                        if self.board.array_board[row][piece].symbol == "♚":
                            king_pos = (row, piece)
                            break
                    else:
                        if self.board.array_board[row][piece].symbol == "♔":
                            king_pos = (row, piece)
                            break

        # Check if king is in check
        for row in range(0, 8):
            for piece in range(0, 8):
                if self.board.array_board[row][piece] is not None:
                    if self.board.array_board[row][piece].symbol not in self.choosable_pieces:
                        self.board.array_board[row][piece].get_legal_moves(row, piece, self.board)
                        if king_pos in self.board.array_board[row][piece].legal_moves:
                            print("you cannot play this move, your king is still in check!")
                            # Undo the move made by user
                            self.board.array_board[self.initial_row][self.initial_col] = self.initial_selected_piece
                            self.board.array_board[self.final_row][self.final_col] = temp_final_piece
                            return True

        # Find opponent king's position
        for row in range(0, 8):
            for piece in range(0, 8):
                if self.board.array_board[row][piece] is not None:
                    if self.turn == "white":
                        if self.board.array_board[row][piece].symbol == "♔":
                            king_pos = (row, piece)
                            break
                    else:
                        if self.board.array_board[row][piece].symbol == "♚":
                            king_pos = (row, piece)
                            break

        # Check if opponent's king is in check
        for row in range(0, 8):
            for piece in range(0, 8):
                if self.board.array_board[row][piece] is not None:
                    if self.board.array_board[row][piece].symbol in self.choosable_pieces:
                        self.board.array_board[row][piece].get_legal_moves(row, piece, self.board)
                        if king_pos in self.board.array_board[row][piece].legal_moves:
                            if self.is_checkmate(king_pos[0], king_pos[1]):
                                print("Checkmate!")
                                print(f"{self.turn} won the game")
                                self.board.print_board()
                                exit()
                            print("CHECK!")
                            return False
        return False

    def is_checkmate(self, king_pos_row, king_pos_col):
        checkmate = True

        # 1. Check if king can move to another place

        # Find all possible places the king can go
        self.board.array_board[king_pos_row][king_pos_col].get_legal_moves(king_pos_row, king_pos_col, self.board)
        for r, c in self.board.array_board[king_pos_row][king_pos_col].legal_moves:
            if self.board.array_board[r][c] is not None:
                if self.board.array_board[r][c].symbol not in self.choosable_pieces:
                    continue
            # Temporary move
            captured = self.board.array_board[r][c]
            self.board.array_board[r][c] = self.board.array_board[king_pos_row][king_pos_col]
            self.board.array_board[king_pos_row][king_pos_col] = None
            not_valid_move = False

            # Check if king can avoid check
            for row in range(0, 8):
                for col in range(0, 8):
                    if self.board.array_board[row][col] is not None:
                        if self.board.array_board[row][col].symbol in self.choosable_pieces:
                            self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                            if (r, c) in self.board.array_board[row][col].legal_moves:
                                not_valid_move = True
                                break
                if not_valid_move:
                    break

            # Undo the temporary move
            self.board.array_board[king_pos_row][king_pos_col] = self.board.array_board[r][c]
            self.board.array_board[r][c] = captured
            if not not_valid_move:
                checkmate = False
                break

        if checkmate:
            # 2. Attack the checking piece directly
            for row in range(0, 8):
                for col in range(0, 8):
                    if self.board.array_board[row][col] is not None:
                        if self.board.array_board[row][col].symbol not in self.choosable_pieces:
                            if (row, col) == (king_pos_row, king_pos_col):
                                continue
                            self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                            for r, c in self.board.array_board[row][col].legal_moves:
                                if self.board.array_board[r][c] is not None:
                                    if self.board.array_board[r][c].symbol not in self.choosable_pieces:
                                        continue

                                # Temporary move
                                captured = self.board.array_board[r][c]
                                self.board.array_board[r][c] = self.board.array_board[row][col]
                                self.board.array_board[row][col] = None

                                not_valid_move = False
                                for i in range(0, 8):
                                    for j in range(0, 8):
                                        if self.board.array_board[i][j] is not None:
                                            if self.board.array_board[i][j].symbol in self.choosable_pieces:
                                                self.board.array_board[i][j].get_legal_moves(i, j, self.board)
                                                if (king_pos_row, king_pos_col) in self.board.array_board[i][j].legal_moves:
                                                    not_valid_move = True
                                                    break
                                    if not_valid_move:
                                        break

                                # Undo temporary move
                                self.board.array_board[row][col] = self.board.array_board[r][c]
                                self.board.array_board[r][c] = captured
                                if not not_valid_move:
                                    checkmate = False
                                    break
                    if not checkmate:
                        break
                if not checkmate:
                    break
        return checkmate


class Board:
    def __init__(self):
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

    def print_board(self):
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


class Pawn():
    def __init__(self, color):
        self.first_time = True

        self.color = color
        self.white_symbol = "♟︎"
        self.black_symbol = "♙"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
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


class Rook():
    def __init__(self, color):
        self.color = color
        self.white_symbol = "♜"
        self.black_symbol = "♖"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
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


class Bishop():
    def __init__(self, color):
        self.color = color
        self.white_symbol = "♝"
        self.black_symbol = "♗"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
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


class Knight():
    def __init__(self, color):
        self.color = color
        self.white_symbol = "♞"
        self.black_symbol = "♘"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
        self.legal_moves = []

        moves = [
            (row-2, col-1), (row-2, col+1),  # Top two
            (row-1, col-2), (row+1, col-2),  # Left two
            (row+2, col-1), (row+2, col+1),  # Bottom two
            (row-1, col+2), (row+1, col+2)  # Right two
        ]

        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:
                self.legal_moves.append((r, c))


class Queen():
    def __init__(self, color):
        self.color = color
        self.white_symbol = "♛"
        self.black_symbol = "♕"

        if self.color == "white":
            self.symbol = self.white_symbol
        else:
            self.symbol = self.black_symbol

    def get_legal_moves(self, row, col, board):
        self.legal_moves = []

        # Rook logic
        temp_rook = Rook(self.color)
        temp_rook.get_legal_moves(row, col, board)
        self.legal_moves.extend(temp_rook.legal_moves)

        # Bishop logic
        temp_bishop = Bishop(self.color)
        temp_bishop.get_legal_moves(row, col, board)
        self.legal_moves.extend(temp_bishop.legal_moves)


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


game = Game()
game.logic()
