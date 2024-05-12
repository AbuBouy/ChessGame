from settings import *
import pygame


class Piece:
    def __init__(self, colour, pos, board):
        self.colour = colour  # black or white
        self.pos = pos  # position on board array
        self.image = pygame.image.load("images/whitePawn.png")
        self.rect = self.image.get_rect(topleft=(self.pos[1] * SQUARE_DIM, self.pos[0] * SQUARE_DIM))
        self.board = board  # board object

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, new_pos):
        # sets the new coordinates
        self.pos = new_pos
        self.rect.topleft = (self.pos[1] * SQUARE_DIM, self.pos[0] * SQUARE_DIM)


class SlidingPiece(Piece):
    """Parent class which the Rook, Bishop and Queen will inherit from since
    they have identical movement logic just with different movement directions

    The 'move_directions' attribute is not defined for this class but will be
    for the classes that inherit from it
    """

    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.move_directions = None

    def get_possible_moves(self):
        legal_moves = []
        for direction in self.move_directions:
            for i in range(1, BOARD_DIM):
                target_square = (self.pos[0] + direction[0] * i, self.pos[1] + direction[1] * i)
                if (target_square[0] < 0 or target_square[0] >= BOARD_DIM or
                        target_square[1] < 0 or target_square[1] >= BOARD_DIM):
                    break
                if target_square not in self.board.dict:
                    legal_moves.append(target_square)
                elif self.board.dict[target_square].colour != self.colour:
                    legal_moves.append(target_square)
                    break
                else:
                    break

        return legal_moves


class Pawn(Piece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "Pawn"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 10

    def get_possible_moves(self):
        possible_moves = []
        start_row = 6
        move_direction = -1
        if self.colour == "black":
            start_row = 1
            move_direction = 1

        blocked = False  # True or false depending on whether the pawn can move forward
        # Can move 1 square forward if not occupied
        target_square = (self.pos[0] + move_direction, self.pos[1])
        if target_square not in self.board.dict:
            possible_moves.append(target_square)
        else:
            blocked = True

        # Can move 2 squares forward if still on start square and if target square and the one behind are not occupied
        if not blocked:
            target_square = (self.pos[0] + 2 * move_direction, self.pos[1])
            if self.pos[0] == start_row and target_square not in self.board.dict:
                possible_moves.append(target_square)

        # Can capture diagonally 1 square
        for capture_direction in [(move_direction, 1), (move_direction, -1)]:
            target_square = (self.pos[0] + capture_direction[0], self.pos[1] + capture_direction[1])
            if target_square in self.board.dict:
                piece = self.board.dict[target_square]
                if piece.colour != self.colour:
                    possible_moves.append(target_square)

        return possible_moves


class Knight(Piece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "Knight"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 30

    def get_possible_moves(self):
        possible_moves = []
        move_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for direction in move_directions:
            target_square = (self.pos[0] + direction[0], self.pos[1] + direction[1])
            if 0 <= target_square[0] < BOARD_DIM and 0 <= target_square[1] < BOARD_DIM:
                if target_square not in self.board.dict:
                    possible_moves.append(target_square)
                elif self.board.dict[target_square].colour != self.colour:
                    possible_moves.append(target_square)

        return possible_moves


class Rook(SlidingPiece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "Rook"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 50
        self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.can_castle = True

    def move(self, new_pos):
        self.pos = new_pos
        self.rect.topleft = (self.pos[1] * SQUARE_DIM, self.pos[0] * SQUARE_DIM)


class Bishop(SlidingPiece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "Bishop"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 50
        self.move_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


class Queen(SlidingPiece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "Queen"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 90
        self.move_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1),
                                (1, 0), (-1, 0), (0, 1), (0, -1)]


class King(Piece):
    def __init__(self, colour, pos, board):
        super().__init__(colour, pos, board)
        self.name = "King"
        self.image = pygame.image.load("images/" + self.colour + self.name + ".png")
        self.value = 0
        self.can_castle = True

    def get_possible_moves(self):
        possible_moves = []
        move_directions = [(1, 0), (1, 1), (1, -1), (-1, 0),
                           (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for direction in move_directions:
            target_square = (self.pos[0] + direction[0], self.pos[1] + direction[1])
            if 0 <= target_square[0] < BOARD_DIM and 0 <= target_square[1] < BOARD_DIM:
                if target_square not in self.board.dict:
                    possible_moves.append(target_square)
                elif self.board.dict[target_square].colour != self.colour:
                    possible_moves.append(target_square)

        return possible_moves

    def move(self, new_pos):
        self.pos = new_pos
        self.rect.topleft = (self.pos[1] * SQUARE_DIM, self.pos[0] * SQUARE_DIM)

