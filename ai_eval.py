

import random
from core import GameBoard, Block
import numpy as np
import ai_player 


class Game:
    def __init__(self, rows=8, cols=8, type_probs=None, max_block_level=5, initial_steps=30):
        if type_probs is None:
            type_probs = [0.2, 0.2, 0.2, 0.2, 0]
        self.rows = rows
        self.cols = cols
        self.type_probs = type_probs
        self.max_block_level = max_block_level
        self.initial_steps = initial_steps
        self.game_board = None
        self.ai_player = None
        self.reset()
    

    def reset(self):
        self.game_board = GameBoard(self.rows, self.cols, self.type_probs, self.max_block_level, self.initial_steps)
        return self.game_board
    
    def set_ai(self, ai_player):
        self.ai_player = ai_player


    # 我需要自己根据core中gameboard的接口，暂时应该不需要再定义一个play_one_step
    # 返回一局游戏结束后的总步数
    def play_full_game(self, verbose=False):
        while not self.game_board.is_game_over():
            best_move = self.ai_player.get_move(self.game_board)
            x1, y1, x2, y2 = best_move
            self.game_board.swap_blocks(x1, y1, x2, y2)
        
        return self.game_board.total_steps



# 返回每局游戏结束后的总步数的list
def evaluate_ai(ai_player, num_games=100, verbose=False):

    game = Game()

    game.set_ai(ai_player)
    
    results = []
    for i in range(num_games):
        if verbose:
            print(f"Game {i+1}/{num_games}")
        
        game.reset()
        result = game.play_full_game(verbose=verbose)
        results.append(result)

    
    return results

if __name__ == "__main__":
    # Example usage

    num_games = 100
    ai_player = ai_player.OneStepGreedyAI()

    results = evaluate_ai(ai_player, num_games, verbose=True)

    # 打印结果, 包括num_games, results的平均值，最大值，最小值，方差
    results_array = np.array(results)
    print("\n游戏结果统计:")
    print(f"游戏局数: {num_games}")
    print(f"平均步数: {np.mean(results_array):.2f}")
    print(f"最大步数: {np.max(results_array)}")
    print(f"最小步数: {np.min(results_array)}")
    print(f"步数标准差: {np.std(results_array):.2f}")

    #print(f"Evaluation result: {result['avg_score']}")
