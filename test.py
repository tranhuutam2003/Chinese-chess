import pygame

pygame.init()

# Khai báo kích thước màn hình
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cờ Tướng")

# Khai báo màu sắc
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

# Khai báo kích thước ô cờ
cell_size = 40

# Kích thước bàn cờ (10 hàng, 9 cột)
board_width = 8 * cell_size
board_height = 9 * cell_size

# Tính toán vị trí bắt đầu vẽ bàn cờ
board_x = (screen_width - board_width) // 2
board_y = (screen_height - board_height) // 2

# Font chữ
try:
    font = pygame.font.Font("assets/simhei.ttf", 30)  # SimHei là font phổ biến hỗ trợ tiếng Trung
except:
    font = pygame.font.Font(None, 30)

# Dữ liệu quân cờ
black_pieces = {
    (4, 0): "將", (0, 0): "車", (8, 0): "車", (1, 0): "馬", (7, 0): "馬",
    (2, 0): "象", (6, 0): "象", (3, 0): "士", (5, 0): "士",
    (1, 2): "包", (7, 2): "包"
}
for i in range(5):
    black_pieces[(i * 2, 3)] = "卒"

red_pieces = {}
for (x, y), text in black_pieces.items():
    red_text = text.replace("將", "帥").replace("卒", "兵").replace("包", "炮").replace("象", "相").replace("士", "仕")
    red_pieces[(x, 9 - y)] = red_text

# Biến lưu lượt chơi (True là đỏ, False là đen)
red_turn = True
selected_piece = None
valid_moves = []

# Hàm vẽ bàn cờ và quân cờ
def draw_board():
    screen.fill(white)

    # Vẽ các đường kẻ ngang và dọc
    for i in range(10):
        pygame.draw.line(screen, blue, (board_x, board_y + i * cell_size), (board_x + board_width, board_y + i * cell_size))
    for i in range(9):
        pygame.draw.line(screen, blue, (board_x + i * cell_size, board_y), (board_x + i * cell_size, board_y + board_height))

    # Vẽ "sông"
    pygame.draw.rect(screen, blue, (board_x, board_y + 4 * cell_size, board_width, cell_size))

    # Tô màu bước đi hợp lệ
    for move in valid_moves:
        pygame.draw.circle(screen, green, (board_x + move[0] * cell_size, board_y + move[1] * cell_size), cell_size // 4)

    # Vẽ quân cờ
    for pos, text in black_pieces.items():
        draw_piece(pos[0], pos[1], black, text)
    for pos, text in red_pieces.items():
        draw_piece(pos[0], pos[1], red, text)

    pygame.display.flip()

def draw_piece(x, y, color, text):
    pygame.draw.circle(screen, color, (board_x + x * cell_size, board_y + y * cell_size), cell_size // 2)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(board_x + x * cell_size, board_y + y * cell_size))
    screen.blit(text_surface, text_rect)

# Hàm kiểm tra nước đi hợp lệ
def is_valid_move(piece, current_pos, new_pos, pieces, other_pieces):
    x, y = current_pos
    new_x, new_y = new_pos

    if piece == "卒" or piece == "兵":  # Tốt/Binh
        direction = 1 if piece == "卒" else -1  # Hướng đi của tốt/binh
        if new_x == x and new_y == y + direction: # đi lên 1 ô
            return True
    elif piece == "將" or piece == "帥": # Tướng/Soái
        dx = abs(new_x - x)
        dy = abs(new_y - y)
        if dx <= 1 and dy <= 1 and new_y >= 0 and new_y <= 9 and new_x >= 0 and new_x <= 8:
            return True
    elif piece == "車": # Xe
        if new_x == x or new_y == y:
            return True
    elif piece == "馬": # Mã
        dx = abs(new_x - x)
        dy = abs(new_y - y)
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return True
    elif piece == "象" or piece == "相": # Tượng/Tướng
        dx = abs(new_x - x)
        dy = abs(new_y - y)
        if dx == 2 and dy == 2:
            return True
    elif piece == "士" or piece == "仕": # Sĩ
        dx = abs(new_x - x)
        dy = abs(new_y - y)
        if dx == 1 and dy == 1:
            return True
    elif piece == "包" or piece == "炮": # Pháo
        if new_x == x or new_y == y:
            return True

    return False  # Nước đi không hợp lệ

# Hàm tạo danh sách nước đi hợp lệ
def generate_valid_moves(piece, current_pos, pieces, other_pieces):
    valid_moves = []
    for i in range(10):
        for j in range(9):
            if is_valid_move(piece, current_pos, (j, i), pieces, other_pieces):
                valid_moves.append((j, i))
    return valid_moves

# Chạy vòng lặp chính
running = True
while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = (x - board_x) // cell_size
            grid_y = (y - board_y) // cell_size

            pieces = red_pieces if red_turn else black_pieces
            other_pieces = black_pieces if red_turn else red_pieces

            if (grid_x, grid_y) in pieces:  # Chọn quân cờ
                selected_piece = (grid_x, grid_y)
                valid_moves = generate_valid_moves(pieces[selected_piece], selected_piece, pieces, other_pieces)
            elif selected_piece and (grid_x, grid_y) in valid_moves:
                pieces[(grid_x, grid_y)] = pieces.pop(selected_piece)
                red_turn = not red_turn
                selected_piece = None
                valid_moves = []

pygame.quit()
