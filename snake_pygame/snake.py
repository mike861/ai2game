import pygame
import time
import random
import math

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set display screen size
DIS_WIDTH = 600
DIS_HEIGHT = 400

# Set initial size and speed of the snake
SNAKE_BLOCK = 10
SNAKE_SPEED = 5

# Initialize display screen
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by python coder')

# Initialize clock
clock = pygame.time.Clock()

# Set font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


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

        # Snake's initial position
        self.x1, self.y1 = DIS_WIDTH / 2, DIS_HEIGHT / 2
        self.x1_change, self.y1_change = 0, 0

        # Snake properties
        self.snake_list = []
        self.length_of_snake = 1
        self.snake_speed = SNAKE_SPEED
        self.snake_block = SNAKE_BLOCK

        # Food properties
        self.food_count = 0
        self.foodx, self.foody = self.generate_food()

    def generate_food(self):
        # Generate food in a random position
        while True:
            #foodx = round(random.randrange(0, DIS_WIDTH - self.snake_block) / 10.0) * 10.0
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
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
                elif event.key == pygame.K_RIGHT and self.x1_change == 0:
                    self.x1_change, self.y1_change = self.snake_block, 0
                elif event.key == pygame.K_UP and self.y1_change == 0:
                    self.x1_change, self.y1_change = 0, -self.snake_block
                elif event.key == pygame.K_DOWN and self.y1_change == 0:
                    self.x1_change, self.y1_change = 0, self.snake_block

    def check_food_collision2(self):
        """Check if the snake has collided with the food."""
        # Check if any part of the snake's head is overlapping with the food
        for dx in range(self.snake_block):
            for dy in range(self.snake_block):
                if self.foodx <= self.x1 + dx <= self.foodx + self.snake_block and \
                   self.foody <= self.y1 + dy <= self.foody + self.snake_block:
                    return True
        return False
    
    def check_food_collision(self):
        """Check if the snake has collided with the food."""
        # Calculate the center point of the snake's head
        head_center_x = self.x1 + self.snake_block // 2
        head_center_y = self.y1 + self.snake_block // 2

        # Check if the center of the snake's head is within the food block
        if self.foodx <= head_center_x < self.foodx + self.snake_block and \
           self.foody <= head_center_y < self.foody + self.snake_block:
            return True
        return False
    
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
        return center_x, center_y, start_angle, stop_angle
        
    def draw_snake(self):
        head_position = self.snake_list[-1]
        if self.check_food_collision():
            # When food is eaten, draw a ring to represent the snake opening its mouth
            print("check_food_collision")
            pygame.draw.circle(dis, RED, head_position, self.snake_block // 2 + 3, 3)
        else:
            # Normally, draw a solid circle to represent the snake head
            pygame.draw.ellipse(dis, RED, [head_position[0], head_position[1], self.snake_block, self.snake_block])

        if len(self.snake_list) > 1 :
            tail_position = self.snake_list[0]
            prev_position = self.snake_list[1]
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

            # Increase snake's block size and speed after eating food
            if self.food_count % 10 == 0:
                self.snake_block += 1
            if self.food_count % 3 == 0:
                self.snake_speed += 1

        # Check for collision with boundaries
        if self.x1 < 0 or self.x1 >= DIS_WIDTH or self.y1 < 0 or self.y1 >= DIS_HEIGHT:
            self.game_close = True
            return

        for x in self.snake_list[:-1]:
            if x == [self.x1, self.y1]:
                self.game_close = True

    def render_game(self):
        # Render the game state to the screen
        dis.fill(BLUE)
        #pygame.draw.rect(dis, GREEN, [self.foodx, self.foody, self.snake_block, self.snake_block])
        pygame.draw.rect(dis, GREEN, [self.foodx, self.foody, SNAKE_BLOCK, SNAKE_BLOCK])
        #draw_snake(self.snake_block, self.snake_list)
        self.draw_snake()
        display_score(self.length_of_snake - 1)
        pygame.display.update()

    def run(self):
        while not self.game_over:
            while self.game_close:
                # Handle game close logic
                dis.fill(BLUE)
                display_message("You Lost! Press Q-Quit or C-Play Again", RED)
                pygame.display.update()

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
            self.render_game()
            #print("tick")
            clock.tick(self.snake_speed)

        print("game_over")
        pygame.quit()
        quit()

game = SnakeGame()
game.run()
