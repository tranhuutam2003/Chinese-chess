import pygame

# Khai báo kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Khai báo màu sắc
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Khai báo kích thước ô cờ
CELL_SIZE = 40

# Kích thước bàn cờ
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE

# Tính toán vị trí bắt đầu vẽ bàn cờ
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2