"""Main module to run Pong-Lan game."""
import sys
from os import path, getcwd
from math import floor
import pygame
from pong_menu import PongMenu

# States
INGAME = 0
MENU = 1

# Screen
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def render_fps(font, surface, fps):
  """Render fps text on screen"""
  fps_text = font.render(str(fps), True, WHITE)
  surface.blit(fps_text, (0, surface.get_height()-fps_text.get_height()))


if __name__ == "__main__":
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Pong-Lan')
  state = MENU
  
  FONT = pygame.font.Font(path.join(getcwd(), "src", "bit5x3.ttf"), 12)
  menu = PongMenu()
  active_scene = menu

  while True:
    # print("oi")
    # if state == MENU:
    #   pass
    # elif state == INGAME:
    #   pass
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    screen.fill(BLACK)
    active_scene.update()
    active_scene.render(screen)
    render_fps(FONT, screen, floor(clock.get_fps()))
    pygame.display.update()
    clock.tick(60)
