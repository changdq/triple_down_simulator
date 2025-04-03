import pygame

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Rect Width Example")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

screen.fill(LIGHT_GRAY)

# 绘制实心矩形
pygame.draw.rect(screen, BLACK, (50, 50, 100, 100), 0)

# 绘制边框宽度为 2 的空心矩形
pygame.draw.rect(screen, BLACK, (200, 50, 100, 100), 2)

# 更新显示
pygame.display.flip()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出 Pygame
pygame.quit()