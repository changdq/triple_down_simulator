import unittest
import pygame
from unittest.mock import patch
from ui import elimination_animation
from core import GameBoard  

# Todo: 还有bug，unittest这个库还没完全用明白
class TestEliminationAnimation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        # 初始化一个简单的 GameBoard 实例
        self.rows = 8
        self.cols = 8
        type_probs = [0.2, 0.2, 0.2, 0.2, 0]
        initial_steps = 10
        max_block_level = 5
        self.game_board = GameBoard(self.rows, self.cols, type_probs, max_block_level, initial_steps)

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


        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


    @patch('pygame.display.flip')
    @patch('pygame.time.delay')
    def test_elimination_animation_normal(self, mock_delay, mock_flip):
        # 模拟一些匹配的方块
        matches = [(1, 1), (1, 2), (1, 3)]
        with patch('ui.draw_board') as mock_draw_board:
            result = elimination_animation(matches,gameboard,screen)
            self.assertEqual(isinstance(result, bool), True)
            # 检查 draw_board 是否被调用
            self.assertEqual(mock_draw_board.call_count > 0, True)
            # 检查 delay 和 flip 是否被调用
            self.assertEqual(mock_delay.call_count > 0, True)
            self.assertEqual(mock_flip.call_count > 0, True)


if __name__ == '__main__':
    unittest.main()
