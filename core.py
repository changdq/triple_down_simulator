import random

# 方块类
class Block:
    def __init__(self, block_type):
        self.block_type = block_type

    def __repr__(self):
        return str(self.block_type)
    
    def __format__(self, format_spec):
        return format(self.block_type, format_spec)    

# 游戏板类
class GameBoard:
    def __init__(self, rows, cols, type_probs, max_block_level, initial_steps):
        self.rows = rows
        self.cols = cols
        self.type_probs = type_probs
        self.max_block_level = max_block_level
        self.board = self.initialize_board()
        # 如果初始就无法消除，重新打散棋盘
        if self.is_board_stuck():
            self.reshuffle_board()       
            
        self.remaining_steps = initial_steps
        # 总步数，用于展示结果
        self.total_steps = 0

    def initialize_board(self):
        board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                while True:
                    block_type = random.choices(range(1, len(self.type_probs) + 1), weights=self.type_probs)[0]
                    board[row][col] = Block(block_type)
                    if not self.has_matches_at_position(board, row, col):
                        break
   
        return board
    
    # 判断是否游戏结束
    def is_game_over(self):
        if self.remaining_steps <= 0:
            # 游戏结束，打印最终的消除步数
            print("步数已用完，游戏结束！总步数为" + str(self.total_steps))
            return True
        else:
            return False

    def has_matches_at_position(self, board, row, col):
        # 检查水平匹配
        if col >= 2 and board[row][col].block_type == board[row][col - 1].block_type == board[row][col - 2].block_type and board[row][col].block_type < self.max_block_level:
            return True
        # 检查垂直匹配
        if row >= 2 and board[row][col].block_type == board[row - 1][col].block_type == board[row - 2][col].block_type and board[row][col].block_type < self.max_block_level:
            return True
        return False


    def display_board(self):
        # 显示列坐标
        print("  ", end="")
        for col in range(self.cols):
            print(f"{col:2d}", end="")
        print()
        for row in range(self.rows):
            print(f"{row:2d}", end="")
            for col in range(self.cols):
                block = self.board[row][col]
                if block is None:
                    print("  ", end="")
                else:
                    print(f"{block:2d}", end="")
            print()
        print('-----')        

    # For ui, 交换只是交换，以插入动画过程
    def swap_blocks_ui(self, x1, y1, x2, y2):
        if (abs(x1 - x2) + abs(y1 - y2)) == 1:
            self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]

    def swap_blocks(self, x1, y1, x2, y2):
        # if self.remaining_steps <= 0:
        #     print("步数已用完，游戏结束！")
        #     return

        # 检查是否相邻
        if (abs(x1 - x2) + abs(y1 - y2)) == 1:
            self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
            matches = self.find_matches()
            if matches:
                # 此时一定发生合法交换，总步数+1
                self.total_steps += 1 

                grouped_matches = self.group_matches(matches)
                self.update_steps(grouped_matches)
                self.remove_matches(grouped_matches, (x2, y2))
                self.fill_empty_spaces()
                # Debug:
                # self.display_board()
                # 处理连续消除：
                while True:
                    new_matches = self.find_matches()
                    if not new_matches:
                        break
                    new_grouped_matches = self.group_matches(new_matches)
                    self.remove_matches(new_grouped_matches)
                    self.fill_empty_spaces()
                # 如果棋盘都无法消除，则进行打散，直到能够消除
                if self.is_board_stuck():
                    self.reshuffle_board()

            else:
                # 如果没有匹配，交换回来
                self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
                print("此次交换没有产生匹配，步数不消耗。")
        else:
            print("只能交换相邻的方块！")

    
    def update_steps(self, grouped_matches):
        # 只判断最长的matches 和数量来判断更新
        max_matches = 0
        for group in grouped_matches:
            if len(group) > 4:
                self.remaining_steps += 1
            max_matches = max(max_matches,len(group))
                
        if max_matches <= 3:
            self.remaining_steps -= 1

        print(f"剩余步数: {self.remaining_steps}, 已移动总步数: {self.total_steps}")
        

    # 最高等级的方块不会匹配
    # 需要兼容value是None的情况
    def find_matches(self):
        matches = []
        # 检查水平匹配
        for row in range(self.rows):
            for col in range(self.cols - 2):
                if self.board[row][col] and self.board[row][col + 1] and self.board[row][col + 2]:
                    if (self.board[row][col].block_type == self.board[row][col + 1].block_type == self.board[row][col + 2].block_type) and (self.board[row][col].block_type < self.max_block_level):
                        for i in range(3):
                            if (row, col + i) not in matches:
                                matches.append((row, col + i))
        # 检查垂直匹配
        for col in range(self.cols):
            for row in range(self.rows - 2):
                if self.board[row][col] and self.board[row + 1][col] and self.board[row+2 ][col]:
                    if (self.board[row][col].block_type == self.board[row + 1][col].block_type == self.board[row + 2][col].block_type) and (self.board[row][col].block_type < self.max_block_level):
                        for i in range(3):
                            if (row + i, col) not in matches:
                                matches.append((row + i, col))
        return matches

    # 加入一个check_matches的函数：
    # 先用find_matches代替，效率差不多


    def group_matches(self, matches):
        grouped = []
        visited = set()
        for match in matches:
            if match not in visited:
                block_type = self.board[match[0]][match[1]].block_type
                group = []
                self._dfs(match, block_type, matches, visited, group)
                grouped.append(group)
        return grouped

    def _dfs(self, pos, block_type, matches, visited, group):
        if pos in visited or pos not in matches or self.board[pos[0]][pos[1]].block_type != block_type:
            return
        visited.add(pos)
        group.append(pos)
        row, col = pos
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                self._dfs(neighbor, block_type, matches, visited, group)

    # 得到生成新方块的位置和type，和下面的remove_matches类似
    # 需要注意swap_pos是两个，原位置和新位置都需要保留
    def remove_matches_ui(self, matches, swap_pos=None):
        res = []
        groups = self.group_matches(matches)
        for group in groups:
            assert len(group) > 0
            original_type = self.board[group[0][0]][group[0][1]].block_type

            # 移除当前组内的匹配方块
            for row, col in group:
                self.board[row][col] = None

            # 确定生成新方块的位置
            if swap_pos and swap_pos[0] in group:
                x, y = swap_pos[0]
            elif swap_pos and swap_pos[1] in group:
                x,y = swap_pos[1]
            else:
                # 计算当前组的中心位置
                sum_x = sum([row for row, _ in group])
                sum_y = sum([col for _, col in group])
                x = sum_x // len(group)
                y = sum_y // len(group)

            # 生成高 1 等级的方块，虽然不会发生，但暂时取max保护下
            new_block_type = min(original_type + 1, self.max_block_level)

            self.board[x][y] = Block(new_block_type)

            res.append((x,y,new_block_type))
        
        return res


    # remove_matches 按照groups移除，并在每个group的中心位置生成一个高1等级的方块
    def remove_matches(self, groups, swap_pos=None):
        for group in groups:

            # 保存原方块等级用于生产新方块
            assert len(group) > 0
            original_type = self.board[group[0][0]][group[0][1]].block_type

            # 移除当前组内的匹配方块
            for row, col in group:
                self.board[row][col] = None

            # 确定生成新方块的位置
            if swap_pos and swap_pos in group:
                x, y = swap_pos
            else:
                # 计算当前组的中心位置
                sum_x = sum([row for row, _ in group])
                sum_y = sum([col for _, col in group])
                x = sum_x // len(group)
                y = sum_y // len(group)


            # 生成高 1 等级的方块，虽然不会发生，但暂时取max保护下
            new_block_type = min(original_type + 1, self.max_block_level)
            self.board[x][y] = Block(new_block_type)

    # For ui，需要增加一个获取fill_info的函数，获取fill动画所必须的信息：
    def fill_empty_spaces_ui(self):
        #self.display_board()

        fall_info = []
        new_blocks = []
        for col in range(self.cols):
            empty_spaces = []
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] is None: 
                    empty_spaces.append(row)
                else:
                    if empty_spaces:
                        new_row = empty_spaces.pop(0)
                        fall_info.append((row, col, new_row, col))
                        self.board[new_row][col] = self.board[row][col]
                        self.board[row][col] = None
                        empty_spaces.append(row)
            # 填充顶部的空缺
            
            for empty_row in empty_spaces:
                # 按照type_probs 填充
                block_type = random.choices(range(1, len(self.type_probs) + 1), weights=self.type_probs)[0]
                new_blocks.append((empty_row, col, block_type))
                self.board[empty_row][col] = Block(block_type)

        #self.display_board()

        return fall_info, new_blocks

    
    def fill_empty_spaces(self):

        for col in range(self.cols):
            empty_spaces = []
            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] is None: 
                    empty_spaces.append(row)
                else:
                    if empty_spaces:
                        new_row = empty_spaces.pop(0)
                        self.board[new_row][col] = self.board[row][col]
                        self.board[row][col] = None
                        empty_spaces.append(row)
            # 填充顶部的空缺
            for empty_row in empty_spaces:
                # 按照type_probs 填充
                block_type = random.choices(range(1, len(self.type_probs) + 1), weights=self.type_probs)[0]
                self.board[empty_row][col] = Block(block_type)

    # 如果全图都无法消除, 则对现在的棋盘进行随机打散，直到可以消除
    def is_board_stuck(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # 尝试交换右边的方块
                if col < self.cols - 1:
                    self.board[row][col], self.board[row][col + 1] = self.board[row][col + 1], self.board[row][col]
                    matches = self.find_matches()
                    self.board[row][col], self.board[row][col + 1] = self.board[row][col + 1], self.board[row][col]
                    if matches:
                        return False
                # 尝试交换下边的方块
                if row < self.rows - 1:
                    self.board[row][col], self.board[row + 1][col] = self.board[row + 1][col], self.board[row][col]
                    matches = self.find_matches()
                    self.board[row][col], self.board[row + 1][col] = self.board[row + 1][col], self.board[row][col]
                    if matches:
                        return False
        print('The game board is stuck, reshuffle!')
        return True

    # 额外返回all_blocks和all_pos列表用于新动画的生成
    def reshuffle_board_ui(self):
        all_blocks = [self.board[row][col] for row in range(self.rows) for col in range(self.cols)]
        random.shuffle(all_blocks)
        index = 0
        while True:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.board[row][col] = all_blocks[index]
                    index += 1
            if not self.find_matches():
                break
            random.shuffle(all_blocks)
            index = 0
        print("棋盘已重新打散。")        
        all_pos = []
        all_blocks = []
        for i in range(self.rows):
            for j in range(self.cols):
                all_pos.append((i,j))
                all_blocks.append((i,j,self.board[i][j].block_type))
        return all_pos, all_blocks

    # 暴力随机，可能重试次数很多，此时怎么办？
    def reshuffle_board(self):
        all_blocks = [self.board[row][col] for row in range(self.rows) for col in range(self.cols)]
        random.shuffle(all_blocks)
        index = 0
        while True:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.board[row][col] = all_blocks[index]
                    index += 1
            if not self.find_matches():
                break
            random.shuffle(all_blocks)
            index = 0
        print("棋盘已重新打散。")

    # 贪心AI
    # 暂时先只兼容ui版本，后续还需要改
    def ai_move(self):
        best_move = None
        best_match_length = 0
        best_block_type = 0

        for row in range(self.rows):
            for col in range(self.cols):
                # 尝试交换右边的方块
                if col < self.cols - 1:
                    self.board[row][col], self.board[row][col + 1] = self.board[row][col + 1], self.board[row][col]
                    matches = self.find_matches()
                    grouped_matches = self.group_matches(matches)
                    max_match_length = max([len(group) for group in grouped_matches], default=0)
                    max_block_type = max([self.board[r][c].block_type for r, c in matches], default=0) if matches else 0

                    if max_match_length > 4 and max_match_length > best_match_length:
                        best_move = (row, col, row, col + 1)
                        best_match_length = max_match_length
                        best_block_type = max_block_type
                    elif max_match_length == best_match_length and max_block_type > best_block_type:
                        best_move = (row, col, row, col + 1)
                        best_block_type = max_block_type
                    elif max_match_length <= 3 and max_match_length > 0 and max_block_type > best_block_type and best_match_length <= 3:
                        best_move = (row, col, row, col + 1)
                        best_block_type = max_block_type

                    self.board[row][col], self.board[row][col + 1] = self.board[row][col + 1], self.board[row][col]

                # 尝试交换下边的方块
                if row < self.rows - 1:
                    self.board[row][col], self.board[row + 1][col] = self.board[row + 1][col], self.board[row][col]
                    matches = self.find_matches()
                    grouped_matches = self.group_matches(matches)
                    max_match_length = max([len(group) for group in grouped_matches], default=0)
                    max_block_type = max([self.board[r][c].block_type for r, c in matches], default=0) if matches else 0

                    if max_match_length > 4 and max_match_length > best_match_length:
                        best_move = (row, col, row + 1, col)
                        best_match_length = max_match_length
                        best_block_type = max_block_type
                    elif max_match_length == best_match_length and max_block_type > best_block_type:
                        best_move = (row, col, row + 1, col)
                        best_block_type = max_block_type
                    elif max_match_length <= 3 and max_match_length > 0 and max_block_type > best_block_type and best_match_length <= 3:
                        best_move = (row, col, row + 1, col)
                        best_block_type = max_block_type

                    self.board[row][col], self.board[row + 1][col] = self.board[row + 1][col], self.board[row][col]

        if best_move:
            return best_move
            #x1, y1, x2, y2 = best_move
            #self.swap_blocks(x1, y1, x2, y2)
        else:
            print("AI 未找到合适的移动，步数不消耗。")



# 主函数
def main():
    rows = 8
    cols = 8
    # 示例概率分布，这里表示每种类型方块出现的概率
    # 最高等级宝石不会掉落和初始化
    type_probs = [0.2, 0.2, 0.2, 0.2, 0]
    initial_steps = 10
    max_block_level = 5
    game_board = GameBoard(rows, cols, type_probs, max_block_level, initial_steps)
    game_board.display_board()
    print(f"初始步数: {initial_steps}")

    # 选择玩家输入或 AI 移动
    move_type = input("请选择移动方式 (1: 玩家输入, 2: AI 移动): ")
    if move_type == '1':
        while not game_board.is_game_over():
            try:
                x1, y1, x2, y2 = map(int, input(
                    "请输入要交换的两个方块的坐标 (x1 y1 x2 y2): ").split(','))
                if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
                    game_board.swap_blocks(x1, y1, x2, y2)
                    game_board.display_board()
                else:
                    print("输入的坐标超出范围，请重新输入！")
            except ValueError:
                print("输入格式错误，请输入四个整数！")
    elif move_type == '2':
        while not game_board.is_game_over():
            game_board.ai_move()
            game_board.display_board()
    else:
        print("无效的选择，请输入 1 或 2。")


    # while True:
    #     try:
    #         if game_board.remaining_steps <= 0:
    #             print(f"游戏结束，最终步数: {game_board.remaining_steps}")
    #             break
    #         x1, y1, x2, y2 = map(int, input("请输入要交换的两个方块的坐标 (x1 y1 x2 y2): ").split(','))
    #         if 0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols:
    #             game_board.swap_blocks(x1, y1, x2, y2)
    #             game_board.display_board()
    #         else:
    #             print("输入的坐标超出范围，请重新输入！")
    #     except ValueError:
    #         print("输入格式错误，请输入四个整数！")


if __name__ == "__main__":
    main()