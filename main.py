import pygame
import sys
from settings import *
from engine import Engine
from ai import AI

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess by Abu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Algerian", 45)
        self.engine = Engine()
        self.ai = AI("black", 4, self.engine)  # adjust as desired, set colour to None for PvP

    def run(self):
        game_ended = False
        click_count = 0
        last_square_clicked = None

        while not game_ended:
            if self.engine.turn == self.ai.colour:
                best_move = self.ai.get_best_move()
                if best_move:
                    self.engine.make_move(best_move[0], best_move[1])
                    self.animate_move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_count += 1
                    mouse_pos = pygame.mouse.get_pos()
                    square_clicked = (mouse_pos[1] // SQUARE_DIM, mouse_pos[0] // SQUARE_DIM)
                    # First click selects a piece otherwise does nothing
                    if click_count == 1:
                        # Mouse click is valid if it is a piece that is selected during its turn
                        if square_clicked in self.engine.board.dict:
                            piece_selected = self.engine.board.dict[square_clicked]
                            if piece_selected.colour == self.engine.turn:
                                last_square_clicked = square_clicked
                            else:
                                click_count = 0
                        else:
                            click_count = 0

                    elif click_count == 2:
                        # Double click
                        if last_square_clicked == square_clicked:
                            click_count = 0
                        elif square_clicked in self.engine.board.dict:
                            piece_to_move = self.engine.board.dict[square_clicked]
                            # A different piece was selected (but on the correct team)
                            if piece_to_move.colour == self.engine.turn:
                                last_square_clicked = square_clicked
                                click_count = 1
                            # A capture move was made
                            elif square_clicked in self.engine.legal_moves(self.engine.board.dict[last_square_clicked]):
                                self.engine.make_move(last_square_clicked, square_clicked)
                                self.animate_move()
                                click_count = 0
                            else:
                                click_count = 0
                        # A move was made to an empty square
                        else:
                            piece_to_move = self.engine.board.dict[last_square_clicked]
                            if square_clicked in self.engine.legal_moves(piece_to_move):
                                self.engine.make_move(last_square_clicked, square_clicked)
                                self.animate_move()
                            click_count = 0

                if event.type == pygame.KEYDOWN:
                    # Left arrow key will undo the previous move
                    if event.key == pygame.K_LEFT:
                        self.engine.undo_move()
                        click_count = 0
                    # 'R' key resets the game
                    if event.key == pygame.K_r:
                        self.engine.reset()
                        click_count = 0

                self.engine.board.draw(self.window)
                # If the king is in check show it on the board
                if self.engine.in_check():
                    self.reveal_check()
                self.show_previous_move()
                # If a piece has been selected highlight its square
                if click_count == 1:
                    self.highlight_selection(last_square_clicked)
                # Draw all the pieces
                for piece in self.engine.board.dict.values():
                    piece.draw(self.window)
                # If a piece has been selected show its possible moves
                if click_count == 1:
                    self.show_moves(last_square_clicked)

                # Show checkmate/stalemate message if required
                if self.engine.is_checkmate():
                    self.display_message("Checkmate!!!", "press R to reset")
                if self.engine.is_stalemate():
                    self.display_message("Stalemate -_-", "press R to reset")

                # Display update
                pygame.display.update()
                self.clock.tick(FPS)

    def highlight_selection(self, square: tuple[int, int]):
        pygame.draw.rect(self.window, "khaki1", (square[1] * SQUARE_DIM, square[0] * SQUARE_DIM, SQUARE_DIM,
                                                 SQUARE_DIM))

    def show_moves(self, start_square: tuple[int, int]):
        piece = self.engine.board.dict[start_square]
        end_squares = self.engine.legal_moves(piece)
        for end_square in end_squares:
            pygame.draw.circle(self.window, "red", (end_square[1] * SQUARE_DIM + SQUARE_DIM / 2,
                                                    end_square[0] * SQUARE_DIM + SQUARE_DIM / 2), SQUARE_DIM / 8)

    def show_previous_move(self):
        if len(self.engine.move_log) > 0:
            last_move = self.engine.move_log[-1]
            sq1 = last_move.start_square
            sq2 = last_move.end_square
            pygame.draw.rect(self.window, "khaki", (sq1[1] * SQUARE_DIM, sq1[0] * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))
            pygame.draw.rect(self.window, "khaki1", (sq2[1] * SQUARE_DIM, sq2[0] * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))

    def reveal_check(self):
        king = next(piece for piece in self.engine.board.dict.values() if piece.name == "King" and
                    piece.colour == self.engine.turn)
        pygame.draw.rect(self.window, "red", (king.pos[1] * SQUARE_DIM, king.pos[0] * SQUARE_DIM,
                                              SQUARE_DIM, SQUARE_DIM))

    def animate_move(self):
        last_move = self.engine.move_log[-1]
        piece_moved = self.engine.board.dict[last_move.end_square]
        start_row, start_col = last_move.start_square
        end_row, end_col = last_move.end_square
        dR = end_row - start_row
        dC = end_col - start_col

        frames_per_square = 2
        frame_count = (abs(dR) + abs(dC)) * frames_per_square
        for frame in range(frame_count + 1):
            self.engine.board.draw(self.window)
            for piece in self.engine.board.dict.values():
                piece.draw(self.window)
            if last_move.piece_captured is not None:
                last_move.piece_captured.draw(self.window)
            piece_moved.move(((start_row + dR * frame / frame_count), (start_col + dC * frame / frame_count)))
            piece_moved.draw(self.window)

            pygame.display.update()
            self.clock.tick(FPS)

        piece_moved.pos = (end_row, end_col)  # to eliminate any dict key errors
        pygame.display.update()
        self.clock.tick(FPS)

    def display_message(self, message1: str, message2: str | None = None):
        text1 = self.font.render(message1, True, "green")
        text1_rect = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.window.blit(text1, text1_rect)
        if message2:
            text2 = self.font.render(message2, True, "green")
            text2_rect = text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.window.blit(text2, text2_rect)


if __name__ == "__main__":
    game = Game()
    game.run()
