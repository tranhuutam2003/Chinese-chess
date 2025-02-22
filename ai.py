import copy
import random
from move_validator import MoveValidator

class ChessAI:
    def __init__(self, is_red):
        self.is_red = is_red  # AI là bên Đỏ hay Đen

    def evaluate_board(self, red_pieces, black_pieces):
        piece_values = {"帥": 1000, "將": -1000, "車": 90, "馬": 40, "象": 20, "相": -20,
                        "士": 10, "仕": -10, "包": 45, "炮": -45, "卒": 5, "兵": -5}
        score = 0
        for pos, piece in red_pieces.items():
            score += piece_values.get(piece, 0)
        for pos, piece in black_pieces.items():
            score += piece_values.get(piece, 0)
        return score

    def minimax(self, red_pieces, black_pieces, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate_board(red_pieces, black_pieces), None

        best_move = None
        current_pieces = red_pieces if maximizing else black_pieces
        other_pieces = black_pieces if maximizing else red_pieces

        best_value = float('-inf') if maximizing else float('inf')

        for pos, piece in list(current_pieces.items()):
            valid_moves = MoveValidator.generate_valid_moves(piece, pos, current_pieces, other_pieces)

            for new_pos in valid_moves:
                # Kiểm tra xem new_pos có quân cùng màu không
                if new_pos in current_pieces:
                    continue  # Bỏ qua nước đi này

                new_current = copy.deepcopy(current_pieces)
                new_other = copy.deepcopy(other_pieces)

                # Di chuyển quân
                new_current[new_pos] = new_current.pop(pos)

                # Nếu ăn quân đối phương
                if new_pos in new_other:
                    new_other.pop(new_pos)

                value, _ = self.minimax(
                    new_current if maximizing else new_other,
                    new_other if maximizing else new_current,
                    depth - 1, alpha, beta, not maximizing
                )

                if maximizing and value > best_value:
                    best_value, best_move = value, (pos, new_pos)
                    alpha = max(alpha, value)
                elif not maximizing and value < best_value:
                    best_value, best_move = value, (pos, new_pos)
                    beta = min(beta, value)

                if beta <= alpha:
                    break

        return best_value, best_move

    def get_best_move(self, red_pieces, black_pieces, depth=3):
        _, best_move = self.minimax(
            red_pieces,
            black_pieces,
            depth,
            float('-inf'),
            float('inf'),
            self.is_red  # Đã sửa từ not self.is_red → self.is_red
        )
        return best_move