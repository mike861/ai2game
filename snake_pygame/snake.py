import pygame
import time
import random

# 初始化Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# 设置显示屏幕尺寸
DIS_WIDTH = 600
DIS_HEIGHT = 400

# 设置蛇块的大小和初始速度
SNAKE_BLOCK = 10
SNAKE_SPEED = 5

# 初始化显示屏幕
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by python coder')

# 初始化时钟
clock = pygame.time.Clock()

# 设置字体样式
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

#def draw_snake(snake_block, snake_list):
#    for x in snake_list:
#        pygame.draw.rect(dis, BLACK, [x[0], x[1], snake_block, snake_block])
def draw_snake(snake_block, snake_list):
    for idx, x in enumerate(snake_list):
        if idx == 0:
            color = RED  # 蛇头颜色
        elif idx == len(snake_list) - 1:
            color = GREEN  # 蛇尾颜色
        else:
            color = BLACK  # 蛇身体颜色
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def display_message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3 + y_displace])

def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])

def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        if [foodx, foody] not in snake_list:
            return foodx, foody

def game_loop():
    game_over = False
    game_close = False
    game_pause = False

    x1, y1 = DIS_WIDTH / 2, DIS_HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1
    snake_speed = SNAKE_SPEED  # 初始速度
    snake_block = SNAKE_BLOCK  # 初始蛇宽度
    food_count = 0  # 吃到的食物数量

    foodx, foody = generate_food(snake_list)

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            display_message("You Lost! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("Pause pressed")
                    game_pause = not game_pause
                if event.key == pygame.K_LEFT and x1_change == 0:
                    print("Pause left")
                    x1_change, y1_change = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change, y1_change = 0, -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change, y1_change = 0, SNAKE_BLOCK

        if game_pause:
            display_message("Paused", RED)  # 显示暂停信息
            pygame.display.update()
            continue

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLUE)

        pygame.draw.rect(dis, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_list)
            length_of_snake += 1
            food_count += 1

            if food_count % 10 == 0:  # 每吃到10次食物
                snake_block += 1  # 蛇变宽
            if food_count % 3 == 0:  # 每吃到3次食物
                snake_speed += 1  # 速度增加

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
