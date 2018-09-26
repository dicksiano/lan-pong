"""Main module to run Pong-Lan game."""
import sys
from os import path
from math import floor
import pygame
from Server.server import Server
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
class Main:
  """Main program"""
  def __init__(self):
    self.msg = {
        'filtered_events':[],
        'pressed_keys': [],
        'servers': [],
        'update_servers': False
    }

    # pygame statements
    pygame.init()
    pygame.display.set_caption('Pong-Lan')
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Screens Statements
    self.state = MENU
    self.font = pygame.font.Font(path.join(path.dirname(__file__), \
    "Client", "src", "bit5x3.ttf"), 12)
    self.menu = PongMenu()
    self.active_scene = self.menu

    # Client / Server
    self.client = Client()
    self.client.search_servers()

    self.server = None

  def handle_client_events(self, client):
    """Handle Client events"""
    if client.updated_state:
      client.updated_state = False
      self.msg['servers'] = client.available_servers
      self.msg['update_servers'] = True

  def handle_acscene_events(self):
    """Handle Active Scene Events"""
    if self.active_scene.ref_servers_clicked:
      self.active_scene.ref_servers_clicked = False
      self.client.search_servers()

    if self.active_scene.ref_nic_clicked:
      self.active_scene.ref_nic_clicked = False
      self.active_scene.load_ip_options()

    if self.active_scene.play_clicked:
      self.active_scene.play_clicked = False
      if self.active_scene.server_selected:
        ip_addr = self.active_scene.server_selected['tcp_addr']
        print(ip_addr)
        self.client.tcp_connect(tuple(ip_addr))
      else:
        print("Cannot play: No selected server")

    if self.active_scene.create_server_clicked:
      self.active_scene.create_server_clicked = False
      if self.active_scene.nic_selected:
        ip_addr = self.active_scene.nic_selected['ip']
        self.active_scene.ref_servers_clicked = True
        self.server = Server(ip=ip_addr)
        self.server.wait_conn()
      else:
        print("Cannot create server: No IP selected")

  def render_fps(self):
    """Render fps text on screen"""
    fps = floor(self.clock.get_fps())
    fps_text = self.font.render(str(fps), True, WHITE)
    self.screen.blit(fps_text, (0, self.screen.get_height()-fps_text.get_height()))

  def run(self):
    """Run main program"""
    while True:
      # print("oi")
      # if state == MENU:
      #   pass
      # elif state == INGAME:
      #   pass
      self.msg['pressed_keys'] = pygame.key.get_pressed()
      self.msg['filtered_events'] = []
      for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
          quit_attempt = True
        elif event.type == pygame.KEYDOWN:
          alt_pressed = self.msg['pressed_keys'][pygame.K_LALT] or \
          self.msg['pressed_keys'][pygame.K_RALT]
          if event.key == pygame.K_ESCAPE:
            quit_attempt = True
          elif event.key == pygame.K_F4 and alt_pressed:
            quit_attempt = True

        if quit_attempt:
          if self.server:
            self.server.quit = True
          pygame.quit()
          sys.exit()
        else:
          self.msg['filtered_events'].append(event)

      self.handle_client_events(self.client)
      self.handle_acscene_events()
      self.active_scene.update(self.msg)


      self.screen.fill(BLACK)
      self.active_scene.render(self.screen)
      self.render_fps()
      pygame.display.update()

      if self.msg['update_servers']:
        self.msg['update_servers'] = False

      self.clock.tick(60)


if __name__ == "__main__":
  MAIN = Main()
  MAIN.run()
