
from abc import ABC, abstractmethod

class BaseAI(ABC):
    """
    所有 AI 策略的基类，定义了 AI 接口。
    """
    @abstractmethod
    def get_move(self, game_board):
        """
        获取 AI 的移动决策。

        参数:
        game_board (GameBoard): 当前的游戏棋盘。

        返回:
        tuple: 表示移动的元组 (x1, y1, x2, y2)，其中 (x1, y1) 和 (x2, y2) 是要交换的两个方块的坐标。
        """
        pass

class GreedyAI(BaseAI):
    """
    简单的贪心 AI 策略示例。
    """
    def get_move(self, game_board):
        # 这里可以实现贪心算法逻辑，暂时返回一个示例移动
        rows = len(game_board.board)
        cols = len(game_board.board[0])
        x1, y1 = 0, 0
        x2, y2 = 0, 1
        if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
            return (x1, y1, x2, y2)
        return None