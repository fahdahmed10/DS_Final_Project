import pygame
import random
import math

pygame.init()
num_of_tiles = 32
tile_width = 25
tile_height = 15
height_shift = 100
WIDTH = num_of_tiles * tile_width
HEIGHT = num_of_tiles * tile_height + height_shift
APP = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")
Running = True
clock = pygame.time.Clock()

class Game:
    def __init__(self, map_width, map_height, num_of_tiles, height_shift):
        global WIDTH
        global HEIGHT
        self.map_width = map_width
        self.map_height = map_height
        self.height_shift = height_shift
        self.pacman_position = []
        self.ghost_position = []
        self.game_map = None
        self.num_of_tiles = num_of_tiles
        self.score = 0
        self.win = False
        self.ghost_speed = 10
        self.ghost_timer = 0
        self.pacman_speed = 5
        self.pacman_timer = 0
        self.level = 1
        self.playing = True
        self.animation_tick = 0
        self.small_font = pygame.font.SysFont("impact", 30)
        self.big_font = pygame.font.SysFont("impact", 40)
        self.title_text = "Pacman Game"
        self.lose_text = "loser  press R to restart"
        self.win_text = "Winner Press Enter to next level"
        self.pacman_image = pygame.image.load("pacman.png").convert_alpha()
        self.pacman_image = pygame.transform.smoothscale(self.pacman_image, (self.num_of_tiles, self.num_of_tiles))
        self.ghost_image = pygame.image.load("ghost.png").convert_alpha()
        self.ghost_image = pygame.transform.smoothscale(self.ghost_image, (self.num_of_tiles, self.num_of_tiles))
        self.eat_sound = pygame.mixer.Sound("pacman_eatfruit.wav")
        self.eat_sound.set_volume(0.1)
        self.win_sound = pygame.mixer.Sound("pacman_intermission.wav")
        self.lose_sound = pygame.mixer.Sound("pacman_death.wav")
        pygame.mixer.music.load("pacman_beginning.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.reset()

    def reset(self):
        self.win = False
        self.score = 0
        self.playing = True
        self.generate_map()

    def update(self):
        self.animation_tick += 1
        if self.playing:
            self.move_pacman()
            self.move_ghost()
            self.check_win()
            self.game_over()
        self.draw()

    def draw(self):
        float_offset = math.sin(self.animation_tick * 0.05) * 5
        title = self.big_font.render(self.title_text, True, "silver")
        title_rect = title.get_rect(center=(WIDTH // 2, self.height_shift // 2 + float_offset))
        APP.blit(title, title_rect)

        score_1 = self.small_font.render(f"score : {self.score}", True, "silver")
        level_1 = self.small_font.render(f"level : {self.level}", True, "silver")
        score_rect = score_1.get_rect(topleft=(10, self.height_shift // 2 - 10))
        level_rect = level_1.get_rect(topright=(WIDTH - 10, self.height_shift // 2 - 10))
        APP.blit(score_1, score_rect)
        APP.blit(level_1, level_rect)

        for row in range(self.map_height):
            for col in range(self.map_width):
                rect = pygame.Rect(col * self.num_of_tiles, row * self.num_of_tiles + self.height_shift, self.num_of_tiles, self.num_of_tiles)
                if self.game_map[row][col] == "#":
                    pygame.draw.rect(APP, "black", rect)
                elif self.game_map[row][col] == '.':
                    pygame.draw.circle(APP, "white", rect.center, 4)

        row_p, col_p = self.pacman_position
        rect_p = pygame.Rect(col_p * self.num_of_tiles, row_p * self.num_of_tiles + self.height_shift, self.num_of_tiles, self.num_of_tiles)
        APP.blit(self.pacman_image, rect_p.topleft)
        row_g, col_g = self.ghost_position
        rect_g = pygame.Rect(col_g * self.num_of_tiles, row_g * self.num_of_tiles + self.height_shift, self.num_of_tiles, self.num_of_tiles)
        APP.blit(self.ghost_image, rect_g.topleft)

        if not self.playing:
            scale = 1.0 + math.sin(self.animation_tick * 0.1) * 0.2
            if self.win:
                text = self.win_text
                color = "green"
            else:
                text = self.lose_text
                color = "red"
            font_size = int(40 * scale)
            font = pygame.font.SysFont("impact", font_size)
            msg = font.render(text, True, color)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            APP.blit(msg, rect)

    def generate_map(self):
        self.game_map = [["#" for _ in range(self.map_width)] for _ in range(self.map_height)]
        while True:
            for y in range(1, self.map_height - 1):
                for x in range(1, self.map_width - 1):
                    if random.random() < .15:
                        self.game_map[y][x] = "#"
                    else:
                        self.game_map[y][x] = '.'
            self.pacman_position = [1, 1]
            self.ghost_position = [self.map_height - 2, self.map_width - 2]
            self.game_map[1][1] = ' '
            self.game_map[self.map_height - 2][self.map_width - 2] = ' '
            if self.BFS(tuple(self.pacman_position), tuple(self.ghost_position)):
                return True

    def BFS(self, start, end):
        queue = [(start, [])]
        visited = set()
        visited.add(start)
        while queue:
            (y, x), path = queue.pop(0)
            if (y, x) == end:
                return path
            for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                y_new, x_new = y + dy, x + dx
                if (0 < x_new < self.map_width) and (0 < y_new < self.map_height) and self.game_map[y_new][x_new] != "#" and ((y_new, x_new) not in visited):
                    queue.append(((y_new, x_new), path + [(y_new, x_new)]))
                    visited.add((y_new, x_new))
        return []

    def move_pacman(self):
        self.pacman_timer += 1
        if self.pacman_timer == self.pacman_speed:
            key = pygame.key.get_pressed()
            y, x = self.pacman_position
            if key[pygame.K_UP] and self.game_map[y - 1][x] != "#":
                self.pacman_position = [y - 1, x]
            if key[pygame.K_DOWN] and self.game_map[y + 1][x] != "#":
                self.pacman_position = [y + 1, x]
            if key[pygame.K_RIGHT] and self.game_map[y][x + 1] != "#":
                self.pacman_position = [y, x + 1]
            if key[pygame.K_LEFT] and self.game_map[y][x - 1] != "#":
                self.pacman_position = [y, x - 1]
            y_new, x_new = self.pacman_position
            if self.game_map[y_new][x_new] == '.':
                self.score += 1
                self.game_map[y_new][x_new] = ' '
                self.eat_sound.play()
            self.pacman_timer = 0

    def move_ghost(self):
        self.ghost_timer += 1
        if self.ghost_timer == self.ghost_speed:
            path = self.BFS(tuple(self.ghost_position), tuple(self.pacman_position))
            if path:
                self.ghost_position = list(path[0])
            self.ghost_timer = 0

    def check_win(self):
        if all(cell != '.' for row in self.game_map for cell in row):
            self.win = True
            self.playing = False
            pygame.mixer.music.stop()
            self.win_sound.play()

    def game_over(self):
        if self.pacman_position == self.ghost_position:
            self.playing = False
            pygame.mixer.music.stop()
            self.lose_sound.play()

    def check_event(self):
        global Running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            if not self.playing and event.type == pygame.KEYDOWN:
                if self.win and event.key == pygame.K_RETURN:
                    self.level += 1
                    pygame.mixer.music.play(-1)
                    self.reset()
                    return
                if not self.win and event.key == pygame.K_r:
                    pygame.mixer.music.play(-1)
                    self.reset()
                    return

my_game = Game(tile_width, tile_height, num_of_tiles, height_shift)
while Running:
    my_game.check_event()
    APP.fill("blue")
    my_game.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
