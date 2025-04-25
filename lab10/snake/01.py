import random
import pygame
from color_palette import *
import time
import numpy as np
from PIL import Image

from db import setup_db, get_or_create_user, get_last_score, save_score, get_all_scores_for_user

setup_db()

username = input("Enter your username: ")
user_id = get_or_create_user(username)
start_level, start_score = get_last_score(user_id)
scores = get_all_scores_for_user(user_id)

if scores:
    print("\nChoose saving:")
    for i, (score_id, level, score, created_at) in enumerate(scores):
        print(f"{i + 1}) level: {level}, score: {round(score, 2)}, date: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        choice = int(input("enter number (or 0 for new starting): "))
        if 1 <= choice <= len(scores):
            selected_score = scores[choice - 1]
            start_level = selected_score[1]
            start_score = selected_score[2]
        else:
            start_level, start_score = 0, 0
    except ValueError:
        print("Invalid input, starting new game")
        start_level, start_score = 0, 0
else:
    print("No data. starting new game")
    start_level, start_score = 0, 0

pygame.init()

SIZE = 1000
WIDTH = SIZE
HEIGHT = SIZE
CELL_COUNT = 20
CELL = SIZE // CELL_COUNT
FPS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_small = pygame.font.SysFont("Verdana", 20)
font = pygame.font.SysFont("Verdana", 60)
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

def draw_grid():
    for i in range(CELL_COUNT):
        for j in range(CELL_COUNT):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [(100, 100, 100), (50, 50, 50)]

    for i in range(CELL_COUNT):
        for j in range(CELL_COUNT):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y



class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x = (self.body[0].x + self.dx) % CELL_COUNT
        self.body[0].y = (self.body[0].y + self.dy) % CELL_COUNT

    def check_collision(self, walls):
        if self.check_self_intersect():
            return True
        if self.is_wall_collision(walls):
            return True
        return False

    def check_self_intersect(self):
        for a in self.body:
            for b in self.body:
                if a is not b and a == b:
                    return True
        return False

    def is_wall_collision(self, walls):
        head = self.body[0]
        for wall in walls:
            if head.x == wall.x and head.y == wall.y:
                return True
        return False
    def draw(self, screen):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def update_food(self, food, owner):
        head = self.body[0]
        if head == food.pos:
            owner.score += food.weight
            while head == food.pos:
                food.set_random_position()
            self.body.append(Point(head.x + self.dx, head.y + self.dy))



class Food:
    def __init__(self, owner:'Game'):
        self.timer = 1
        self.owner = owner
        self.set_random_position()

    def draw(self, screen):
        self.timer -= 0.01 / FPS
        pygame.draw.rect(screen, (0, int(255 * self.weight), 0),
                         (self.timer * self.pos.x * CELL + (1 - self.timer) * (self.pos.x * CELL + CELL / 2),
                          self.timer * self.pos.y * CELL + (1 - self.timer) * (self.pos.y * CELL + CELL / 2),
                          CELL * self.timer, CELL * self.timer))
        if self.timer <= 0:
            self.set_random_position()

    def set_random_position(self):
        self.pos = Point(random.randint(0, CELL_COUNT - 1), random.randint(0, CELL_COUNT - 1))
        while any(wall.x == self.pos.x and wall.y == self.pos.y for wall in self.owner.levels[self.owner.current_level].walls):
            self.pos = Point(random.randint(0, CELL_COUNT - 1), random.randint(0, CELL_COUNT - 1))
        self.weight = random.random()
        self.timer = 1


class Level:
    def __init__(self, level_data):
        self.level_data = level_data
        self.height, self.width = level_data.shape
        self.walls = self.create_wall_list()
        #print(level_data)

    def create_wall_list(self):
        walls = []
        for y in range(self.height):
            for x in range(self.width):
                if self.level_data[y, x] == 1:
                    walls.append(Point(x, y))
        return walls

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, colorBLUE, (wall.x * CELL, wall.y * CELL, CELL, CELL))

    def get_walls(self):
        return self.walls

def load_from_png(filepath):
    img = Image.open(filepath, formats=["PNG"])
    img = img.convert('RGB')
    q = np.array(img)
    q = q.sum(-1) > 0
    img.close()
    return q

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.levels = []
        for l in range(3):
            self.levels.append(Level(load_from_png(f'levels/level{l}.png')))
        self.current_level = start_level
        self.score = start_score
        self.running = True
        self.food = Food(self)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.snake.dx == 0:
                    self.snake.dx = 1
                    self.snake.dy = 0
                elif event.key == pygame.K_LEFT and self.snake.dx == 0:
                    self.snake.dx = -1
                    self.snake.dy = 0
                elif event.key == pygame.K_DOWN and self.snake.dy == 0:
                    self.snake.dx = 0
                    self.snake.dy = 1
                elif event.key == pygame.K_UP and self.snake.dy == 0:
                    self.snake.dx = 0
                    self.snake.dy = -1
                elif event.key == pygame.K_1:
                    self.current_level = 0
                    self.reset_game()
                elif event.key == pygame.K_2:
                    self.current_level = 1
                    self.reset_game()
                elif event.key == pygame.K_3:
                    self.current_level = 2
                    self.reset_game()
                elif event.key == pygame.K_p:
                    save_score(user_id, self.current_level, self.score)
                    print("Game paused. Score saved.")
                    time.sleep(1)

    def update(self):
        self.snake.move()
        self.snake.update_food(self.food, self)
        if self.snake.check_collision(self.levels[self.current_level].get_walls()):
            time.sleep(1)
            self.running = False
            self.game_over()

    def draw(self):
        draw_grid_chess()
        self.levels[self.current_level].draw(self.screen)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        score_text = font_small.render(str(round(self.score, 2)), True, [255] * 3)
        self.screen.blit(score_text, (10, 10))

    def game_over(self):
        self.screen.fill("red")
        self.screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3)

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        global SCORE
        SCORE = 0
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pygame.display.set_caption(f"Snake Game - Level: {self.current_level}, Score: {self.score}")
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()