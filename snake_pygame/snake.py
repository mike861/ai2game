import pygame
import pygame.gfxdraw
import time
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
CLOUR_BAR = (128, 128, 128)

# Set display screen size
DIS_WIDTH = 600
DIS_HEIGHT = 400
# 设置信息栏高度
INFO_BAR_HEIGHT = 40

# Set initial size and speed of the snake
SNAKE_BLOCK = 10
SNAKE_SPEED = 5

# Initialize display screen
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game')

# Initialize clock
clock = pygame.time.Clock()

# Set font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

# 加载声音
eat_sound = pygame.mixer.Sound("snake_pygame/eatfood.wav")
gameover_sound = pygame.mixer.Sound("snake_pygame/gameover2.wav")

def display_message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3 + y_displace])

def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])

class SnakeGame:
    def __init__(self):
        # Initial game state
        self.game_over = False
        self.game_close = False
        self.game_pause = False

        # 调整游戏区域
        self.game_area_rect = pygame.Rect(0, INFO_BAR_HEIGHT, DIS_WIDTH, DIS_HEIGHT - INFO_BAR_HEIGHT)

        # Snake's initial position
        self.x1, self.y1 = DIS_WIDTH / 2, DIS_HEIGHT / 2
        self.x1_change, self.y1_change = 0, 0

        # Snake properties
        self.snake_list = []
        self.length_of_snake = 1
        self.snake_speed = SNAKE_SPEED
        self.snake_block = SNAKE_BLOCK
        self.direction = 'left'  # init head to left

        # Food properties
        self.food_count = 0
        self.foodx, self.foody = self.generate_food()

        self.frame_count = 0
        self.frame_eat_food = 0
        
        # 时间相关变量
        self.start_ticks = pygame.time.get_ticks()  # 获取游戏开始的时间
        self.elapsed_time = 0  # 累积的游戏时间

    def generate_food(self):
        # Generate food in a random position
        while True:
            foodx = round(random.randrange(self.game_area_rect.left, self.game_area_rect.right - self.snake_block) / 10.0) * 10.0
            foody = round(random.randrange(self.game_area_rect.top, self.game_area_rect.bottom - self.snake_block) / 10.0) * 10.0
            #foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            #foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            if [foodx, foody] not in self.snake_list:
                return foodx, foody

    def handle_events(self):
        # Handle all the game events (keyboard inputs, game exit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_pause = not self.game_pause
                # Snake movement controls
                if event.key == pygame.K_LEFT and self.x1_change == 0:
                    self.x1_change, self.y1_change = -self.snake_block, 0
                    self.direction = 'left'
                elif event.key == pygame.K_RIGHT and self.x1_change == 0:
                    self.x1_change, self.y1_change = self.snake_block, 0
                    self.direction = 'right'
                elif event.key == pygame.K_UP and self.y1_change == 0:
                    self.x1_change, self.y1_change = 0, -self.snake_block
                    self.direction = 'up'
                elif event.key == pygame.K_DOWN and self.y1_change == 0:
                    self.x1_change, self.y1_change = 0, self.snake_block
                    self.direction = 'down'

    def check_food_collision2(self):
        """Check if the snake has collided with the food."""
        # Check if any part of the snake's head is overlapping with the food
        for dx in range(self.snake_block):
            for dy in range(self.snake_block):
                if self.foodx <= self.x1 + dx <= self.foodx + self.snake_block and \
                   self.foody <= self.y1 + dy <= self.foody + self.snake_block:
                    return True
        return False
    
    def check_food_collision3(self):
        """Check if the snake has collided with the food."""
        # Calculate the center point of the snake's head
        head_center_x = self.x1 + self.snake_block // 2
        head_center_y = self.y1 + self.snake_block // 2

        # Check if the center of the snake's head is within the food block
        if self.foodx <= head_center_x < self.foodx + self.snake_block and \
           self.foody <= head_center_y < self.foody + self.snake_block:
            return True 
        return False
    
    def check_food_collision(self):
        """Check if the snake has collided with the food with at least 1/4 overlap."""
        # 计算蛇头和食物的中心点
        snake_head_center_x = self.x1 + self.snake_block // 2
        snake_head_center_y = self.y1 + self.snake_block // 2
        food_center_x = self.foodx + self.snake_block // 2
        food_center_y = self.foody + self.snake_block // 2

        # 计算中心点之间的距离
        distance_x = abs(snake_head_center_x - food_center_x)
        distance_y = abs(snake_head_center_y - food_center_y)

        # 设定阈值为蛇头或食物大小的一半（为了允许四分之一重叠）
        threshold_x = self.snake_block // 2
        threshold_y = self.snake_block // 2

        # 如果蛇头中心与食物中心的距离小于等于阈值，则认为发生了碰撞
        if distance_x <= threshold_x and distance_y <= threshold_y:
            return True
        return False
    
    def calculate_head_properties(self):
        start_angle, stop_angle = None, None

        if  'left' == self.direction:  # move left
            start_angle = -140
            stop_angle = 140
        elif 'right' == self.direction:  # move right
            start_angle = 40
            stop_angle = -40
        elif 'up' == self.direction:  # move up
            start_angle = -50
            stop_angle = -130
        elif 'down' == self.direction:  # move down
            start_angle = 130
            stop_angle = 50

        return start_angle, stop_angle
    
    def calculate_tail_swing_properties(self):
        center_x, center_y, start_angle, stop_angle = None, None, None, None

        if len(self.snake_list) > 1:
            tail_position = self.snake_list[0]
            prev_position = self.snake_list[1]
            if tail_position[0] > prev_position[0]:  # move left
                center_x = tail_position[0]
                center_y = tail_position[1] + (self.snake_block / 2)
                start_angle = -30
                stop_angle = 30
            elif tail_position[0] < prev_position[0]:  # move right
                center_x = tail_position[0] + self.snake_block
                center_y = tail_position[1] + (self.snake_block / 2)
                start_angle = 150
                stop_angle = -150
            elif tail_position[1] > prev_position[1]:  # move up
                center_x = tail_position[0] + (self.snake_block / 2)
                center_y = tail_position[1]
                start_angle = -120
                stop_angle = -60
            elif tail_position[1] < prev_position[1]:  # move down
                center_x = tail_position[0] + (self.snake_block / 2)
                center_y = tail_position[1] + self.snake_block
                start_angle = 60
                stop_angle = 120

            angle_tail = [-2,-1,0,1,2]
            angle_index = (int(self.frame_count/2) % 5) 
            start_angle += (angle_tail[angle_index] * 10)
            stop_angle += (angle_tail[angle_index] * 10)
        return center_x, center_y, start_angle, stop_angle
        
    def draw_snake(self):
        head_position = self.snake_list[-1]
        radius = self.snake_block//2
        drawing_head_position = (head_position[0]+radius, head_position[1]+radius)
        if self.frame_eat_food + 3 > self.frame_count and self.food_count > 0:
            # When food is eaten, draw a ring to represent the snake opening its mouth
            pygame.draw.circle(dis, RED, drawing_head_position, self.snake_block // 2 + 1, 2)
        else:
            # Normally, draw a solid circle to represent the snake head
            start_angle,stop_angle = self.calculate_head_properties()
            #rect = pygame.Rect(head_position, (self.snake_block, self.snake_block))
            #pygame.draw.arc(dis, RED, rect, math.radians(start_angle), math.radians(stop_angle), self.snake_block)
            pygame.gfxdraw.pie(dis, int(drawing_head_position[0]), int(drawing_head_position[1]), radius, start_angle, stop_angle, RED)

        if len(self.snake_list) > 1 :
            arc_center_x, arc_center_y,start_angle,stop_angle = self.calculate_tail_swing_properties()
            # Define the bounding rectangle of the arc
            rect = pygame.Rect(0, 0, self.snake_block * 2, self.snake_block * 2)
            rect.center = (arc_center_x, arc_center_y)
            # Draw the arc to simulate the wagging of the snake tail
            pygame.draw.arc(dis, GREEN, rect, math.radians(start_angle), math.radians(stop_angle), self.snake_block)

        for idx, x in enumerate(self.snake_list):
            if idx == 0:
                continue
            elif idx == len(self.snake_list) - 1:
                continue
            else:
                color = BLACK  # Color for the rest of the body
                pygame.draw.rect(dis, color, [x[0], x[1], self.snake_block, self.snake_block])

    def update_game_state(self):
        # Update the game state (snake position, food consumption)
        if self.game_pause:
            display_message("Paused", RED)
            pygame.display.update()
            return

        self.x1 += self.x1_change
        self.y1 += self.y1_change
        self.snake_list.append([self.x1, self.y1])
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

        # Adjust the logic to check for food consumption
        if self.check_food_collision():
            self.foodx, self.foody = self.generate_food()
            self.length_of_snake += 1
            self.food_count += 1
            self.frame_eat_food = self.frame_count

            # Increase snake's block size and speed after eating food
            if self.food_count % 10 == 0:
                self.snake_block += 1
            if self.food_count % 3 == 0:
                self.snake_speed += 1
                
            eat_sound.play()

        # Check for collision with boundaries
        if self.x1 < self.game_area_rect.left or self.x1 >= self.game_area_rect.right or \
          self.y1 < self.game_area_rect.top or self.y1 >= self.game_area_rect.bottom:
            self.game_close = True
            try:
                length = gameover_sound.get_length()  # 获取音频长度
                print("Sound length:", length, "seconds")
            except Exception as e:
                print("Error checking sound:", e)
            gameover_sound.play()
            return

        for x in self.snake_list[:-1]:
            if x == [self.x1, self.y1]:
                self.game_close = True

    def render_game(self):
        # Render the game state to the screen
        dis.fill(BLUE)# 绘制信息栏背景
        pygame.draw.rect(dis, CLOUR_BAR, [0, 0, DIS_WIDTH, INFO_BAR_HEIGHT])
        pygame.draw.rect(dis, GREEN, [self.foodx, self.foody, self.snake_block, self.snake_block])
        #pygame.draw.rect(dis, GREEN, [self.foodx, self.foody, SNAKE_BLOCK, SNAKE_BLOCK])
        #draw_snake(self.snake_block, self.snake_list)
        self.draw_snake()
        display_score(self.length_of_snake - 1)
        pygame.display.update()

    def update_game_time(self):
        """更新游戏时间"""
        if not self.game_pause:
            current_ticks = pygame.time.get_ticks()
            self.elapsed_time = (current_ticks - self.start_ticks) / 1000  # 转换成秒
            
    def display_time(self):
        """在屏幕上显示时间"""
        minutes = int(self.elapsed_time / 60)
        seconds = int(self.elapsed_time % 60)
        time_str = "{:02d}:{:02d}".format(minutes, seconds)
        time_surface = score_font.render(time_str, True, YELLOW)
        # 假设时间显示在屏幕顶部中间
        dis.blit(time_surface, (DIS_WIDTH / 2, 5))

    def run(self):
        while not self.game_over:
            while self.game_close:
                # Handle game close logic
                dis.fill(BLUE)
                display_message("You Lost! Press Q-Quit or C-Play Again", RED)
                #self.render_game()
                pygame.display.flip()  # 更新屏幕显示
                #pygame.display.update()

                #print("game_close")
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            self.__init__()
                            return self.run()

            self.handle_events()
            self.update_game_state()
            self.update_game_time()  # 更新游戏时间
            self.render_game()  # 渲染游戏
            self.display_time()  # 显示时间
            pygame.display.flip()  # 更新屏幕显示

            #print("tick")
            self.frame_count += 1
            clock.tick(self.snake_speed)

        print("game_over")
        pygame.mixer.quit()
        pygame.quit()
        quit()

game = SnakeGame()
game.run()
