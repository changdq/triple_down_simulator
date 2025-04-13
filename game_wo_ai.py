import pygame
import random
from core import GameBoard
import time 

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
WINDOW_HEIGHT = HEIGHT + 2 * PADDING + 100  # 增加高度用于显示步数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
SELECTED_COLOR = (255, 128, 0)  # 选中方块的颜色

GAME_SPEED = 3

# 定义方块颜色，使用更柔和的色调
COLORS = [(255, 102, 102), (102, 255, 102), (102, 102, 255), (255, 255, 102), (255, 178, 102)]

# 加载支持中文的字体，这里以系统自带的宋体为例，不同系统字体路径可能不同
try:
    font = pygame.font.Font("simhei.ttf", 36)  # 尝试加载黑体字体
except FileNotFoundError:
    font = pygame.font.Font(pygame.font.get_default_font(), 36)  # 如果找不到指定字体，使用默认字体


# 绘制游戏板
def draw_board(game_board, screen, selected_block=None, moving_blocks = None):
    screen.fill(LIGHT_GRAY)
    for row in range(ROWS):
        for col in range(COLS):
            block = game_board.board[row][col]

            # 还是需要moving_blocks 和 None共同控制填充
            if (moving_blocks is not None) and ((row,col) in moving_blocks):
                #print((row,col))
                # x1 = col * BLOCK_SIZE + PADDING
                # y1 = row * BLOCK_SIZE + PADDING
                # pygame.draw.rect(screen, BLACK, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))
                continue
                

            if block:
                x1 = col * BLOCK_SIZE + PADDING
                y1 = row * BLOCK_SIZE + PADDING
                #x2 = x1 + BLOCK_SIZE
                #y2 = y1 + BLOCK_SIZE
                color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
                pygame.draw.rect(screen, color, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x1, y1, BLOCK_SIZE, BLOCK_SIZE), 2)  # 添加边框
                text = font.render(str(block.block_type), True, BLACK)
                text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)

            if selected_block and (row, col) == selected_block:
                x1 = col * BLOCK_SIZE + PADDING
                y1 = row * BLOCK_SIZE + PADDING
                pygame.draw.rect(screen, SELECTED_COLOR, (x1, y1, BLOCK_SIZE, BLOCK_SIZE), 4)

    # 显示剩余步数
    steps_text = font.render(f"Remaining steps: {game_board.remaining_steps}", True, BLACK)
    screen.blit(steps_text, (PADDING, HEIGHT + PADDING + 10))
    # 显示已用步数
    steps_text = font.render(f"Action steps: {game_board.total_steps}", True, BLACK)
    screen.blit(steps_text, (PADDING, HEIGHT + PADDING + 50))
    pygame.display.flip()


