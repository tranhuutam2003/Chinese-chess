from move_validator import MoveValidator


class GameState:
    def __init__(self, red_pieces, black_pieces):
        self.red_pieces = red_pieces
        self.black_pieces = black_pieces
        self.red_turn = True

    def is_checkmate(self):
        """Kiểm tra nếu tướng bị chiếu hết cờ."""
        pieces = self.red_pieces if self.red_turn else self.black_pieces
        other_pieces = self.black_pieces if self.red_turn else self.red_pieces

        for pos, piece in pieces.items():
            valid_moves = MoveValidator.generate_valid_moves(piece, pos, pieces, other_pieces)
            if valid_moves:
                return False  # Vẫn còn nước đi hợp lệ
        return True  # Không còn nước đi, bị chiếu hết

    def is_draw(self):
        """Kiểm tra hòa cờ (ví dụ: lặp nước, không thể thắng)."""
        # Thêm điều kiện kiểm tra hòa ở đây (lặp nước, thế cờ hòa...)
        return False  # Tạm thời trả về False