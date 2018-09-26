"""Main module to run Pong-Lan game."""
import sys
from os import path
from math import floor
import pygame
from Server.server import Server
from Client.client import Client
from Client.pong_menu import PongMenu
from Client.game_scene import GameScene

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
    self.game_scene = GameScene()
    self.active_scene = self.menu

    # Client / Server
    self.client = Client()
    self.client.search_servers()

    self.server = None

  def process_ev_to_client(self):
    msg = []
    for event in self.msg['filtered_events']:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          msg.append(("KEYDOWN", "K_UP"))
        elif event.key == pygame.K_DOWN:
          msg.append(("KEYDOWN", "K_DOWN"))
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          msg.append(("KEYUP", "K_UP"))
        elif event.key == pygame.K_DOWN:
          msg.append(("KEYUP", "K_DOWN"))
    return msg

  def handle_client_events(self):
    """Handle Client events"""
    if self.client.updated_state:
      self.client.updated_state = False
      self.msg['servers'] = self.client.available_servers
      self.msg['update_servers'] = True

    if self.client.connected:
      self.client.handle_tcp(self.process_ev_to_client())

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
        self.client.tcp_connect(tuple(ip_addr))

        print('\n\n\n\n aq\n\n\n')
        self.state = INGAME
        self.active_scene = self.game_scene
      else:
        print("Cannot play: No selected server")

    if self.state == MENU:
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
<<<<<<< HEAD

      self.handle_client_events()
=======
      
      self.handle_client_events(self.client)
>>>>>>> 062d4cc01c5a51fd75f3f123c4eece1d4c8a5438
      self.handle_acscene_events()
      if self.state == MENU:
        self.active_scene.update(self.msg)

      self.screen.fill(BLACK)
      
      if self.state == MENU:
        self.active_scene.render(self.screen)
      elif self.state == INGAME:
        self.active_scene.draw(self.screen, [0,0], [0,0], [0,0])

      self.render_fps()
      pygame.display.update()

      if self.msg['update_servers']:
        self.msg['update_servers'] = False

      self.clock.tick(60)


if __name__ == "__main__":
  MAIN = Main()
  MAIN.run()