# 交换两个相邻方块的动画效果
def swap_animation(game_board, screen, x1, y1, x2, y2):
    frames = 10 
    dx = (x2 - x1) * BLOCK_SIZE / frames
    dy = (y2 - y1) * BLOCK_SIZE / frames
    for j in range(frames):
        i = j+1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        draw_board(game_board, screen, moving_blocks=[(x1,y1),(x2,y2)])
        block1 = game_board.board[x1][y1]
        block2 = game_board.board[x2][y2]
        if block1:
            y = x1 * BLOCK_SIZE + PADDING + i * dx
            x = y1 * BLOCK_SIZE + PADDING + i * dy
            color = COLORS[block1.block_type - 1] if block1.block_type - 1 < len(COLORS) else (128, 128, 128)
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2)
            text = font.render(str(block1.block_type), True, BLACK)
            text_rect = text.get_rect(center=(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
        if block2:
            y = x2 * BLOCK_SIZE + PADDING - i * dx
            x = y2 * BLOCK_SIZE + PADDING - i * dy
            color = COLORS[block2.block_type - 1] if block2.block_type - 1 < len(COLORS) else (128, 128, 128)
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2)
            text = font.render(str(block2.block_type), True, BLACK)
            text_rect = text.get_rect(center=(x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(int(20/GAME_SPEED))

    return True


# 消除动画
def elimination_animation(matches, game_board, screen):
    shrink_factor = 1.0 
    while shrink_factor > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        #screen.fill(LIGHT_GRAY)
        draw_board(game_board, screen, moving_blocks=matches)
        #draw_board(game_board, screen)
        for row, col in matches:
            block = game_board.board[row][col]
            if block:
                x1 = col * BLOCK_SIZE + PADDING
                y1 = row * BLOCK_SIZE + PADDING
                new_size = int(BLOCK_SIZE * shrink_factor)
                offset = (BLOCK_SIZE - new_size) // 2
                color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
                pygame.draw.rect(screen, color, (x1 + offset, y1 + offset, new_size, new_size))
                pygame.draw.rect(screen, BLACK, (x1 + offset, y1 + offset, new_size, new_size), 2)
                new_font_size = int(36 * shrink_factor)
                new_font = pygame.font.Font(pygame.font.get_default_font(), new_font_size)
                text = new_font.render(str(block.block_type), True, BLACK)
                text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(int(50/GAME_SPEED))
        shrink_factor -= 0.1 
    return True

# 在指定位置生成方块的动画
def generate_block_animation(matches, new_blocks, game_board, screen):
#def generate_block_animation(row, col, block_type, game_board, screen):
    grow_factor = 0.1
    while grow_factor <= 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        # 
        draw_board(game_board, screen, moving_blocks=matches)

        for row,col,block_type in new_blocks:
            x1 = col * BLOCK_SIZE + PADDING
            y1 = row * BLOCK_SIZE + PADDING
            new_size = int(BLOCK_SIZE * grow_factor)
            offset = (BLOCK_SIZE - new_size) // 2
            color = COLORS[block_type - 1] if block_type - 1 < len(COLORS) else (128, 128, 128)
            pygame.draw.rect(screen, color, (x1 + offset, y1 + offset, new_size, new_size))
            pygame.draw.rect(screen, BLACK, (x1 + offset, y1 + offset, new_size, new_size), 2)
            new_font_size = int(36 * grow_factor)
            new_font = pygame.font.Font(pygame.font.get_default_font(), new_font_size)
            text = new_font.render(str(block_type), True, BLACK)
            text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(int(20/GAME_SPEED))
        grow_factor += 0.1
    #game_board.board[row][col] = GameBoard.Block(block_type)
    return True

# 消除和生成新block之后的掉落动画:
def fill_empty_spaces_animation(game_board, screen, falling_blocks, new_blocks):
  
    # 把信息做成动画，应该是匀速下落，到了指定位置的方块就不再下落。
    # new_blocks可以假设初始位置是在棋盘外面的某个位置开始下落的。
    speed = 5  # 下落速度, 5帧下降一个block的size
    # 计算掉落需要的帧数
    max_gap = 0
    max_new_gap = 0
    moving_blocks = []

    for start_row, start_col, end_row, end_col in falling_blocks:
        max_gap = max(max_gap,end_row-start_row)
        # 先低效实现
        for i in range(start_row,end_row+1):
            if (i,start_col) not in moving_blocks:
                moving_blocks.append((i,start_col))

    for row, col, block_type in new_blocks:
        max_gap = max(max_gap,row+1)
        # 处理新方块掉落位置时用
        max_new_gap = max(max_new_gap,row+1)
        for i in range(row+1):
            if (i,col) not in moving_blocks:
                moving_blocks.append((i,col))


    frames = speed * max_gap +1
    new_block_frames = speed * max_new_gap

    #print(moving_blocks)
    #game_board.display_board()
    
    #time.sleep(60)
    for i in range(frames):
        # 绘制下落的方块
        #screen.fill(LIGHT_GRAY)
        draw_board(game_board, screen, moving_blocks=moving_blocks)      

        #time.sleep(60)  

        if falling_blocks:
            for start_row, start_col, end_row, end_col in falling_blocks:
                block = game_board.board[end_row][end_col]
                #y_offset = (end_row - start_row) * BLOCK_SIZE * i * (BLOCK_SIZE / speed)
                y_offset = i * (BLOCK_SIZE / speed)
                x1 = start_col * BLOCK_SIZE + PADDING
                y1 = start_row * BLOCK_SIZE + PADDING + y_offset
                # 到目标位置就停住
                y1 = min(y1, end_row * BLOCK_SIZE + PADDING)

                color = COLORS[block.block_type - 1] if block.block_type - 1 < len(COLORS) else (128, 128, 128)
                pygame.draw.rect(screen, color, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x1, y1, BLOCK_SIZE, BLOCK_SIZE), 2)  # 添加边框
                text = font.render(str(block.block_type), True, BLACK)
                text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)

        # 绘制新生成的方块
        # 新方块一定是在最上面的连续位置，根据最大位置反推该出现的位置。
        if new_blocks:
            for row, col, block_type in new_blocks:
                y1 = row * BLOCK_SIZE - (new_block_frames - i) * (BLOCK_SIZE / speed)
                x1 = col * BLOCK_SIZE + PADDING
                #y1 = -y_offset + PADDING
                color = COLORS[block_type - 1] if block_type - 1 < len(COLORS) else (128, 128, 128)
                pygame.draw.rect(screen, color, (x1, y1, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x1, y1, BLOCK_SIZE, BLOCK_SIZE), 2)  # 添加边框
                text = font.render(str(block_type), True, BLACK)
                text_rect = text.get_rect(center=(x1 + BLOCK_SIZE // 2, y1 + BLOCK_SIZE // 2))
                screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.delay(int(50/GAME_SPEED))

# 重新打乱棋盘的动画，原始棋盘全部渐出，新棋盘全部渐入：
def reshuffle_animation(game_board, screen,all_pos, all_blocks):
    elimination_animation(all_pos,game_board, screen)
    generate_block_animation(all_pos, all_blocks, game_board,screen)
    

# 显示游戏结束界面
def show_game_over_screen(game_board, screen):
    screen.fill(LIGHT_GRAY)
    game_over_text = font.render("Game Over！", True, BLACK)
    total_steps_text = font.render(f"Total Steps: {game_board.total_steps}", True, BLACK)
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    screen.blit(total_steps_text, (WINDOW_WIDTH // 2 - total_steps_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == "__main__":
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("三消游戏")

    # 初始化游戏板
    type_probs = [0.2, 0.2, 0.2, 0.2, 0]
    initial_steps = 10
    max_block_level = 5

    game_board = GameBoard(ROWS, COLS, type_probs, max_block_level, initial_steps)


    # 显示初始棋盘。先放在这里
    draw_board(game_board, screen)
    pygame.display.flip()

    #move_type = input("请选择移动方式 (1: 玩家输入, 2: AI 移动): ")

    # 主循环
    running = True
    selected_block = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if PADDING <= x < WIDTH + PADDING and PADDING <= y < HEIGHT + PADDING:
                    col = (x - PADDING) // BLOCK_SIZE
                    row = (y - PADDING) // BLOCK_SIZE
                    if selected_block is None:
                        selected_block = (row, col)
                        # draw_board(game_board, screen, selected_block=selected_block)
                        # pygame.display.flip()
                    else:
                        x1, y1 = selected_block
                        x2, y2 = row, col
                        if (abs(x1 - x2) + abs(y1 - y2)) == 1:
                            swap_animation(game_board, screen, x1, y1, x2, y2)
                             # 只是交换borad取值。
                            game_board.swap_blocks_ui(x1, y1, x2, y2)     

                            matches = game_board.find_matches()
                            if not matches:
                                swap_animation(game_board, screen, x2, y2, x1, y1)
                                game_board.swap_blocks_ui(x2, y2, x1, y1)
                            # 处理连续消除
                            # 加一个Flag处理连续消除中的swap_pos参数
                            is_subsequent_eliminate = False

                            # 成功交换则增加已用步数 + 1
                            game_board.increase_total_steps()
                            

                            # 每次while循环整体结算一次步数,每次match统计
                            max_len_list = []
                            
                            while matches:
                                elimination_animation(matches, game_board, screen)
                                
                                max_len_list.append(game_board.get_max_match_len(matches))

                                # 得到需要生成新方块的位置，同时处理掉旧的位置的数据
                                if not is_subsequent_eliminate:
                                    new_blocks = game_board.remove_matches_ui(matches,swap_pos=[(x1,y1),(x2,y2)])
                                else:
                                    # Todo: 需要连续判断是否有matches:
                                    #while game_board.find_matches() is not None:
                                    new_blocks = game_board.remove_matches_ui(matches)

                                
                                # 生成新方块动画
                                generate_block_animation(matches,new_blocks,game_board,screen)

                                #is_subsequent_eliminate = True

                                subsequent_matches = game_board.find_matches()
                                # 掉落新方块之前就需要判断是否还有连续匹配：
                                while subsequent_matches:
                                    max_len_list.append(game_board.get_max_match_len(subsequent_matches))

                                    elimination_animation(subsequent_matches, game_board, screen) 
                                    new_blocks = game_board.remove_matches_ui(subsequent_matches)
                                    # 这个函数需要处理一下
                                    generate_block_animation(subsequent_matches, new_blocks, game_board, screen)
                                    subsequent_matches = game_board.find_matches()

                                # 填充，先不循环填充测试一下
                                # 获取掉落和生成信息
                                falling_blocks, new_blocks = game_board.fill_empty_spaces_ui()  
                                fill_empty_spaces_animation(game_board, screen, falling_blocks, new_blocks)
                                # For debug
                                #time.sleep(60)
                                matches = game_board.find_matches()
                                is_subsequent_eliminate = True

                            is_subsequent_eliminate = False 
                            # 根据   max_len_list 更新步数
                            game_board.update_steps_ui(max_len_list)

                            # 判断是否game_over
                            if game_board.is_game_over():
                                show_game_over_screen(game_board,screen)
                                running = False

                        selected_block = None


        # 处理鼠标选中
        draw_board(game_board, screen,selected_block=selected_block)
        pygame.display.flip()                        

        # 检查棋盘是否stuck
        if game_board.is_board_stuck():
            all_pos,all_blocks = game_board.reshuffle_board_ui()
            reshuffle_animation(game_board, screen, all_pos, all_blocks)

    pygame.quit()