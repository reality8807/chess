from board import Board


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.board.print_board()

        self.letter_conversion = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        self.white_pieces = ["♟︎", "♜", "♞", "♝", "♛", "♚"]
        self.black_pieces = ["♙", "♖", "♘", "♗", "♕", "♔"]

        self.turn = "white"
        self.choosable_pieces = self.white_pieces

    def logic(self) -> None:
        while True:
            # Initial Input
            self.get_initial_input()

            if self.initial_selected_piece is None:
                print("\nInvalid move, select a piece!\n")
                continue
            elif self.initial_selected_piece.symbol not in self.choosable_pieces:
                print(f"\nSelect a {self.turn} piece!\n")
                continue

            # Final Input
            self.get_final_input()
            if self.final_selected_piece is not None:
                if self.final_selected_piece.symbol in self.choosable_pieces:
                    print("\nYou cannot attack your own piece!\n")
                    continue

            self.initial_selected_piece.get_legal_moves(self.initial_row, self.initial_col, self.board)

            if self.final_selected_pos not in self.initial_selected_piece.legal_moves:
                if self.initial_selected_piece.symbol in ["♚", "♔"]:
                    if self.initial_selected_piece.first_time:
                        self.castle()
                        continue
                print("\nIllegal move, try again!\n")
                continue

            if self.is_self_check():
                continue

            if self.initial_selected_piece.symbol in ["♜", "♖", "♚", "♔"]:
                self.initial_selected_piece.first_time = False

            self.board.print_board()
            self.switch_player()

    def get_initial_input(self) -> None:
        initial_move = input("Enter Initial Move: ")
        if initial_move == "exit":
            exit()
        if len(initial_move) != 2:
            print("\nInvalid Move. Enter the position of the piece you want to move (e.g., e2)\n")
            self.get_initial_input()
        try:
            self.initial_row = 8-int(initial_move[1])
            self.initial_col = self.letter_conversion.get(initial_move[0])

            self.initial_selected_pos = (self.initial_row, self.initial_col)
            self.initial_selected_piece = self.board.array_board[self.initial_row][self.initial_col]
        except:
            print("\nInvalid Move. Enter the position of the piece you want to move (e.g., e2)\n")
            self.get_initial_input()

    def get_final_input(self) -> None:
        final_move = input("Enter Final Move: ")
        if final_move == "exit":
            exit()
        if len(final_move) != 2:
            print("\nInvalid Move. Enter proper destination square (e.g., e4)\n")
            self.get_final_input()
        try:
            self.final_row = 8-int(final_move[1])
            self.final_col = self.letter_conversion.get(final_move[0])

            self.final_selected_pos = (self.final_row, self.final_col)
            self.final_selected_piece = self.board.array_board[self.final_row][self.final_col]
        except:
            print("\nInvalid Move. Enter proper destination square (e.g., e4)\n")
            self.get_final_input()

    def switch_player(self) -> None:
        if self.turn == "white":
            self.turn = "black"
            self.choosable_pieces = self.black_pieces
        else:
            self.turn = "white"
            self.choosable_pieces = self.white_pieces

    def is_self_check(self) -> bool:
        board = self.board.array_board
        temp_final_piece = board[self.final_row][self.final_col]

        # Make the move made by user
        board[self.initial_row][self.initial_col] = None
        board[self.final_row][self.final_col] = self.initial_selected_piece

        # Find own king's position
        for row in range(0, 8):
            for piece in range(0, 8):
                if board[row][piece] is not None:
                    if self.turn == "white":
                        if board[row][piece].symbol == "♚":
                            king_pos = (row, piece)
                            break
                    else:
                        if board[row][piece].symbol == "♔":
                            king_pos = (row, piece)
                            break

        # Check if king is in check
        for row in range(0, 8):
            for piece in range(0, 8):
                if board[row][piece] is not None:
                    if board[row][piece].symbol not in self.choosable_pieces:
                        board[row][piece].get_legal_moves(row, piece, self.board)
                        if king_pos in board[row][piece].legal_moves:
                            print("\nYou cannot play this move, your king is still in check!\n")
                            # Undo the move made by user
                            board[self.initial_row][self.initial_col] = self.initial_selected_piece
                            board[self.final_row][self.final_col] = temp_final_piece
                            return True

        return self.is_check()

    def is_check(self) -> bool:
        board = self.board.array_board

        # Find opponent king's position
        for row in range(0, 8):
            for piece in range(0, 8):
                if board[row][piece] is not None:
                    if self.turn == "white":
                        if board[row][piece].symbol == "♔":
                            king_pos = (row, piece)
                            break
                    else:
                        if board[row][piece].symbol == "♚":
                            king_pos = (row, piece)
                            break

        # Check if opponent's king is in check
        for row in range(0, 8):
            for piece in range(0, 8):
                if board[row][piece] is not None:
                    if board[row][piece].symbol in self.choosable_pieces:
                        board[row][piece].get_legal_moves(row, piece, self.board)
                        if king_pos in board[row][piece].legal_moves:
                            if self.is_checkmate(king_pos[0], king_pos[1]):
                                print("\nCheckmate!")
                                print(f"{self.turn.capitalize()} won the game!!")
                                self.board.print_board()
                                exit()
                            print("\nCHECK!\n")
                            return False
        return False

    def is_checkmate(self, king_pos_row: int, king_pos_col: int) -> bool:
        board = self.board.array_board
        checkmate = True

        # 1. Check if king can move to another place

        # Find all possible places the king can go
        board[king_pos_row][king_pos_col].get_legal_moves(king_pos_row, king_pos_col, self.board)
        for r, c in board[king_pos_row][king_pos_col].legal_moves:
            if board[r][c] is not None:
                if board[r][c].symbol not in self.choosable_pieces:
                    continue
            # Temporary move
            captured = board[r][c]
            board[r][c] = board[king_pos_row][king_pos_col]
            board[king_pos_row][king_pos_col] = None
            not_valid_move = False

            # Check if king can avoid check
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col] is not None:
                        if board[row][col].symbol in self.choosable_pieces:
                            board[row][col].get_legal_moves(row, col, self.board)
                            if (r, c) in board[row][col].legal_moves:
                                not_valid_move = True
                                break
                if not_valid_move:
                    break

            # Undo the temporary move
            board[king_pos_row][king_pos_col] = board[r][c]
            board[r][c] = captured
            if not not_valid_move:
                checkmate = False
                break

        if checkmate:
            # 2. Attack the checking piece directly
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col] is not None:
                        if board[row][col].symbol not in self.choosable_pieces:
                            if (row, col) == (king_pos_row, king_pos_col):
                                continue
                            board[row][col].get_legal_moves(row, col, self.board)
                            for r, c in board[row][col].legal_moves:
                                if board[r][c] is not None:
                                    if board[r][c].symbol not in self.choosable_pieces:
                                        continue

                                # Temporary move
                                captured = board[r][c]
                                board[r][c] = board[row][col]
                                board[row][col] = None

                                not_valid_move = False
                                for i in range(0, 8):
                                    for j in range(0, 8):
                                        if board[i][j] is not None:
                                            if board[i][j].symbol in self.choosable_pieces:
                                                board[i][j].get_legal_moves(i, j, self.board)
                                                if (king_pos_row, king_pos_col) in board[i][j].legal_moves:
                                                    not_valid_move = True
                                                    break
                                    if not_valid_move:
                                        break

                                # Undo temporary move
                                board[row][col] = board[r][c]
                                board[r][c] = captured
                                if not not_valid_move:
                                    checkmate = False
                                    break
                    if not checkmate:
                        break
                if not checkmate:
                    break
        return checkmate

    def castle(self):
        if self.initial_selected_piece.color == "white":
            if self.final_selected_pos == (7, 6):
                if self.board.array_board[7][7].first_time and self.board.array_board[7][6] is None and self.board.array_board[7][5] is None:
                    invalid_castle = False
                    for row in range(0, 8):
                        for col in range(0, 8):
                            if self.board.array_board[row][col] is not None:
                                if self.board.array_board[row][col].color == "black":
                                    self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                                    if (7, 4) in self.board.array_board[row][col].legal_moves or (7, 5) in self.board.array_board[row][col].legal_moves or (7, 6) in self.board.array_board[row][col].legal_moves:
                                        invalid_castle = True
                                        break
                        if invalid_castle:
                            break

                    if not invalid_castle:
                        self.board.array_board[7][4].first_time = False
                        self.board.array_board[7][6] = self.initial_selected_piece
                        self.board.array_board[7][4] = None
                        self.board.array_board[7][5] = self.board.array_board[7][7]
                        self.board.array_board[7][7] = None
                        self.is_check()
                        self.board.print_board()
                        self.switch_player()
                    else:
                        print("\nIllegal move, try again!\n")
                else:
                    print("\nIllegal move, try again!\n")

            elif self.final_selected_pos == (7, 2):
                if self.board.array_board[7][0].first_time and self.board.array_board[7][1] is None and self.board.array_board[7][2] is None and self.board.array_board[7][3] is None:
                    invalid_castle = False
                    for row in range(0, 8):
                        for col in range(0, 8):
                            if self.board.array_board[row][col] is not None:
                                if self.board.array_board[row][col].color == "black":
                                    self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                                    if (7, 4) in self.board.array_board[row][col].legal_moves or (7, 3) in self.board.array_board[row][col].legal_moves or (7, 2) in self.board.array_board[row][col].legal_moves:
                                        invalid_castle = True
                                        break
                        if invalid_castle:
                            break

                    if not invalid_castle:
                        self.board.array_board[7][4].first_time = False
                        self.board.array_board[7][2] = self.initial_selected_piece
                        self.board.array_board[7][4] = None
                        self.board.array_board[7][3] = self.board.array_board[7][0]
                        self.board.array_board[7][0] = None
                        self.is_check()
                        self.board.print_board()
                        self.switch_player()
                    else:
                        print("\nIllegal move, try again!\n")
                else:
                    print("\nIllegal move, try again!\n")

            else:
                print("\nIllegal move, try again!\n")

        else:
            if self.final_selected_pos == (0, 6):
                if self.board.array_board[0][7].first_time and self.board.array_board[0][6] is None and self.board.array_board[0][5] is None:
                    invalid_castle = False
                    for row in range(0, 8):
                        for col in range(0, 8):
                            if self.board.array_board[row][col] is not None:
                                if self.board.array_board[row][col].color == "white":
                                    self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                                    if (0, 4) in self.board.array_board[row][col].legal_moves or (0, 5) in self.board.array_board[row][col].legal_moves or (0, 6) in self.board.array_board[row][col].legal_moves:
                                        invalid_castle = True
                                        break
                        if invalid_castle:
                            break

                    if not invalid_castle:
                        self.board.array_board[0][4].first_time = False
                        self.board.array_board[0][6] = self.initial_selected_piece
                        self.board.array_board[0][4] = None
                        self.board.array_board[0][5] = self.board.array_board[0][7]
                        self.board.array_board[0][7] = None
                        self.is_check()
                        self.board.print_board()
                        self.switch_player()
                    else:
                        print("\nIllegal move, try again!\n")
                else:
                    print("\nIllegal move, try again!\n")

            elif self.final_selected_pos == (0, 2):
                if self.board.array_board[0][0].first_time and self.board.array_board[0][1] is None and self.board.array_board[0][2] is None and self.board.array_board[0][3] is None:
                    invalid_castle = False
                    for row in range(0, 8):
                        for col in range(0, 8):
                            if self.board.array_board[row][col] is not None:
                                if self.board.array_board[row][col].color == "black":
                                    self.board.array_board[row][col].get_legal_moves(row, col, self.board)
                                    if (0, 4) in self.board.array_board[row][col].legal_moves or (0, 3) in self.board.array_board[row][col].legal_moves or (0, 2) in self.board.array_board[row][col].legal_moves:
                                        invalid_castle = True
                                        break
                        if invalid_castle:
                            break

                    if not invalid_castle:
                        self.board.array_board[0][4].first_time = False
                        self.board.array_board[0][2] = self.initial_selected_piece
                        self.board.array_board[0][4] = None
                        self.board.array_board[0][3] = self.board.array_board[0][0]
                        self.board.array_board[0][0] = None
                        self.is_check()
                        self.board.print_board()
                        self.switch_player()
                    else:
                        print("\nIllegal move, try again!\n")
                else:
                    print("\nIllegal move, try again!\n")

            else:
                print("\nIllegal move, try again!\n")
