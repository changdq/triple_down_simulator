import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Match-3 Game")

# 定义颜色
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# 定义方块大小
block_size = 50

# 生成初始游戏网格
grid = [[random.randint(0, len(colors) - 1) for _ in range(width // block_size)] for _ in range(height // block_size)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制网格
    screen.fill((255, 255, 255))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pygame.draw.rect(screen, colors[grid[i][j]], (j * block_size, i * block_size, block_size, block_size))

    pygame.display.flip()

pygame.quit()
