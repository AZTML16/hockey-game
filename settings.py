import pygame

# Initialize pygame
pygame.init()

# Get screen size dynamically
info = pygame.display.Info()
WIDTH = info.current_w  # Full screen width
HEIGHT = info.current_h  # Full screen height

# Set FPS
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.NOFRAME)  # No borders but not fullscreen

# Clock for managing FPS
clock = pygame.time.Clock()
