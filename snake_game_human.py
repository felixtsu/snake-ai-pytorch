import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:

    def __init__(self, w=640, h=480):

        ## 这里制定整个界面的宽w和高h
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        ## 当前的头节点
        self.head = Point(self.w / 2, self.h / 2)

        ## 当前蛇的全部节点（数组）
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    #这个函数用来生成一个食物
    def _place_food(self):

        ## 这个地方应该要计算出来一个随机的x、y，让食物出现在这个地方
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        ## TODO 这里会有隐藏的bug
        ## 想想，生成食物会有什么bug？？？？


    def play_step(self):

        ## 这里有个主流程，可以先分析一下是怎么回事
        ## 如果有个core loop的概念就最好了

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        
        ## TODO 这里需要处理这一轮有没有吃到食物的情况
        # 1. 怎么判断有没有吃到食物呢？
        # 2. 吃到食物要做什么？
        # 3. 没吃到食物要做什么？
        # self.head可以拿到蛇头的点的坐标
        # self.food可以拿到食物的点的坐标
        # self.score就是当前游戏得分
        # self.snake就是蛇全部身体的点的列表/数组

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):

        # 这个函数用来判定，我们的蛇有没有撞到障碍物
        # 障碍物分成两类
        # 1. 边界（上下左右四边的墙）
        # 我帮你们写好了
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        # 2. 自己
        # TODO 这个地方你们需要自己判定
        # self.head 可以拿到头的点
        # self.snake 可以拿到整条蛇的点的数组 （从头到尾）
        # 想想怎么用这些来判定自己有没有撞到自己


        # 3. 如果我们想要好玩一点，比如在地图中央也有迷宫一样的墙，那么可以在这里添加
        # TODO
        # 添加的方法可以结合 边界和自己的方式来实现

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            ## 画蛇的话，就是外层深色，内层浅色
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))


        ## 这里是加入了食物的点 （红色）
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
