# 单独测试一下fill in blank 的逻辑

from ui import *

# 初始化 Pygame
pygame.init()

# 定义常量
ROWS = 8
COLS = 8
BLOCK_SIZE = 50
WIDTH = COLS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
PADDING = 0
WINDOW_WIDTH = WIDTH + 2 * PADDING
WINDOW_HEIGHT = HEIGHT + 2 * PADDING + 50  # 增加高度用于显示步数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
SELECTED_COLOR = (255, 255, 0)  # 选中方块的颜色

# 定义方块颜色，使用更柔和的色调
COLORS = [(255, 102, 102), (102, 255, 102), (102, 102, 255), (255, 255, 102), (255, 178, 102)]

# 加载支持中文的字体，这里以系统自带的宋体为例，不同系统字体路径可能不同
try:
    font = pygame.font.Font("simhei.ttf", 36)  # 尝试加载黑体字体
except FileNotFoundError:
    font = pygame.font.Font(pygame.font.get_default_font(), 36)  # 如果找不到指定字体，使用默认字体


if __name__ == "__main__":
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("三消游戏")

    # 初始化游戏板
    type_probs = [0.2, 0.2, 0.2, 0.2, 0]
    initial_steps = 10
    max_block_level = 5
    game_board = GameBoard(ROWS, COLS, type_probs, max_block_level, initial_steps)

    falling_blocks = [(1, 0, 2, 0), (0, 0, 1, 0), (1, 2, 2, 2), (0, 2, 1, 2)]
    new_blocks = [(0, 0, 1), (0, 2, 2)]
    moving_blocks = [(1, 0), (2, 0), (0, 0), (1, 2), (2, 2), (0, 2)]


    # 主循环
    running = True
    selected_block = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         x, y = event.pos
        #         if PADDING <= x < WIDTH + PADDING and PADDING <= y < HEIGHT + PADDING:
        #             col = (x - PADDING) // BLOCK_SIZE
        #             row = (y - PADDING) // BLOCK_SIZE
        #             if selected_block is None:
        #                 selected_block = (row, col)
        #             else:
        #                 x1, y1 = selected_block
        #                 x2, y2 = row, col
        #                 if (abs(x1 - x2) + abs(y1 - y2)) == 1:
        #                     if not swap_animation(game_board, screen, x1, y1, x2, y2):
        #                         running = False
        #                     matches = game_board.find_matches()
        #                     if matches:
        #                         if not elimination_animation(matches, game_board, screen):
        #                             running = False

        #                         # 得到需要生成新方块的位置，同时处理掉旧的位置的数据
        #                         new_blocks = game_board.get_new_block_pos(matches,swap_pos=(x2,y2)) 
                        
        #                         # 生成新方块动画
        #                         generate_block_animation(matches,new_blocks,game_board,screen)

        #                         # 填充，先不循环填充测试一下
        #                         fill_empty_spaces_animation(game_board, screen)

        #                     else: # 如果没有matchs，再交换回来
        #                         swap_animation(game_board, screen, x2, y2, x1, y1)
        #                 selected_block = None

        draw_board(game_board, screen, selected_block, moving_blocks=moving_blocks)
        pygame.display.flip()

    pygame.quit()    