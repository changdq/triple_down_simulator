
from abc import ABC, abstractmethod
import copy

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

class OneStepGreedyAI(BaseAI):
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


# 还可以细分成两类：是否考虑掉落的随机性带来的消除，如果考虑，需要细分两部分reward怎么合成
# 先不考虑随机掉落, 此时只需要模拟1次
class TwoStepGreedyAI(BaseAI):
    
    # 计算交换之后进行连续消除之后的最大平均消除长度。通过模拟一定次数得到
    def cal_reward(self, game_board):
        # 模拟1次
        simulate_num = 1
        
        reward_list = []
        # Todo：还需要存储block_type用于best_move比较
        reward_block_type_list = []
        # 默认一定能够消除
        for _ in range(simulate_num):
            # 创建游戏棋盘的副本
            board_copy = copy.deepcopy(game_board)
            # 找到匹配
            matches = board_copy.find_matches()
            # 默认此时matches不为空
            assert matches is not None

            grouped_matches = board_copy.group_matches(matches)
            max_match_length = max([len(group) for group in grouped_matches], default=0)
            max_group = max(grouped_matches, key=len)
            block_type = board_copy.board[max_group[0][0]][max_group[0][1]].block_type

            match_len_list = [max_match_length]
            reward_block_type_list = [block_type]

            # 处理连续消除
            while True:
                new_matches = board_copy.find_matches()

                if not new_matches:
                    break

                new_grouped_matches = board_copy.group_matches(new_matches)
                max_match_length = max([len(group) for group in new_grouped_matches], default=0)
                max_match_length.append(max_match_length)

                max_group = max(new_grouped_matches, key=len)
                reward_block_type_list.append(board_copy.board[max_group[0][0]][max_group[0][1]].block_type)                

                # 处理不掉落新方块下，连续的子消除
                while True:
                    board_copy.remove_matches(new_grouped_matches)
                    new_matches = board_copy.find_matches()
                    if not new_matches:
                        break
                    new_grouped_matches = board_copy.group_matches(new_matches)
                    max_match_length = max([len(group) for group in new_grouped_matches], default=0)
                    match_len_list.append(max_match_length)

                    max_group = max(new_grouped_matches, key=len)
                    reward_block_type_list.append(board_copy.board[max_group[0][0]][max_group[0][1]].block_type)
                    
                # 先不考虑随机掉落新方块的reward
                #board_copy.fill_empty_spaces()

            reward_list.append(max(match_len_list))

        return reward_list[0]   

    # 遍历所有可能，计算reward
    def get_move(self, game_board):
        best_move = None
        best_match_length = 0
        best_block_type = 0

        # 保存所有可能交换的reward
        for row in range(game_board.rows):
            for col in range(game_board.cols):
                # 尝试交换右边的方块
                if col < game_board.cols - 1:
                    game_board.board[row][col], game_board.board[row][col + 1] = game_board.board[row][col + 1], game_board.board[row][col]
                    # 计算reward
                    # best_match_length = self.cal_reward(game_board)
                    game_board.board[row][col], game_board.board[row + 1][col] = game_board.board[row + 1][col], game_board.board[row][col]

                # 尝试交换下边的方块
                if row < game_board.rows - 1:
                    game_board.board[row][col], game_board.board[row + 1][col] = game_board.board[row + 1][col], game_board.board[row][col]
                    # 计算reward

                    game_board.board[row][col], game_board.board[row + 1][col] = game_board.board[row + 1][col], game_board.board[row][col]

        # 选择best_move，如果存在多个，则random选取


        if best_move:
            return best_move
            #x1, y1, x2, y2 = best_move
            #game_board.swap_blocks(x1, y1, x2, y2)
        else:
            print("AI 未找到合适的移动，步数不消耗。")
