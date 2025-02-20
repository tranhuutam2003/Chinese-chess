class MoveValidator:
    @staticmethod
    def is_valid_move(piece, current_pos, new_pos, pieces, other_pieces):
        x, y = current_pos
        new_x, new_y = new_pos

        if piece in ["卒", "兵"]:  # Tốt/Binh
            direction = 1 if piece == "卒" else -1  # Tốt (卒) đi xuống, Binh (兵) đi lên
            if new_x == x and new_y == y + direction:
                return True  # Đi thẳng bình thường
            if (piece == "卒" and y >= 5) or (piece == "兵" and y <= 4):
                # Nếu đã qua sông, cho phép đi ngang
                if abs(new_x - x) == 1 and new_y == y:
                    return True
            return False

        elif piece in ["將", "帥"]:  # Tướng/Soái
            dx = abs(new_x - x)
            dy = abs(new_y - y)
            if piece == "將":
                if not (3 <= new_x <= 5 and 0 <= new_y <= 2):
                    return False
            if piece == "帥":
                if not (3 <= new_x <= 5 and 7 <= new_y <= 9):
                    return False
            return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

        elif piece == "車":  # Xe
            if new_x == x:  # Đi dọc
                step = 1 if new_y > y else -1
                for i in range(y + step, new_y, step):
                    if (x, i) in pieces or (x, i) in other_pieces:
                        return False
            elif new_y == y:  # Đi ngang
                step = 1 if new_x > x else -1
                for i in range(x + step, new_x, step):
                    if (i, y) in pieces or (i, y) in other_pieces:
                        return False
            else:
                return False
            return True

        elif piece == "馬":  # Mã
            dx = abs(new_x - x)
            dy = abs(new_y - y)
            if dx == 2 and dy == 1:  # Nhảy ngang trước, dọc sau
                if (x + (new_x - x) // 2, y) in pieces or (x + (new_x - x) // 2, y) in other_pieces:
                    return False
            elif dx == 1 and dy == 2:  # Nhảy dọc trước, ngang sau
                if (x, y + (new_y - y) // 2) in pieces or (x, y + (new_y - y) // 2) in other_pieces:
                    return False

            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

        elif piece in ["象", "相"]:  # Tượng/Tướng
            dx = abs(new_x - x)
            dy = abs(new_y - y)
            if piece == "象":
                if not (0 <= new_x <= 8 and 0 <= new_y <= 4):
                    return False
            if piece == "相":
                if not (0 <= new_x <= 8 and 5 <= new_y <= 9):
                    return False
            return dx == 2 and dy == 2

        elif piece in ["士", "仕"]:  # Sĩ
            dx = abs(new_x - x)
            dy = abs(new_y - y)
            if piece == "士":
                if not (3 <= new_x <= 5 and 0 <= new_y <= 2):
                    return False
            if piece == "仕":
                if not (3 <= new_x <= 5 and 7 <= new_y <= 9):
                    return False
            return dx == 1 and dy == 1

        elif piece in ["包", "炮"]:  # Pháo
            count = 0
            if new_x == x:  # Đi dọc
                step = 1 if new_y > y else -1
                for i in range(y + step, new_y, step):
                    if (x, i) in pieces or (x, i) in other_pieces:
                        count += 1
            elif new_y == y:  # Đi ngang
                step = 1 if new_x > x else -1
                for i in range(x + step, new_x, step):
                    if (i, y) in pieces or (i, y) in other_pieces:
                        count += 1
            else:
                return False
            if new_pos in other_pieces:  # Ăn quân
                return count == 1  # Phải có đúng 1 quân cản
            return count == 0  # Đi thường thì không được có quân cản

        return False

    @staticmethod
    def generate_valid_moves(piece, current_pos, pieces, other_pieces):
        valid_moves = []
        for i in range(10):
            for j in range(9):
                if MoveValidator.is_valid_move(piece, current_pos, (j, i), pieces, other_pieces):
                    valid_moves.append((j, i))
        return valid_moves