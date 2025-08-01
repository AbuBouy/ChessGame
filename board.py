from settings import BOARD_DIM, SQUARE_DIM
from pieces import *


class Board:
    def __init__(self):
        self.dict = {}  # dictionary where the keys are board positions and the values are piece objects
        for piece in self.create_pieces():
            self.dict[piece.pos] = piece

        self.colours = ["beige", "bisque4"]

    def create_pieces(self) -> list[Piece]:
        pieces = []
        # Place pawns
        for col in range(BOARD_DIM):
            pieces.append(Pawn("white", BoardPosition(6, col), self))  # white pawns are on row 6
            pieces.append(Pawn("black", BoardPosition(1, col), self))  # black pawns are on row 1

        # Place Rooks
        pieces.append(Rook("white", BoardPosition(7, 0), self))
        pieces.append(Rook("white", BoardPosition(7, 7), self))
        pieces.append(Rook("black", BoardPosition(0, 0), self))
        pieces.append(Rook("black", BoardPosition(0, 7), self))

        # Place Knights
        pieces.append(Knight("white", BoardPosition(7, 1), self))
        pieces.append(Knight("white", BoardPosition(7, 6), self))
        pieces.append(Knight("black", BoardPosition(0, 1), self))
        pieces.append(Knight("black", BoardPosition(0, 6), self))

        # Place Bishops
        pieces.append(Bishop("white", BoardPosition(7, 2), self))
        pieces.append(Bishop("white", BoardPosition(7, 5), self))
        pieces.append(Bishop("black", BoardPosition(0, 2), self))
        pieces.append(Bishop("black", BoardPosition(0, 5), self))

        # Place Queens
        pieces.append(Queen("white", BoardPosition(7, 3), self))
        pieces.append(Queen("black", BoardPosition(0, 3), self))

        # Place Kings
        pieces.append(King("white", BoardPosition(7, 4), self))
        pieces.append(King("black", BoardPosition(0, 4), self))

        return pieces

    def draw(self, window: pygame.Surface):
        for row in range(BOARD_DIM):
            for col in range(BOARD_DIM):
                pygame.draw.rect(window, self.colours[(row + col) % 2], (col * SQUARE_DIM, row * SQUARE_DIM,
                                                                         SQUARE_DIM, SQUARE_DIM))
