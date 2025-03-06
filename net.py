import pygame
from settings import WIDTH, HEIGHT

# Net dimensions
NET_WIDTH = 25
NET_HEIGHT = 100

class Net:
    def __init__(self, x_pos, y_pos, facing_left=False):
        self.pos = [x_pos, y_pos]  # Position of the net (left or right side)
        self.width = NET_WIDTH
        self.height = NET_HEIGHT
        self.facing_left = facing_left  # Determines which side is the scoring side (left or right)

    def draw(self, screen):
        # Draw the vertical net (goal post)
        pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1], self.width, self.height), 3)  # White border

    def check_goal(self, puck, player):
        if self.facing_left:
            # Right side of the left net (scoring side)
            if self.pos[0] + self.width >= puck.pos[0] >= self.pos[0] and self.pos[1] <= puck.pos[1] <= self.pos[1] + self.height:
                # Goal scored, reset player and puck
                player.pos = [WIDTH // 2, HEIGHT // 2]  # Reset player position
                puck.pos = [WIDTH // 2, HEIGHT // 2]  # Reset puck position
                return True  # Goal scored
        else:
            # Left side of the right net (scoring side)
            if self.pos[0] <= puck.pos[0] <= self.pos[0] + self.width and self.pos[1] <= puck.pos[1] <= self.pos[1] + self.height:
                # Goal scored, reset player and puck
                player.pos = [WIDTH // 2, HEIGHT // 2]  # Reset player position
                puck.pos = [WIDTH // 2, HEIGHT // 2]  # Reset puck position
                return True  # Goal scored
        return False
