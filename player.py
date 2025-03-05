import pygame
import math
from settings import WIDTH, HEIGHT  # Import screen dimensions

player_size = 20  # Player size
friction = 0.9  # Friction for player movement
speed = 3  # Player speed
max_speed = 5  # Limit to prevent infinite acceleration

# Define margin to prevent touching edges
MARGIN = 0

class Player:
    def __init__(self):
        self.pos = [WIDTH // 2, HEIGHT // 2]  # Starting position at the center of the screen
        self.vel = [0, 0]  # Starting velocity
        self.angle = [0, 0]  # Angle facing direction
        self.has_puck = False  # Whether the player has the puck

    def handle(self):
        keys = pygame.key.get_pressed()

        # Movement (WASD or Arrow keys)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel[0] -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel[0] += speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel[1] -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel[1] += speed

        # Stop instantly when pressing Q
        if keys[pygame.K_q]:
            self.vel = [0, 0]

        # Apply friction
        self.vel[0] *= friction
        self.vel[1] *= friction

        # Limit max speed
        self.vel[0] = max(-max_speed, min(self.vel[0], max_speed))
        self.vel[1] = max(-max_speed, min(self.vel[1], max_speed))

        # Move player
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Keep player inside screen bounds with margin
        self.pos[0] = max(player_size + MARGIN, min(self.pos[0], WIDTH - player_size - MARGIN))
        self.pos[1] = max(player_size + MARGIN, min(self.pos[1], HEIGHT - player_size - MARGIN))

        # Update angle to face mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - self.pos[0], mouse_y - self.pos[1]
        angle = math.atan2(dy, dx)
        self.angle = [math.cos(angle), math.sin(angle)]

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.pos[0]), int(self.pos[1])), player_size)
