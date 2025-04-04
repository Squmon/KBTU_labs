from math import floor
import random
import pygame
from color_palette import *
import time

pygame.init()


size = 1000
WIDTH = size
HEIGHT = size

screen = pygame.display.set_mode((HEIGHT, WIDTH))

font_small = pygame.font.SysFont("Verdana", 20) # для счетчика

font = pygame.font.SysFont("Verdana", 60)
image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))

cell_count = 20
SCORE = 0
CELL = size // cell_count

def draw_grid():
    for i in range(cell_count):
        for j in range(cell_count):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [(100, 100, 100), (50, 50, 50)]

    for i in range(cell_count):
        for j in range(cell_count):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __eq__(self, value:'Point'):
        return self.x == value.x and self.y == value.y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x = (self.body[0].x + self.dx) % cell_count
        self.body[0].y = (self.body[0].y + self.dy) % cell_count

    @property
    def outside(self) -> bool:
        return not (0 <= self.body[0].x < cell_count and 0 <= self.body[0].y < cell_count)

    def check_self_intersect(self):
        for a in self.body:
            for b in self.body:
                if a is not b:
                    if a == b:
                        return True
        return False

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def update_food(self, food):
        global SCORE, LEVEL
        head = self.body[0]
        if head == food.pos:
            SCORE += food.weight
            while head == food.pos:
                food.set_random_position()
            self.body.append(Point(head.x + self.dx, head.y + self.dy))
            if floor(SCORE) % 5 == 4:
                LEVEL += 1

class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = random.random()
        self.timer = 1

    def draw(self):
        global LEVEL
        self.timer -= 0.01/LEVEL
        pygame.draw.rect(screen, (0, int(255*self.weight), 0), (self.timer*self.pos.x * CELL + (1-self.timer)*(self.pos.x * CELL + CELL/2),
                                                                self.timer*self.pos.y * CELL + (1-self.timer)*(self.pos.y * CELL + CELL/2),
                                                                CELL*self.timer, CELL*self.timer))
        if self.timer <= 0:
            self.set_random_position()

    def set_random_position(self):
        self.timer = 1
        self.weight = random.random()
        self.pos = Point(random.randint(0, cell_count - 1), random.randint(0, cell_count - 1))


FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()

LEVEL = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if snake.dx == 0:
                    snake.dx = 1
                    snake.dy = 0
                    break
            elif event.key == pygame.K_LEFT:
                if snake.dx == 0:
                    snake.dx = -1
                    snake.dy = 0
                    break
            elif event.key == pygame.K_DOWN:
                if snake.dy == 0:
                    snake.dx = 0
                    snake.dy = 1
                    break
            elif event.key == pygame.K_UP:
                if snake.dy == 0:
                    snake.dx = 0
                    snake.dy = -1
                    break

    draw_grid_chess()
    scores = font_small.render(str(round(SCORE, 2)), True, [255]*3)
    screen.blit(scores, (10, 10))

    snake.move()
    snake.update_food(food)

    if snake.check_self_intersect():
        time.sleep(1)

        running = False
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(3)
        pygame.quit()
        quit()

    snake.draw()
    food.draw()

    pygame.display.flip()
    clock.tick(FPS*LEVEL) # сложность игры

pygame.quit()