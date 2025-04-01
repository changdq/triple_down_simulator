import pygame
import random
from main import GameBoard

# 初始化 Pygame
pygame.init()

# 定义常量
ROWS = 8
COLS = 8
BLOCK_SIZE = 50
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
PADDING = 5
WINDOW_WIDTH = WIDTH + 2 * PADDING
WINDOW_HEIGHT = HEIGHT + 2 * PADDING + 50  # 增加高度用于显示步数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# 定义方块颜色，使用更柔和的色调
COLORS = [(255, 102, 102), (102, 255, 102), (102, 102, 255), (255, 255, 102), (255, 178, 102)]

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("三消游戏")

# 初始化游戏板
type_probs = [0.2, 0.2, 0.2, 0.2, 0]
initial_steps = 10
max_block_level = 5
game_board = GameBoard(ROWS, COLS, type_probs, max_block_level, initial_steps)

# 加载字体
font = pygame.font.Font(None, 36)

# 绘制游戏板
def draw_board():
    screen.fill(LIGHT_GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            block = game_board.board[row][col]
            if block:
                x1 = col * BLOCK_SIZE + PADDING
                y1 = row * BLOCK_SIZE + PADDING
                x2 = x1 + BLOCK_SIZE
                y2 = y1 + BLOCK_SIZE
                color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
                pygame.draw.rect(screen, color, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x1, y1, BLOCK_SIZE, BLOCK_SIZE), 2)  # 添加边框
                text = font.render(str(block.block_type), True, BLACK)
                text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)

    # 显示剩余步数
    steps_text = font.render(f"剩余步数: {game_board.remaining_steps}", True, BLACK)
    screen.blit(steps_text, (PADDING, HEIGHT + PADDING + 10))

# 消除动画
def elimination_animation(matches):
    shrink_factor = 0.1
    while shrink_factor > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        draw_board()
        for row, col in matches:
            x1 = col * BLOCK_SIZE + PADDING
            y1 = row * BLOCK_SIZE + PADDING
            new_size = int(BLOCK_SIZE * shrink_factor)
            offset = (BLOCK_SIZE - new_size) // 2
            block = game_board.board[row][col]
            color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
            pygame.draw.rect(screen, color, (x1 + offset, y1 + offset, new_size, new_size))
            pygame.draw.rect(screen, BLACK, (x1 + offset, y1 + offset, new_size, new_size), 2)
            text = font.render(str(block.block_type), True, BLACK)
            text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(50)
        shrink_factor -= 0.05
    return True

# 主循环
running = True
selected_block = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if PADDING <= x < WIDTH + PADDING and PADDING <= y < HEIGHT + PADDING:
                col = (x - PADDING) // BLOCK_SIZE
                row = (y - PADDING) // BLOCK_SIZE
                if selected_block is None:
                    selected_block = (row, col)
                else:
                    x1, y1 = selected_block
                    x2, y2 = row, col
                    if (abs(x1 - x2) + abs(y1 - y2)) == 1:
                        game_board.swap_blocks(x1, y1, x2, y2)
                        matches = game_board.find_matches()
                        if matches:
                            if not elimination_animation(matches):
                                running = False
                            game_board.remove_matches(game_board.group_matches(matches))
                            game_board.fill_empty_spaces()
                    selected_block = None

    draw_board()
    pygame.display.flip()

pygame.quit()