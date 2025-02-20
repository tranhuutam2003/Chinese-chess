import math
import copy

import board
from move_validator import MoveValidator

piece_values = {
    "King": 10000, "Rook": 500, "Cannon": 400, "Knight": 300,
    "Elephant": 200, "Advisor": 150, "Pawn": 100
}

def evaluate_board(black_pieces, red_pieces):
    """Đánh giá bàn cờ (giá trị cao hơn là lợi thế cho AI)"""
    piece_values = {
        "將": 10000, "車": 500, "馬": 300, "包": 400, "象": 200, "士": 150, "卒": 100,
        "帥": -10000, "車": -500, "馬": -300, "炮": -400, "相": -200, "仕": -150, "兵": -100
    }
    score = 0

    for pos, piece in black_pieces.items():
        score += piece_values.get(piece, 0)

    for pos, piece in red_pieces.items():
        score += piece_values.get(piece, 0)

    return score

def minimax(black_pieces, red_pieces, depth, alpha, beta, maximizing):
    """Thuật toán Minimax có cắt tỉa Alpha-Beta"""
    if depth == 0:
        return evaluate_board(black_pieces, red_pieces)

    if maximizing:
        max_eval = -math.inf
        for move in get_all_moves(black_pieces, "black", red_pieces):  # Truyền đủ 3 tham số
            temp_black = copy.deepcopy(black_pieces)
            temp_red = copy.deepcopy(red_pieces)

            if move[1] in temp_red:  # Nếu ăn quân
                del temp_red[move[1]]

            temp_black[move[1]] = temp_black.pop(move[0])

            eval = minimax(temp_black, temp_red, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_all_moves(red_pieces, "red", black_pieces):  # Truyền đủ 3 tham số
            temp_black = copy.deepcopy(black_pieces)
            temp_red = copy.deepcopy(red_pieces)

            if move[1] in temp_black:
                del temp_black[move[1]]

            temp_red[move[1]] = temp_red.pop(move[0])

            eval = minimax(temp_black, temp_red, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_all_moves(pieces, color, other_pieces):
    """Lấy tất cả nước đi hợp lệ của một màu quân"""
    moves = []
    for pos, piece in pieces.items():
        if (color == "black" and piece in ["將", "車", "馬", "包", "象", "士", "卒"]) or \
           (color == "red" and piece in ["帥", "車", "馬", "炮", "相", "仕", "兵"]):
            for x in range(9):
                for y in range(10):
                    if MoveValidator.is_valid_move(piece, pos, (x, y), pieces, other_pieces):
                        moves.append((pos, x, y))
    return moves

def get_best_move(black_pieces, red_pieces, depth=3):
    """Tìm nước đi tốt nhất cho AI (quân Đen)"""
    best_move = None
    best_value = -math.inf

    for move in get_all_moves(black_pieces, "black", red_pieces):
        temp_black = copy.deepcopy(black_pieces)
        temp_red = copy.deepcopy(red_pieces)

        if move[1] in temp_red:  # Nếu ăn quân
            del temp_red[move[1]]

        temp_black[move[1]] = temp_black.pop(move[0])

        move_value = minimax(temp_black, temp_red, depth - 1, -math.inf, math.inf, False)

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

