import pygame
import math
import time
from settings import WIDTH, HEIGHT, FPS, screen, clock
from player import Player
from puck import Puck, puck_speed
from net import Net  # Import the Net class

# Initialize pygame
pygame.init()

# Fixed size for the play area (800x600)
PLAY_AREA_WIDTH = int(WIDTH * 0.8)
PLAY_AREA_HEIGHT = int(HEIGHT * 0.8)

# Player and puck sizes
player_size = 20
puck_size = 10

# Game setup
player = Player()
puck = Puck()

# Create nets (placed near the left and right edges)
net1 = Net(PLAY_AREA_WIDTH // 4 - 12, HEIGHT // 2 - 50, facing_left=True)  # Left net (right side is the scoring side)
net2 = Net(4 * PLAY_AREA_WIDTH // 4 - 12, HEIGHT // 2 - 50, facing_left=False)  # Right net (left side is the scoring side)

# Scoreboard setup
class Scoreboard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("Arial", 36)
        self.timer_font = pygame.font.SysFont("Arial", 28)
        self.left_score = 0
        self.right_score = 0
        self.timer = 1200  # Start the timer at 20:00 (in seconds)
        self.box_padding = 10  # Padding for the box around the scoreboard
        self.score_padding = 100  # Increased space between the scores (enough space for the timer)
        self.timer_padding = 20  # Space to separate the timer from the scores

    def update_score(self, left_score, right_score):
        self.left_score = left_score
        self.right_score = right_score

    def update_timer(self):
        # Decrease the timer 10 times faster (decrement by 10 seconds per frame)
        self.timer -= 10 / FPS

    def draw(self, screen):
        left_text = self.font.render(str(self.left_score), True, (255, 255, 255))
        right_text = self.font.render(str(self.right_score), True, (255, 255, 255))

        # Format the timer as MM:SS
        minutes = int(self.timer // 60)
        seconds = int(self.timer % 60)
        timer_text = self.timer_font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))

        # Calculate the total width and height of the box (including space for both scores, timer, and additional padding)
        box_width = (left_text.get_width() + right_text.get_width() +
                     self.score_padding + self.timer_padding + timer_text.get_width() + 2 * self.box_padding)
        box_height = max(left_text.get_height(), right_text.get_height()) + 2 * self.box_padding

        # Draw the box around the scores and timer
        pygame.draw.rect(screen, (255, 255, 255), (self.x - box_width // 2, self.y - self.box_padding, box_width, box_height), 2)

        # Draw the flipped scores inside the box
        screen.blit(right_text, (self.x - box_width // 4, self.y))  # Right score (now on the left side)
        screen.blit(left_text, (self.x + box_width // 4 - left_text.get_width(), self.y))  # Left score (now on the right side)

        # Draw the timer in the center
        screen.blit(timer_text, (self.x - timer_text.get_width() // 2, self.y + left_text.get_height() // 2))

# Initialize the scoreboard
scoreboard = Scoreboard(WIDTH // 2, 20)

# Main game loop
running = True
while running:
    # Get current window size
    window_width, window_height = screen.get_size()  # Get updated window size

    # Calculate the offset to center the fixed-size play area in the window
    offset_x = (WIDTH - PLAY_AREA_WIDTH) // 2
    offset_y = (HEIGHT - PLAY_AREA_HEIGHT) // 2

    # Fill screen with black
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Player controls
    player.handle()

    # Puck handling
    puck.handle(player)

    # Shooting the puck with left-click (mouse)
    if pygame.mouse.get_pressed()[0] and player.has_puck:  # Left-click
        mouse_pos = pygame.mouse.get_pos()
        puck.shoot(player, mouse_pos, puck_speed)

    # Constrain player position within the white lines (play area)
    player.pos[0] = max(offset_x + player_size, min(player.pos[0], offset_x + PLAY_AREA_WIDTH - player_size))
    player.pos[1] = max(offset_y + player_size, min(player.pos[1], offset_y + PLAY_AREA_HEIGHT - player_size))

    # Constrain puck position within the white lines (play area)
    puck.pos[0] = max(offset_x + puck_size, min(puck.pos[0], offset_x + PLAY_AREA_WIDTH - puck_size))
    puck.pos[1] = max(offset_y + puck_size, min(puck.pos[1], offset_y + PLAY_AREA_HEIGHT - puck_size))

    # Handle puck bouncing off the white lines (top, bottom, left, right)
    if puck.pos[0] <= offset_x + puck_size or puck.pos[0] >= offset_x + PLAY_AREA_WIDTH - puck_size:
        puck.vel[0] = -puck.vel[0]  # Reverse horizontal velocity
    if puck.pos[1] <= offset_y + puck_size or puck.pos[1] >= offset_y + PLAY_AREA_HEIGHT - puck_size:
        puck.vel[1] = -puck.vel[1]  # Reverse vertical velocity

    # Detect if player is touching the white lines (left, right, top, or bottom edges)
    if player.pos[0] <= offset_x + player_size or player.pos[0] >= offset_x + PLAY_AREA_WIDTH - player_size:
        player.vel[0] = -player.vel[0]  # Reverse horizontal velocity if touching the white line
    if player.pos[1] <= offset_y + player_size or player.pos[1] >= offset_y + PLAY_AREA_HEIGHT - player_size:
        player.vel[1] = -player.vel[1]  # Reverse vertical velocity if touching the white line

    # Check if puck has scored in any net
    if net1.check_goal(puck, player):
        print("Goal in left net!")
        scoreboard.update_score(scoreboard.left_score + 1, scoreboard.right_score)  # Update left score
        puck.pos = [WIDTH // 2, HEIGHT // 2]  # Reset puck position
        puck.vel = [0, 0]  # Stop puck

    if net2.check_goal(puck, player):
        print("Goal in right net!")
        scoreboard.update_score(scoreboard.left_score, scoreboard.right_score + 1)  # Update right score
        puck.pos = [WIDTH // 2, HEIGHT // 2]  # Reset puck position
        puck.vel = [0, 0]  # Stop puck

    # Draw the player, puck, and nets
    player.draw(screen)
    puck.draw(screen)
    net1.draw(screen)  # Draw the left net
    net2.draw(screen)  # Draw the right net

    # Draw the white lines (acting as the boundary)
    pygame.draw.line(screen, (255, 255, 255), (offset_x, offset_y), (offset_x + PLAY_AREA_WIDTH, offset_y), 5)  # Top line
    pygame.draw.line(screen, (255, 255, 255), (offset_x, offset_y), (offset_x, offset_y + PLAY_AREA_HEIGHT), 5)  # Left line
    pygame.draw.line(screen, (255, 255, 255), (offset_x + PLAY_AREA_WIDTH, offset_y), (offset_x + PLAY_AREA_WIDTH, offset_y + PLAY_AREA_HEIGHT), 5)  # Right line
    pygame.draw.line(screen, (255, 255, 255), (offset_x, offset_y + PLAY_AREA_HEIGHT), (offset_x + PLAY_AREA_WIDTH, offset_y + PLAY_AREA_HEIGHT), 5)  # Bottom line

    # Update the timer (4 times faster)
    scoreboard.update_timer()

    # Draw the scoreboard with flipped scores and timer in the center
    scoreboard.draw(screen)

    # Update the display
    pygame.display.flip()

    # Maintain FPS
    clock.tick(FPS)

pygame.quit()
