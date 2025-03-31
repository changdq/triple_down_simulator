import tkinter as tk
from main import GameBoard

# 方块大小
BLOCK_SIZE = 50

class GameUI:
    def __init__(self, root, rows, cols, type_probs, max_block_level, initial_steps):
        self.root = root
        self.root.title("三消游戏")
        self.game_board = GameBoard(rows, cols, type_probs, max_block_level, initial_steps)
        self.canvas = tk.Canvas(root, width=cols * BLOCK_SIZE, height=rows * BLOCK_SIZE)
        self.canvas.pack()
        self.draw_board()
        self.selected_block = None
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.game_board.rows):
            for col in range(self.game_board.cols):
                block = self.game_board.board[row][col]
                if block:
                    x1 = col * BLOCK_SIZE
                    y1 = row * BLOCK_SIZE
                    x2 = x1 + BLOCK_SIZE
                    y2 = y1 + BLOCK_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.get_block_color(block.block_type))
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(block.block_type))

    def get_block_color(self, block_type):
        # 根据方块类型返回不同颜色
        colors = ["red", "green", "blue", "yellow", "orange"]
        return colors[block_type - 1] if block_type - 1 < len(colors) else "gray"

    def on_click(self, event):
        col = event.x // BLOCK_SIZE
        row = event.y // BLOCK_SIZE
        if self.selected_block is None:
            self.selected_block = (row, col)
        else:
            x1, y1 = self.selected_block
            x2, y2 = row, col
            if (abs(x1 - x2) + abs(y1 - y2)) == 1:
                self.game_board.swap_blocks(x1, y1, x2, y2)
                self.draw_board()
            self.selected_block = None

def main():
    rows = 8
    cols = 8
    type_probs = [0.2, 0.2, 0.2, 0.2, 0]
    initial_steps = 10
    max_block_level = 5
    root = tk.Tk()
    game_ui = GameUI(root, rows, cols, type_probs, max_block_level, initial_steps)
    root.mainloop()

if __name__ == "__main__":
    main()