import pygame

import config


class GameBoard:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font = pygame.font.Font("assets/simhei.ttf", 30)
        except:
            self.font = pygame.font.Font(None, 30)

    def draw_board(self, black_pieces, red_pieces, valid_moves):
        self.screen.fill(config.WHITE)

        # Vẽ các đường kẻ ngang và dọc
        for i in range(10):
            pygame.draw.line(self.screen, config.BLUE,
                             (config.BOARD_X, config.BOARD_Y + i * config.CELL_SIZE),
                             (config.BOARD_X + config.BOARD_WIDTH, config.BOARD_Y + i * config.CELL_SIZE))
        for i in range(9):
            pygame.draw.line(self.screen, config.BLUE,
                             (config.BOARD_X + i * config.CELL_SIZE, config.BOARD_Y),
                             (config.BOARD_X + i * config.CELL_SIZE, config.BOARD_Y + config.BOARD_HEIGHT))

        # Vẽ "sông"
        pygame.draw.rect(self.screen, config.BLUE,
                        (config.BOARD_X, config.BOARD_Y + 4 * config.CELL_SIZE, config.BOARD_WIDTH, config.CELL_SIZE))

        # Vẽ đường chéo trong cung (mới)
        self.draw_palace_lines()

        # Tô màu bước đi hợp lệ
        for move in valid_moves:
            pygame.draw.circle(self.screen, config.GREEN,
                             (config.BOARD_X + move[0] * config.CELL_SIZE, config.BOARD_Y + move[1] * config.CELL_SIZE),
                             config.CELL_SIZE // 4)

        # Vẽ quân cờ
        for pos, text in black_pieces.items():
            self.draw_piece(pos[0], pos[1], config.BLACK, text)
        for pos, text in red_pieces.items():
            self.draw_piece(pos[0], pos[1], config.RED, text)

        pygame.display.flip()

    def draw_piece(self, x, y, color, text):
        pygame.draw.circle(self.screen, color,
                         (config.BOARD_X + x * config.CELL_SIZE, config.BOARD_Y + y * config.CELL_SIZE),
                         config.CELL_SIZE // 2)
        text_surface = self.font.render(text, True, config.WHITE)
        text_rect = text_surface.get_rect(center=(config.BOARD_X + x * config.CELL_SIZE,
                                                 config.BOARD_Y + y * config.CELL_SIZE))
        self.screen.blit(text_surface, text_rect)

    def draw_palace_lines(self):  # Hàm vẽ đường chéo trong cung
        # Cung đen
        pygame.draw.line(self.screen, config.BLUE,
                         (config.BOARD_X + 3 * config.CELL_SIZE, config.BOARD_Y),
                         (config.BOARD_X + 5 * config.CELL_SIZE, config.BOARD_Y + 2 * config.CELL_SIZE))
        pygame.draw.line(self.screen, config.BLUE,
                         (config.BOARD_X + 5 * config.CELL_SIZE, config.BOARD_Y),
                         (config.BOARD_X + 3 * config.CELL_SIZE, config.BOARD_Y + 2 * config.CELL_SIZE))

        # Cung đỏ
        pygame.draw.line(self.screen, config.BLUE,
                         (config.BOARD_X + 3 * config.CELL_SIZE, config.BOARD_Y + 7 * config.CELL_SIZE),
                         (config.BOARD_X + 5 * config.CELL_SIZE, config.BOARD_Y + 9 * config.CELL_SIZE))
        pygame.draw.line(self.screen, config.BLUE,
                         (config.BOARD_X + 5 * config.CELL_SIZE, config.BOARD_Y + 7 * config.CELL_SIZE),
                         (config.BOARD_X + 3 * config.CELL_SIZE, config.BOARD_Y + 9 * config.CELL_SIZE))

    def draw_timer(self, red_time, black_time):
        font = pygame.font.Font(None, 24)
        red_time_text = font.render(f"Red: {int(red_time)}s", True, config.RED)
        black_time_text = font.render(f"Black: {int(black_time)}s", True, config.BLACK)
        self.screen.blit(red_time_text, (10, 500))
        self.screen.blit(black_time_text, (10, 100))

