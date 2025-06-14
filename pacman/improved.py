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

class Particle:
    def __init__(self, x, y, color, velocity_x=None, velocity_y=None, size=4, lifetime=60):
        self.x = x
        self.y = y
        self.vx = velocity_x if velocity_x else random.uniform(-3, 3)
        self.vy = velocity_y if velocity_y else random.uniform(-3, 3)
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.1
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        
    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color_with_alpha = (*self.color, alpha)
            temp_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, color_with_alpha, (self.size, self.size), self.size)
            surface.blit(temp_surf, (self.x - self.size, self.y - self.size))

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
        
        self.particles = []
        self.death_animation_timer = 0
        self.death_animation_active = False
        self.eat_animation_scale = 1.0
        self.eat_animation_timer = 0
        self.shake_intensity = 0
        
        try:
            self.small_font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 52)
        except:
            self.small_font = pygame.font.SysFont("consolas", 30, bold=True)
            self.big_font = pygame.font.SysFont("consolas", 42, bold=True)
            
        self.title_text = "PACMAN NEON"
        self.lose_text = "GAME OVER - PRESS R TO RESTART"
        self.win_text = "LEVEL COMPLETE - PRESS ENTER FOR NEXT"
        
        try:
            self.pacman_image = pygame.image.load("pacman.png").convert_alpha()
            self.pacman_image = pygame.transform.smoothscale(self.pacman_image, (self.num_of_tiles, self.num_of_tiles))
            self.ghost_image = pygame.image.load("ghost.png").convert_alpha()
            self.ghost_image = pygame.transform.smoothscale(self.ghost_image, (self.num_of_tiles, self.num_of_tiles))
        except:
            self.pacman_image = pygame.Surface((self.num_of_tiles, self.num_of_tiles), pygame.SRCALPHA)
            pygame.draw.circle(self.pacman_image, (255, 255, 0), (self.num_of_tiles//2, self.num_of_tiles//2), self.num_of_tiles//2 - 2)
            self.ghost_image = pygame.Surface((self.num_of_tiles, self.num_of_tiles), pygame.SRCALPHA)
            pygame.draw.circle(self.ghost_image, (255, 100, 150), (self.num_of_tiles//2, self.num_of_tiles//2), self.num_of_tiles//2 - 2)
        
        try:
            self.eat_sound = pygame.mixer.Sound("pacman_eatfruit.wav")
            self.eat_sound.set_volume(0.1)
            self.win_sound = pygame.mixer.Sound("pacman_intermission.wav")
            self.lose_sound = pygame.mixer.Sound("pacman_death.wav")
            pygame.mixer.music.load("pacman_beginning.wav")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            self.eat_sound = None
            self.win_sound = None
            self.lose_sound = None
            
        self.reset()

    def reset(self):
        self.win = False
        self.score = 0
        self.playing = True
        self.particles = []
        self.death_animation_active = False
        self.death_animation_timer = 0
        self.shake_intensity = 0
        self.generate_map()

    def add_eat_particles(self, x, y):
        for _ in range(6):
            particle = Particle(x, y, (255, 255, 100), 
                              random.uniform(-2, 2), random.uniform(-3, -1), 
                              random.randint(3, 5), random.randint(30, 50))
            self.particles.append(particle)

    def add_death_particles(self, x, y):
        for _ in range(12):
            particle = Particle(x, y, (255, 50, 50), 
                              random.uniform(-4, 4), random.uniform(-4, 4), 
                              random.randint(4, 7), random.randint(60, 90))
            self.particles.append(particle)

    def update(self):
        self.animation_tick += 1
        
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
            
        if self.death_animation_active:
            self.death_animation_timer += 1
            self.shake_intensity = max(0, 10 - self.death_animation_timer // 5)
            if self.death_animation_timer > 120:
                self.death_animation_active = False
                self.shake_intensity = 0
                
        if self.eat_animation_timer > 0:
            self.eat_animation_timer -= 1
            self.eat_animation_scale = 1.0 + (self.eat_animation_timer / 15.0) * 0.3
        else:
            self.eat_animation_scale = 1.0
            
        if self.playing:
            self.move_pacman()
            self.move_ghost()
            self.check_win()
            self.game_over()
        self.draw()

    def draw(self):
        shake_x = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        shake_y = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        
        for y in range(HEIGHT):
            intensity = int(15 + (y / HEIGHT) * 25)
            pygame.draw.line(APP, (0, 0, intensity), (0, y), (WIDTH, y))
        
        float_offset = math.sin(self.animation_tick * 0.05) * 5
        glow_intensity = int(100 + math.sin(self.animation_tick * 0.1) * 50)
        
        for i in range(3):
            glow_r = max(0, min(255, glow_intensity - i * 30))
            glow_g = max(0, min(255, glow_intensity + i * 20))
            glow_color = (0, glow_r, glow_g)
            title_glow = self.big_font.render(self.title_text, True, glow_color)
            title_glow.set_alpha(100 - i * 30)
            title_rect_glow = title_glow.get_rect(center=(WIDTH // 2 + i + shake_x, self.height_shift // 2 + float_offset + i + shake_y))
            APP.blit(title_glow, title_rect_glow)
            
        title = self.big_font.render(self.title_text, True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2 + shake_x, self.height_shift // 2 + float_offset + shake_y))
        APP.blit(title, title_rect)

        score_pulse = 1.0 + math.sin(self.animation_tick * 0.15) * 0.1
        level_pulse = 1.0 + math.sin(self.animation_tick * 0.15 + math.pi/2) * 0.1
        
        score_font_size = int(30 * score_pulse)
        level_font_size = int(30 * level_pulse)
        
        try:
            score_font = pygame.font.Font(None, score_font_size)
            level_font = pygame.font.Font(None, level_font_size)
        except:
            score_font = self.small_font
            level_font = self.small_font
            
        score_1 = score_font.render(f"SCORE: {self.score}", True, (0, 255, 200))
        level_1 = level_font.render(f"LEVEL: {self.level}", True, (255, 150, 0))
        score_rect = score_1.get_rect(topleft=(10 + shake_x, self.height_shift // 2 - 10 + shake_y))
        level_rect = level_1.get_rect(topright=(WIDTH - 10 + shake_x, self.height_shift // 2 - 10 + shake_y))
        APP.blit(score_1, score_rect)
        APP.blit(level_1, level_rect)

        for row in range(self.map_height):
            for col in range(self.map_width):
                rect = pygame.Rect(col * self.num_of_tiles + shake_x, row * self.num_of_tiles + self.height_shift + shake_y, self.num_of_tiles, self.num_of_tiles)
                if self.game_map[row][col] == "#":
                    wall_color = (0, 100 + int(math.sin(self.animation_tick * 0.1) * 30), 150)
                    pygame.draw.rect(APP, wall_color, rect)
                    pygame.draw.rect(APP, (0, 150, 255), rect, 2)
                elif self.game_map[row][col] == '.':
                    dot_pulse = 1.0 + math.sin(self.animation_tick * 0.3 + row * 0.5 + col * 0.5) * 0.4
                    dot_size = int(4 * dot_pulse)
                    dot_color = (255, 255, int(200 + math.sin(self.animation_tick * 0.2) * 55))
                    pygame.draw.circle(APP, dot_color, rect.center, dot_size)

        row_p, col_p = self.pacman_position
        pacman_x = col_p * self.num_of_tiles + shake_x
        pacman_y = row_p * self.num_of_tiles + self.height_shift + shake_y
        
        if self.eat_animation_scale > 1.0:
            scaled_size = int(self.num_of_tiles * self.eat_animation_scale)
            scaled_pacman = pygame.transform.scale(self.pacman_image, (scaled_size, scaled_size))
            offset = (scaled_size - self.num_of_tiles) // 2
            APP.blit(scaled_pacman, (pacman_x - offset, pacman_y - offset))
        else:
            rotation_angle = math.sin(self.animation_tick * 0.2) * 10
            rotated_pacman = pygame.transform.rotate(self.pacman_image, rotation_angle)
            rotated_rect = rotated_pacman.get_rect(center=(pacman_x + self.num_of_tiles//2, pacman_y + self.num_of_tiles//2))
            APP.blit(rotated_pacman, rotated_rect)
        
        row_g, col_g = self.ghost_position
        ghost_x = col_g * self.num_of_tiles + shake_x
        ghost_y = row_g * self.num_of_tiles + self.height_shift + shake_y
        
        ghost_bob = math.sin(self.animation_tick * 0.25) * 3
        ghost_scale = 1.0 + math.sin(self.animation_tick * 0.3) * 0.1
        
        if self.death_animation_active:
            ghost_scale += math.sin(self.death_animation_timer * 0.5) * 0.3
            
        scaled_ghost_size = int(self.num_of_tiles * ghost_scale)
        scaled_ghost = pygame.transform.scale(self.ghost_image, (scaled_ghost_size, scaled_ghost_size))
        ghost_offset = (scaled_ghost_size - self.num_of_tiles) // 2
        APP.blit(scaled_ghost, (ghost_x - ghost_offset, ghost_y - ghost_offset + ghost_bob))

        for particle in self.particles:
            particle.draw(APP)

        if not self.playing:
            text_scale = 1.0 + math.sin(self.animation_tick * 0.2) * 0.15
            text_glow = int(150 + math.sin(self.animation_tick * 0.3) * 100)
            
            if self.win:
                text = self.win_text
                text_color = (0, 255, 150)
                glow_color = (0, text_glow, 100)
            else:
                text = self.lose_text
                text_color = (255, 100, 100)
                glow_color = (text_glow, 50, 50)
            
            try:
                font_size = int(36 * text_scale)
                scaled_font = pygame.font.Font(None, font_size)
            except:
                scaled_font = self.big_font
                
            for i in range(3):
                glow_r = max(0, min(255, text_glow)) if self.win else max(0, min(255, text_glow))
                glow_g = max(0, min(255, 100)) if self.win else max(0, min(255, 50))
                glow_b = max(0, min(255, 100)) if self.win else max(0, min(255, 50))
                final_glow_color = (glow_r, glow_g, glow_b)
                glow_msg = scaled_font.render(text, True, final_glow_color)
                glow_msg.set_alpha(80 - i * 20)
                glow_rect = glow_msg.get_rect(center=(WIDTH // 2 + i, HEIGHT // 2 + i))
                APP.blit(glow_msg, glow_rect)
                
            msg = scaled_font.render(text, True, text_color)
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
                
                eat_x = x_new * self.num_of_tiles + self.num_of_tiles // 2
                eat_y = y_new * self.num_of_tiles + self.height_shift + self.num_of_tiles // 2
                self.add_eat_particles(eat_x, eat_y)
                self.eat_animation_timer = 15
                
                if self.eat_sound:
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
            if self.win_sound:
                pygame.mixer.music.stop()
                self.win_sound.play()

    def game_over(self):
        if self.pacman_position == self.ghost_position:
            self.playing = False
            self.death_animation_active = True
            self.death_animation_timer = 0
            
            death_x = self.pacman_position[1] * self.num_of_tiles + self.num_of_tiles // 2
            death_y = self.pacman_position[0] * self.num_of_tiles + self.height_shift + self.num_of_tiles // 2
            self.add_death_particles(death_x, death_y)
            
            if self.lose_sound:
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
                    if pygame.mixer.music:
                        pygame.mixer.music.play(-1)
                    self.reset()
                    return
                if not self.win and event.key == pygame.K_r:
                    if pygame.mixer.music:
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



# this animations using ai