import pygame
import time
import random

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
SNAKE_SPEED = 10

# Initialize display screen
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by python coder')

# Initialize clock
clock = pygame.time.Clock()

# Set font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_snake(snake_block, snake_list):
    """Draw the snake on the display.

    Args:
        snake_block (int): The size of each block of the snake.
        snake_list (list): A list of coordinates representing the snake's body.

    The function iterates through the snake_list and draws each block of the snake.
    It colors the head and tail of the snake differently for visual distinction.
    """
    for idx, x in enumerate(snake_list):
        if idx == 0:
            color = RED  # Color for the head of the snake
        elif idx == len(snake_list) - 1:
            color = GREEN  # Color for the tail of the snake
        else:
            color = BLACK  # Color for the rest of the body
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

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
        draw_snake(self.snake_block, self.snake_list)
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
