import pygame
import random
from core import GameBoard

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

# 加载支持中文的字体，这里以系统自带的宋体为例，不同系统字体路径可能不同
try:
    font = pygame.font.Font("simhei.ttf", 36)  # 尝试加载黑体字体
except FileNotFoundError:
    font = pygame.font.Font(pygame.font.get_default_font(), 36)  # 如果找不到指定字体，使用默认字体


# 绘制游戏板
def draw_board(game_board, screen, animating_block=None):
    screen.fill(LIGHT_GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            if animating_block and (row, col) == animating_block:
                continue
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


# 方块缩小动画
def shrink_block_animation(row, col, game_board, screen):
    shrink_factor = 1.0
    while shrink_factor > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # 清除屏幕
        # screen.fill(LIGHT_GRAY)
        draw_board(game_board, screen, animating_block=(row, col))
        block = game_board.board[row][col]
        if block:
            x1 = col * BLOCK_SIZE + PADDING
            y1 = row * BLOCK_SIZE + PADDING
            new_size = int(BLOCK_SIZE * shrink_factor)
            offset = (BLOCK_SIZE - new_size) // 2
            color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
            pygame.draw.rect(screen, color, (x1 + offset, y1 + offset, new_size, new_size))
            pygame.draw.rect(screen, BLACK, (x1 + offset, y1 + offset, new_size, new_size), 2)
            text = font.render(str(block.block_type), True, BLACK)
            text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(50)
        shrink_factor -= 0.1
    # 移除方块
    game_board.board[row][col] = None
    return True


if __name__ == "__main__":
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("三消游戏")

    # 初始化游戏板
    type_probs = [0.2, 0.2, 0.2, 0.2, 0]
    initial_steps = 10
    max_block_level = 5
    game_board = GameBoard(ROWS, COLS, type_probs, max_block_level, initial_steps)

    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if PADDING <= x < WIDTH + PADDING and PADDING <= y < HEIGHT + PADDING:
                    col = (x - PADDING) // BLOCK_SIZE
                    row = (y - PADDING) // BLOCK_SIZE
                    if game_board.board[row][col]:
                        if not shrink_block_animation(row, col, game_board, screen):
                            running = False

        draw_board(game_board, screen)
        pygame.display.flip()

    pygame.quit()