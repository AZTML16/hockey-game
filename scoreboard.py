import pygame

class Scoreboard:
    def __init__(self, x, y, fps):  # Accept fps as an argument
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
        self.fps = fps  # Store FPS value

    def update_score(self, left_score, right_score):
        self.left_score = left_score
        self.right_score = right_score

    def update_timer(self):
        # Decrease the timer 10 times faster (decrement by 10 seconds per frame)
        self.timer -= 10 / self.fps  # Use the passed FPS

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
