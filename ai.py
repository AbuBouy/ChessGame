class AI:
    def __init__(self, colour, depth):
        self.colour = colour
        self.depth = depth

        # Piece square tables
        pawn_scores = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
            [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
            [0, 0, 0, 0.2, 0.2, 0, 0, 0],
            [0.05, -0.05, -0.1, 0, 0, -0.1, -0.05, 0.05],
            [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        knight_scores = [
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
            [-0.4, -0.2, 0, 0, 0, 0, -0.2, -0.4],
            [-0.3, 0, 0.1, 0.15, 0.15, 0.1, 0, -0.3],
            [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
            [-0.3, 0, 0.15, 0.2, 0.2, 0.15, 0, -0.3],
            [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
            [-0.4, -0.2, 0, 0.05, 0.05, 0, -0.2, -0.4],
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
        ]

        bishop_scores = [
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
            [-0.1, 0, 0, 0, 0, 0, 0, -0.1],
            [-0.1, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.1],
            [-0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1],
            [-0.1, 0, 0.1, 0.1, 0.1, 0.1, 0, -0.1],
            [-0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
            [-0.1, 0.05, 0, 0, 0, 0, 0.05, -0.1],
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
        ]

        rook_scores = [
            [0, 0, 0, 0.05, 0.05, 0, 0, 0],
            [0.05, 0, 0, 0, 0, 0, 0, 0.05],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        queen_scores = [
            [-0.1, -0.05, -0.05, -0.025, -0.025, -0.05, -0.05, -0.1],
            [-0.05, 0, 0, 0, 0, 0, 0, -0.05],
            [-0.05, 0, 0.025, 0.025, 0.025, 0.025, 0, -0.05],
            [-0.025, 0, 0.025, 0.025, 0.025, 0.025, 0, -0.025],
            [0, 0, 0.025, 0.025, 0.025, 0.025, 0, 0],
            [-0.05, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, -0.05],
            [-0.05, 0, 0.025, 0, 0, 0, 0, -0.05],
            [-0.1, -0.05, -0.05, -0.025, -0.025, -0.05, -0.05, -0.1]
        ]

        king_scores = [
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
            [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
            [0.2, 0.2, 0, 0, 0, 0, 0.2, 0.2],
            [0.2, 0.3, 0.1, 0, 0, 0.1, 0.3, 0.2]
        ]

        # Create a dictionary to map piece names to their respective scores
        self.square_values = {
            "Pawn": pawn_scores,
            "Knight": knight_scores,
            "Bishop": bishop_scores,
            "Rook": rook_scores,
            "Queen": queen_scores,
            "King": king_scores
        }

    def evaluate_board(self, engine):
        score = 0
        for piece in engine.board.dict.values():
            if piece.colour == "white":
                score += piece.value
                score += self.square_values[piece.name][piece.pos[0]][piece.pos[1]]
            else:
                score -= piece.value
                flipped_row_index = 7 - piece.pos[0]  # piece square table is flipped for black pieces
                score -= self.square_values[piece.name][flipped_row_index][piece.pos[1]]

        return score

    def negamax(self, engine, depth, alpha, beta, turn_multiplier):
        if depth == 0:
            return turn_multiplier * self.evaluate_board(engine), None

        moves = self.order_moves(engine)
        if len(moves) == 0:
            if engine.in_check():
                return float("-inf"), None
            else:
                return 0, None

        max_score = float("-inf")
        best_move = moves[0]  # a default move is chosen in case all moves evaluate to the same score, e.g. an
        # inevitable checkmate
        for move in moves:
            engine.make_move(move[0], move[1])
            score, _ = self.negamax(engine, depth - 1, -beta, -alpha, -turn_multiplier)
            score *= -1  # Negate the score since it's from the opponent's perspective
            engine.undo_move()

            if score > max_score:
                max_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Beta cutoff

        return max_score, best_move

    def get_best_move(self, engine):
        # Call negamax to find the best move
        turn_multiplier = 1 if engine.turn == "white" else -1
        score, best_move = self.negamax(engine, self.depth, float('-inf'), float('inf'), turn_multiplier)
        return best_move

    @staticmethod
    def order_moves(engine):
        """Orders the legal moves in a way that will potentially speed up the negamax search"""
        ordered_moves = []

        moves = engine.get_legal_moves()
        # Prioritise pawn promotions
        promotion_moves = [move for move in moves if engine.board.dict[move[0]].name == "Pawn" and
                           (move[1][0] == 0 or move[1][0] == 7)]
        ordered_moves.extend(promotion_moves)

        # Prioritise capture moves and sort by value of piece captured
        capture_moves = [move for move in moves if engine.board.dict.get(move[1]) is not None]
        capture_moves.sort(key=lambda move: engine.board.dict[move[1]].value, reverse=True)
        ordered_moves.extend(capture_moves)

        # Prioritise moves that control central squares
        central_moves = [move for move in moves if move[1] in [(3, 3), (3, 4), (4, 3), (4, 4)]]
        ordered_moves.extend(central_moves)

        # Add in the rest of the moves
        remaining_moves = [move for move in moves if move not in ordered_moves]
        ordered_moves.extend(remaining_moves)

        return ordered_moves
