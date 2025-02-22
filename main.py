import pygame
import config
from ai import ChessAI
from pieces import PieceData
from move_validator import MoveValidator
from board import GameBoard
from timer_manager import TimerManager
from captured_pieces import CapturedPieces



def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Cờ Tướng")

    board = GameBoard(screen)
    timer_manager = TimerManager(600)  # 10 phút
    captured_pieces = CapturedPieces(screen)
    black_pieces, red_pieces = PieceData.get_initial_pieces()

    # Khởi tạo AI cho bên đen
    ai = ChessAI(is_red=False)

    red_turn = True
    selected_piece = None
    valid_moves = []

    running = True
    while running:
        timer_manager.update_timers()
        red_time, black_time = timer_manager.get_times()

        # Kiểm tra hết giờ
        if red_time <= 0:
            print("Bên Đen thắng do bên Đỏ hết thời gian!")
            running = False
        elif black_time <= 0:
            print("Bên Đỏ thắng do bên Đen hết thời gian!")
            running = False

        # Lượt của AI (bên đen)
        if not red_turn and running:
            pygame.time.delay(500)  # Tạo độ trễ giúp người chơi dễ theo dõi
            move = ai.get_best_move(red_pieces, black_pieces)

            if move:
                start_pos, end_pos = move

                # Kiểm tra xem start_pos có tồn tại trong black_pieces không
                if start_pos not in black_pieces:
                    print(f"AI chọn nước đi không hợp lệ: {start_pos} -> {end_pos}")
                    continue  # Bỏ qua nước đi này và thử lại trong vòng lặp tiếp theo

                # Nếu AI ăn quân
                if end_pos in red_pieces:
                    captured_piece = red_pieces.pop(end_pos)
                    captured_pieces.add_captured_piece(captured_piece, False)

                    if captured_piece == "帥":  # Nếu ăn tướng đỏ
                        print("Bên Đen thắng!")
                        running = False

                black_pieces[end_pos] = black_pieces.pop(start_pos)
                red_turn = True
                timer_manager.switch_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:  # Xử lý thay đổi kích thước cửa sổ
                config.SCREEN_WIDTH, config.SCREEN_HEIGHT = event.size
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                board.screen = screen  # Cập nhật màn hình của bàn cờ
                captured_pieces.screen = screen  # Cập nhật màn hình hiển thị quân bị ăn

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x = (x - config.BOARD_X) // config.CELL_SIZE
                grid_y = (y - config.BOARD_Y) // config.CELL_SIZE

                pieces = red_pieces if red_turn else black_pieces
                other_pieces = black_pieces if red_turn else red_pieces

                if (grid_x, grid_y) in pieces:
                    # Chọn quân cờ
                    selected_piece = (grid_x, grid_y)
                    valid_moves = MoveValidator.generate_valid_moves(
                        pieces[selected_piece], selected_piece, pieces, other_pieces
                    )

                elif selected_piece and (grid_x, grid_y) in valid_moves:
                    # Nếu ăn quân đối phương
                    if (grid_x, grid_y) in other_pieces:
                        captured_piece = other_pieces.pop((grid_x, grid_y))
                        captured_pieces.add_captured_piece(captured_piece, red_turn)

                        # Kiểm tra nếu vua bị ăn
                        if captured_piece in ["將", "帥"]:
                            if captured_piece == "將":
                                print("Bên Đỏ thắng! Vua Đen bị ăn.")
                            else:
                                print("Bên Đen thắng! Vua Đỏ bị ăn.")
                            running = False  # Kết thúc trò chơi

                    # Di chuyển quân cờ
                    pieces[(grid_x, grid_y)] = pieces.pop(selected_piece)

                    # Chuyển lượt và cập nhật thời gian
                    red_turn = not red_turn
                    timer_manager.switch_turn()

                    # Reset lựa chọn
                    selected_piece = None
                    valid_moves = []

        board.draw_board(black_pieces, red_pieces, valid_moves)
        captured_pieces.draw_captured_pieces()
        board.draw_timer(red_time, black_time)
        pygame.display.flip()

        pygame.time.delay(50)

    pygame.quit()


if __name__ == "__main__":
    main()