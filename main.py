"""Main module to run Pong-Lan game."""
import sys
from os import path
from math import floor
import pygame
import socket
from Client.client import Client
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

# "MVC" message model
msg = {
    'filtered_events':[],
    'pressed_keys': [],
    'servers': [],
    'update_servers': False
}

def render_fps(font, surface, fps):
  """Render fps text on screen"""
  fps_text = font.render(str(fps), True, WHITE)
  surface.blit(fps_text, (0, surface.get_height()-fps_text.get_height()))


if __name__ == "__main__":
  # pygame statements
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Pong-Lan')

  # Screens Statements
  state = MENU
  FONT = pygame.font.Font(path.join(path.dirname(__file__), "Client", "src", "bit5x3.ttf"), 12)
  menu = PongMenu()
  active_scene = menu

  # Client / Server
  client = Client()
  client.search_servers()
  msg['servers'] = client.available_servers
  msg['update_servers'] = True

  while True:
    # print("oi")
    # if state == MENU:
    #   pass
    # elif state == INGAME:
    #   pass
    msg['pressed_keys'] = pygame.key.get_pressed()
    msg['filtered_events'] = []
    for event in pygame.event.get():
      quit_attempt = False
      if event.type == pygame.QUIT:
        quit_attempt = True
      elif event.type == pygame.KEYDOWN:
        alt_pressed = msg['pressed_keys'][pygame.K_LALT] or \
        msg['pressed_keys'][pygame.K_RALT]
        if event.key == pygame.K_ESCAPE:
          quit_attempt = True
        elif event.key == pygame.K_F4 and alt_pressed:
          quit_attempt = True

      if quit_attempt:
        pygame.quit()
        sys.exit()
      else:
        msg['filtered_events'].append(event)

    active_scene.update(msg)


    screen.fill(BLACK)
    active_scene.render(screen)
    render_fps(FONT, screen, floor(clock.get_fps()))
    pygame.display.update()

    if msg['update_servers']: msg['update_servers'] = False

    clock.tick(60)
