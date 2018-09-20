"""Main module to run Pong-Lan game."""
import sys
from os import path
from math import floor
import pygame
import socket
from Client.pong_menu import PongMenu

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

  FONT = pygame.font.Font(path.join(path.dirname(__file__), "Client", "src", "bit5x3.ttf"), 12)
  menu = PongMenu()
  active_scene = menu

  while True:
    # print("oi")
    # if state == MENU:
    #   pass
    # elif state == INGAME:
    #   pass
    pressed_keys = pygame.key.get_pressed()
    filtered_events = []
    for event in pygame.event.get():
      quit_attempt = False
      if event.type == pygame.QUIT:
        quit_attempt = True
      elif event.type == pygame.KEYDOWN:
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        if event.key == pygame.K_ESCAPE:
          quit_attempt = True
        elif event.key == pygame.K_F4 and alt_pressed:
          quit_attempt = True

      if quit_attempt:
        pygame.quit()
        sys.exit()
      else:
        filtered_events.append(event)

    screen.fill(BLACK)
    active_scene.update(filtered_events, pressed_keys)
    active_scene.render(screen)
    render_fps(FONT, screen, floor(clock.get_fps()))
    pygame.display.update()
    clock.tick(60)
