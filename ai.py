
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
        best_move = None
        best_match_length = 0
        best_block_type = 0

        for row in range(game_board.rows):
            for col in range(game_board.cols):
                # 尝试交换右边的方块
                if col < game_board.cols - 1:
                    game_board.board[row][col], game_board.board[row][col + 1] = game_board.board[row][col + 1], game_board.board[row][col]
                    matches = game_board.find_matches()
                    grouped_matches = game_board.group_matches(matches)
                    max_match_length = max([len(group) for group in grouped_matches], default=0)
                    max_block_type = max([game_board.board[r][c].block_type for r, c in matches], default=0) if matches else 0

                    if max_match_length >= 4 and max_match_length > best_match_length:
                        best_move = (row, col, row, col + 1)
                        best_match_length = max_match_length
                        best_block_type = max_block_type
                    elif max_match_length == best_match_length and max_block_type > best_block_type:
                        best_move = (row, col, row, col + 1)
                        best_block_type = max_block_type
                    elif max_match_length <= 3 and max_match_length > 0 and max_block_type > best_block_type and best_match_length <= 3:
                        best_move = (row, col, row, col + 1)
                        best_block_type = max_block_type

                    game_board.board[row][col], game_board.board[row][col + 1] = game_board.board[row][col + 1], game_board.board[row][col]

                # 尝试交换下边的方块
                if row < game_board.rows - 1:
                    game_board.board[row][col], game_board.board[row + 1][col] = game_board.board[row + 1][col], game_board.board[row][col]
                    matches = game_board.find_matches()
                    grouped_matches = game_board.group_matches(matches)
                    max_match_length = max([len(group) for group in grouped_matches], default=0)
                    max_block_type = max([game_board.board[r][c].block_type for r, c in matches], default=0) if matches else 0

                    if max_match_length >= 4 and max_match_length > best_match_length:
                        best_move = (row, col, row + 1, col)
                        best_match_length = max_match_length
                        best_block_type = max_block_type
                    elif max_match_length == best_match_length and max_block_type > best_block_type:
                        best_move = (row, col, row + 1, col)
                        best_block_type = max_block_type
                    elif max_match_length <= 3 and max_match_length > 0 and max_block_type > best_block_type and best_match_length <= 3:
                        best_move = (row, col, row + 1, col)
                        best_block_type = max_block_type

                    game_board.board[row][col], game_board.board[row + 1][col] = game_board.board[row + 1][col], game_board.board[row][col]

        if best_move:
            return best_move
            #x1, y1, x2, y2 = best_move
            #game_board.swap_blocks(x1, y1, x2, y2)
        else:
            print("AI 未找到合适的移动，步数不消耗。")