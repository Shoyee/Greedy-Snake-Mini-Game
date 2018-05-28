#coding:utf-8
import pygame
from enum import Enum, unique
import random

#设置颜色:
@unique
class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
#方向:
@unique
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

#墙
class Wall():
    def __init__(self, x, y, width, height, color = Color.BLACK.value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    #画墙
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 5)

#食物:
class Food():
    def __init__(self, x, y, size, color = Color.RED.value):
        '''

        :param x: 起始点x
        :param y: 起始点y
        :param size: 直径
        :param color: 颜色
        '''
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        #隐藏状态
        self.hidden = False

    def draw(self, screen):
        #没有处于隐藏状态 画出来
        if not self.hidden:
            pygame.draw.circle(screen, self.color, (self.x + self.size // 2, self.y + self.size // 2),(self.size // 2), 0)


#蛇的节点
class SnakeNode():
    def __init__(self, x, y, size, color=Color.GREEN.value):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, screen):
        #实心体
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.size, self.size), 0)
        #边框
        pygame.draw.rect(screen, Color.BLACK.value, (self.x, self.y, self.size, self.size), 1)

#蛇
class Snake():
    def __init__(self, x, y, size = 20, length = 5):
        '''
        :param x:
        :param y:
        :param size:  大小
        :param length:  初始化长度
        '''
        self.dir = Direction.LEFT
        self.nodes = []
        self.alive = True #存活状态
        #新的方向
        self.newdir = None
        #向蛇的身体中放入蛇的节点
        for index in range(length):
            #每个节点的位置是依次向后的
            node = SnakeNode(x + index * size, y, size)
            self.nodes.append(node)
    @property
    def head(self):
        return self.nodes[0]

    #操作方向的时候 蛇要改变方向
    def changedir(self, new_dir):
        #改变
        if new_dir != self.dir and (self.dir.value + new_dir.value) % 2 != 0:
            self.newdir = new_dir

    #移动:
    def move(self):
        #移动的时候:
        if self.newdir:
            #有新的方向 按照新的方向走
            self.dir = self.newdir
            self.newdir = None #恢复到默认值 准备再次接受新的方向
        #记录一下头的坐标
        x, y, size = self.head.x, self.head.y, self.head.size

        #根据方向更改坐标位置
        if self.dir == Direction.UP:
            y -= size
        elif self.dir == Direction.DOWN:
            y += size
        elif self.dir == Direction.LEFT:
            x -= size
        else:
            x += size

        #移动完成之后 head有了新的坐标
        newhead = SnakeNode(x, y, size)
        #放到节点列表中放入
        self.nodes.insert(0, newhead)
        #移除最后一个
        self.nodes.pop()

    def collide_wall(self, wall):
        "头撞墙"
        head = self.head
        if head.x < wall.x or (head.x + head.size> wall.x + wall.width) or head.y < wall.y or (head.y + head.size > wall.y + wall.height):
            self.alive = False

    #撞自己
    def eat_self(self):
        for index in range(4, len(self.nodes)):
            node = self.nodes[index]
            #判断两个段撞上了
            if node.x == self.head.x and node.y == self.head.y:
                self.alive = False
    #吃食物
    def eat_food(self, food):
        #吃到了还是没吃到
        if self.head.x == food.x and self.head.y == food.y:
            #蛇增加节点
            tail = self.nodes[-1]
            self.nodes.append(tail)
            return True
        return False

    #画蛇
    def draw(self, screen):
        #画节点
        for node in self.nodes:
            node.draw(screen)

def main():
    #处理键盘按键操作
    def handle_key(event):
        #获取键盘按键的内容
        key = event.key
        if key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
            #在蛇活着的基础上
            if snake.alive:
                if key == pygame.K_w:
                    newdir = Direction.UP
                elif key ==  pygame.K_d:
                    newdir = Direction.RIGHT
                elif key == pygame.K_s:
                    newdir = Direction.DOWN
                else:
                    newdir = Direction.LEFT
                #让蛇改变方向
                snake.changedir(newdir)

    #创建食物
    def create_food():
        #获得蛇的大小
        snake_size = snake.head.size
        #计算网格
        max_row = wall.height // snake_size
        max_col = wall.width // snake_size
        #创建食物的时候随机网格
        row = random.randrange(0, max_row)
        col = random.randrange(0, max_col)
        return Food(col * snake_size + wall.x, wall.y + row * snake_size, snake_size)

    #创建墙:
    wall = Wall(10, 10, 500, 500)
    #c创建蛇
    snake = Snake(250, 250)
    #创建食物
    food = create_food()
    #游戏界面初始化
    pygame.init()
    screen = pygame.display.set_mode((520, 520))
    #窗口名字
    pygame.display.set_caption("贪吃蛇")
    #创建控制游戏每秒帧数的时钟
    clock = pygame.time.Clock()

    #事件过程中
    running = True
    while running:
        for et in pygame.event.get():
            if et.type == pygame.QUIT:
                running = False
            elif et.type == pygame.KEYDOWN:
                #处理按键操作
                handle_key(et)
        #刷新游戏界面
        #蛇活着的基础上
        if snake.alive:
            screen.fill((255, 255, 255))
            wall.draw(screen)
            food.draw(screen)
            snake.draw(screen)
            #渲染
            pygame.display.flip()
        #按帧数刷新
        clock.tick(5)
        #界面渲染完成之后 蛇动起来
        if snake.alive:
            snake.move()
            #检测是否撞墙
            snake.collide_wall(wall)
            #吃食物
            if snake.eat_food(food):
                food.hidden = True
                food = create_food()
            #吃到自己
            snake.eat_self()

if __name__ == '__main__':
    main()