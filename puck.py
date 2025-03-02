import pygame
import math
from settings import WIDTH, HEIGHT  # Import screen dimensions

puck_size = 10  # Puck size
puck_speed = 7  # Puck speed
friction = 0.99  # Puck friction
player_size = 20  # Player size

# Define margin to prevent touching edges
MARGIN = 0

class Puck:
    def __init__(self):
        self.pos = [WIDTH // 2, HEIGHT // 2]  # Initial puck position
        self.vel = [0, 0]  # Puck velocity
        self.has_owner = False  # Whether the player has the puck

    def handle(self, player):
        # Check if player is close enough to take possession
        distance = math.sqrt((player.pos[0] - self.pos[0])**2 + (player.pos[1] - self.pos[1])**2)

        if distance < player_size + puck_size and not self.has_owner:
            self.has_owner = True
            player.has_puck = True

        if self.has_owner:
            # Attach puck to player's stick
            self.pos[0] = player.pos[0] + player.angle[0] * (player_size + puck_size)
            self.pos[1] = player.pos[1] + player.angle[1] * (player_size + puck_size)
            self.vel = [0, 0]  # Reset velocity

        else:
            # Apply friction to puck velocity
            self.vel[0] *= friction
            self.vel[1] *= friction

            # Move puck
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            # Bounce off walls with margin
            if self.pos[0] <= puck_size + MARGIN or self.pos[0] >= WIDTH - puck_size - MARGIN:
                self.vel[0] = -self.vel[0]
            if self.pos[1] <= puck_size + MARGIN or self.pos[1] >= HEIGHT - puck_size - MARGIN:
                self.vel[1] = -self.vel[1]

    def shoot(self, player, mouse_pos, shot_power):
        if self.has_owner:
            # Calculate shot direction
            angle = math.atan2(mouse_pos[1] - player.pos[1], mouse_pos[0] - player.pos[0])
            self.vel = [math.cos(angle) * shot_power, math.sin(angle) * shot_power]

            # Release puck
            self.has_owner = False
            player.has_puck = False

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos[0]), int(self.pos[1])), puck_size)
