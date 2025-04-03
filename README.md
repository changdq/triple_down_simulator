项目说明：

我感觉百分之一这个手游的遗迹模式很好玩，看似简单的三消但想要玩高分需要non-trivial的技巧（本人手操在这个模式的排行榜上排58）。所以我打算写一个模拟器，同时训练一个RL模型来挑战一下这个模式的最高分。

分为这么几个阶段：写一个模拟器 -> 训练模型 -> 写一个监控屏幕的应用让模型帮我决策，在游戏内刷榜

工作进度：
core.py 包含了主要后台游戏逻辑和一个简单的贪心AI
ui.py 使用pygame设计一个游戏界面

说明：本项目由我本人和豆包大模型合作进行