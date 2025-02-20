class PieceData:
    @staticmethod
    def get_initial_pieces():
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

        return black_pieces, red_pieces