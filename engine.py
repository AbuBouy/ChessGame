from board import Board
from settings import *
from pieces import Queen, Pawn


class Engine:
    def __init__(self):
        self.board = Board()
        self.turn = "white"  # white moves first
        self.move_log = []  # list of Move objects to track moves made in the game

    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def make_move(self, start_square, end_square):
        piece_to_move = self.board.dict.pop(start_square)  # remove piece from start square

        is_promotion = False
        # Check for pawn promotion
        if piece_to_move.name == "Pawn":
            if ((piece_to_move.colour == "white" and end_square[0] == 0) or
                    (piece_to_move.colour == "black" and end_square[0] == 7)):
                piece_to_move = Queen(piece_to_move.colour, piece_to_move.pos, self.board)
                is_promotion = True

        # If the King or a rook was moved, keep track of whether it could castle before the move was made
        original_can_castle = None
        if piece_to_move.name in ["King", "Rook"]:
            original_can_castle = piece_to_move.can_castle
            piece_to_move.can_castle = False

        # Check if a castle move was made
        is_castle_move = False
        if piece_to_move.name == "King" and abs(end_square[1] - start_square[1]) == 2:
            row, col = end_square
            # King-side castling
            if end_square[1] - start_square[1] == 2:
                rook = self.board.dict.pop((row, 7))  # remove rook from old position
                new_pos = (row, col - 1)  # rook goes to the left of the king
                rook.move(new_pos)
                self.board.dict[new_pos] = rook
                rook.can_castle = False
                is_castle_move = True

            # Queen-side castling
            else:
                rook = self.board.dict.pop((row, 0))  # remove rook from old position
                new_pos = (row, col + 1)  # rook goes to the right of the king
                rook.move(new_pos)
                self.board.dict[new_pos] = rook
                rook.can_castle = False
                is_castle_move = True

        # Update the move log
        piece_captured = self.board.dict.get(end_square)
        self.move_log.append(Move(start_square, end_square, piece_captured, is_promotion, is_castle_move, original_can_castle))

        # Move piece to end square
        piece_to_move.move(end_square)
        self.board.dict[end_square] = piece_to_move

        self.switch_turn()

    def undo_move(self):
        if len(self.move_log) > 0:
            previous_move = self.move_log.pop(-1)
            piece_moved = self.board.dict.pop(previous_move.end_square)

            # Undo promotion
            if previous_move.is_promotion:
                piece_moved = Pawn(piece_moved.colour, piece_moved.pos, self.board)  # demote queen back to a pawn

            # Move the piece back to its original place
            self.board.dict[previous_move.start_square] = piece_moved
            piece_moved.move(previous_move.start_square)

            # If a piece was captured then place it back on the board
            if previous_move.piece_captured is not None:
                self.board.dict[previous_move.end_square] = previous_move.piece_captured

            # Undo castle move
            if previous_move.is_castle_move:
                piece_moved.can_castle = True  # if a castle move was made then the piece moved is the king
                end_row, end_col = previous_move.end_square
                # Undo King-side castle
                if previous_move.end_square[1] - previous_move.start_square[1] == 2:
                    rook = self.board.dict.pop((end_row, end_col - 1))  # Rook will be 1 to the left of the king
                    rook.move((end_row, 7))
                    self.board.dict[(end_row, 7)] = rook
                    rook.can_castle = True

                # Undo Queen-side castle
                else:
                    rook = self.board.dict.pop((end_row, end_col + 1))
                    rook.move((end_row, 0))
                    self.board.dict[(end_row, 0)] = rook
                    rook.can_castle = True

            # Restore previous castling rights if the king or rook was moved (but wasn't a castle move)
            elif piece_moved.name in ["King", "Rook"]:
                piece_moved.can_castle = previous_move.original_can_castle

            # Reverse the turn
            self.switch_turn()

    def reset(self):
        for _ in range(len(self.move_log)):
            self.undo_move()

    def is_attacked(self, square):
        # Check diagonals for enemy bishops/queen/king
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            for i in range(1, 8):
                pos = (square[0] + direction[0] * i, square[1] + direction[1] * i)
                if pos[0] < 0 or pos[0] > BOARD_DIM or pos[1] < 0 or pos[1] > BOARD_DIM:
                    break  # no longer need to search direction as we are off the board

                if pos in self.board.dict:
                    piece = self.board.dict[pos]
                    if i == 1:
                        if piece.colour != self.turn and piece.name in ["Bishop", "Queen", "King"]:
                            return True
                        else:
                            break  # no longer need to check the direction
                    else:
                        if piece.colour != self.turn and piece.name in ["Bishop", "Queen"]:
                            return True
                        else:
                            break

        # Check horizontally and vertically for enemy rooks/queen/king
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in directions:
            for i in range(1, 8):
                pos = (square[0] + direction[0] * i, square[1] + direction[1] * i)
                if pos[0] < 0 or pos[0] > BOARD_DIM or pos[1] < 0 or pos[1] > BOARD_DIM:
                    break

                if pos in self.board.dict:
                    piece = self.board.dict[pos]
                    if i == 1:
                        if piece.colour != self.turn and piece.name in ["Rook", "Queen", "King"]:
                            return True
                        else:
                            break
                    else:
                        if piece.colour != self.turn and piece.name in ["Rook", "Queen"]:
                            return True
                        else:
                            break

        # Check for enemy knights
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for direction in directions:
            pos = (square[0] + direction[0], square[1] + direction[1])
            if pos[0] < 0 or pos[0] > BOARD_DIM or pos[1] < 0 or pos[1] > BOARD_DIM:
                continue

            if pos in self.board.dict:
                piece = self.board.dict[pos]
                if piece.colour != self.turn and piece.name == "Knight":
                    return True

        # Check for enemy pawns
        dy = -1 if self.turn == "white" else 1
        for dx in [1, -1]:
            pos = (square[0] + dy, square[1] + dx)
            if pos in self.board.dict:
                piece = self.board.dict[pos]
                if piece.colour != self.turn and piece.name == "Pawn":
                    return True

    def in_check(self):
        king = next(piece for piece in self.board.dict.values() if piece.name == "King" and piece.colour == self.turn)
        return self.is_attacked(king.pos)

    def legal_moves(self, piece):
        """Filters a piece's possible moves to not include those that will put the king in check"""
        legal_moves = []
        start_square = piece.pos

        # Apply each possible move and check that the king is not left in danger
        for end_square in piece.get_possible_moves():
            self.make_move(start_square, end_square)
            # Want to check if the team that made the move is in check so need to switch the turn
            self.switch_turn()
            if not self.in_check():
                legal_moves.append(end_square)
            self.switch_turn()
            self.undo_move()

        if piece.name == "King":
            legal_moves += self.add_castle_moves(piece)

        return legal_moves

    def is_checkmate(self):
        # Checkmate if king is in check and there are no possible legal moves
        if self.in_check():
            for piece in list(self.board.dict.values()):
                if piece.colour == self.turn:
                    if len(self.legal_moves(piece)) > 0:
                        return False  # If any piece can move, it's not checkmate
            return True  # If no piece can move, it's checkmate
        return False  # If the king is not in check, it's not checkmate

    def is_stalemate(self):
        # Stalemate if there are no possible legal moves while king is not in check
        if not self.in_check():
            for piece in list(self.board.dict.values()):
                if piece.colour == self.turn:
                    if len(self.legal_moves(piece)) > 0:
                        return False
            return True
        return False

    def add_castle_moves(self, king):
        castle_moves = []
        if not self.in_check() and king.can_castle:  # cannot castle whilst in check
            # King-side castling
            kingside_piece = self.board.dict.get((king.pos[0], 7))
            if kingside_piece is not None and kingside_piece.name == "Rook":
                # Allowed to castle if the square the king has to move over is not being attacked
                if (kingside_piece.can_castle and not self.is_attacked((king.pos[0], 5)) and
                        not self.is_attacked((king.pos[0], 6))):
                    if (king.pos[0], 5) not in self.board.dict and (king.pos[0], 6) not in self.board.dict:
                        castle_moves.append((king.pos[0], 6))
            # Queen-side castling
            queenside_piece = self.board.dict.get((king.pos[0], 0))
            if queenside_piece is not None and queenside_piece.name == "Rook":
                # Allowed to castle if the square the king has to move over is not being attacked
                if (queenside_piece.can_castle and not self.is_attacked((king.pos[0], 3)) and
                        not self.is_attacked((king.pos[0], 2))):
                    if (king.pos[0], 3) not in self.board.dict and (king.pos[0], 2) not in self.board.dict:
                        castle_moves.append((king.pos[0], 2))
        return castle_moves

    def get_legal_moves(self):
        moves = []
        for piece in list(self.board.dict.values()):
            if piece.colour == self.turn:
                for end_square in self.legal_moves(piece):
                    moves.append((piece.pos, end_square))
        return moves


class Move:
    def __init__(self, start_square, end_square, piece_captured, is_promotion, is_castle_move, original_can_castle=None):
        self.start_square = start_square
        self.end_square = end_square
        self.piece_captured = piece_captured
        self.is_promotion = is_promotion
        self.is_castle_move = is_castle_move
        self.original_can_castle = original_can_castle  # to let the king/rooks castle when moved and the move is undone
