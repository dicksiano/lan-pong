"""Class of Menu Scene in Pong-Lan game"""
from os import path
import socket
import pygame
from .scene_base import SceneBase

WHITE = (255, 255, 255)

class PongMenu(SceneBase):
  """Menu Scene in Pong-Lan game."""
  def __init__(self):
    SceneBase.__init__(self)

    # Available ips to create server
    self.nic_info = []
    self.nic_info_text = []


    # PONG title
    font = pygame.font.Font(path.join(path.dirname(__file__), "src", "bit5x3.ttf"), 130)
    self.pong_text = font.render("PONG", False, WHITE)

    # Servers title
    font = pygame.font.Font(path.join(path.dirname(__file__), "src", "bit5x3.ttf"), 35)
    self.servers_text = font.render("SERVERS", False, WHITE)

    # Play Title
    font = pygame.font.Font(path.join(path.dirname(__file__), "src", "bit5x3.ttf"), 45)
    self.play_text = font.render("PLAY", False, WHITE)
    self.play_rect = None

    # Create Server Title
    font = pygame.font.Font(path.join(path.dirname(__file__), "src", "bit5x3.ttf"), 45)
    self.create_server_text = font.render("CREATE SERVER", False, WHITE)
    self.create_server_rect = None

    self.mouse_pos = (0, 0)

    self.load_ip_options()

  def load_ip_options(self):
    """Get ip of NIC used to create server"""
    # List of NIC
    self.nic_info = socket.gethostbyname_ex(socket.gethostname())
    # Set font used to text
    font = pygame.font.Font(path.join(path.dirname(__file__), "src", "bit5x3.ttf"), 40)
    # For each NIC, create text surface and append it to a list
    for ip_addr in self.nic_info[2]:
      text = font.render(ip_addr, False, WHITE)
      self.nic_info_text.append({'ip': ip_addr, 'text': text})

  def process_events(self):
    """Process pygame events"""
    pass

  def update(self, events, pressed_keys):
    """Update local variables"""
    self.mouse_pos = pygame.mouse.get_pos()

  def render_server_pick(self, surface):
    """Draw rectangle with list of servers"""
    x_offset = surface.get_width() * 55 // 100
    y_offset = surface.get_height() * 4 // 10
    rect_width = surface.get_width() * 40 // 100
    rect_height = surface.get_height() * 55 // 100
    border_thick = surface.get_width() // 100

    # Picker Borders
    pygame.draw.rect(surface, WHITE, pygame.Rect(x_offset, \
    y_offset, rect_width, rect_height), border_thick)

    # Middle Line
    pygame.draw.rect(surface, WHITE, pygame.Rect(surface.get_width()//2\
    -border_thick//2, y_offset, border_thick, rect_height))

    # Servers Title text
    surface.blit(self.servers_text, (x_offset, \
    y_offset - self.servers_text.get_height()))

  def render_options(self, surface):
    """Draw menu options"""
    x_offset = surface.get_width() * 5 // 100
    y_offset = surface.get_height() * 4 // 10
    rect_width = surface.get_width() * 40 // 100
    # rect_height = surface.get_height() * 55 // 100
    border_thick = surface.get_width() // 100

    # Play Title text
    play_x = x_offset + (rect_width-self.play_text.get_width())//2
    self.play_rect = surface.blit(self.play_text, (play_x, \
    y_offset))

    # Play Create Server
    create_server_y = y_offset + self.play_text.get_height()
    create_server_x = x_offset + (rect_width-self.create_server_text.get_width())//2
    self.create_server_rect = surface.blit(self.create_server_text, (create_server_x, \
    create_server_y))

    # NIC ips
    ## Rect
    nic_rect_x = x_offset
    nic_rect_y = self.create_server_text.get_height() + create_server_y + 10
    nic_rect_h = surface.get_height() * 95//100 - nic_rect_y
    pygame.draw.rect(surface, WHITE, pygame.Rect(nic_rect_x, \
    nic_rect_y, rect_width, nic_rect_h), border_thick)
    ## Ip Options
    ip_x_offset = x_offset + border_thick + 5
    ip_y_offset = nic_rect_y + border_thick + 5
    for elem in self.nic_info_text:
      elem['rect'] = surface.blit(elem['text'], (ip_x_offset, ip_y_offset))
      ip_y_offset += elem['text'].get_height()

  def render_mouse_hover(self, surface):
    """Mouse hover effects"""

    # Play Button
    radius = 10
    x_pos = self.play_rect.x - 20
    y_pos = self.play_rect.y + self.play_rect.height//2
    if self.play_rect.collidepoint(self.mouse_pos):
      pygame.draw.circle(surface, WHITE, (x_pos, y_pos), radius)

    # Create Server Button
    radius = 10
    x_pos = self.create_server_rect.x - 20
    y_pos = self.create_server_rect.y + self.create_server_rect.height//2
    if self.create_server_rect.collidepoint(self.mouse_pos):
      pygame.draw.circle(surface, WHITE, (x_pos, y_pos), radius)

  def render(self, surface):
    """Render components from scene"""

    #Render PONG title
    surface.blit(self.pong_text, \
    ((surface.get_width()-self.pong_text.get_width())//2, \
    surface.get_height() // 10))

    #Render Sections
    self.render_server_pick(surface)
    self.render_options(surface)

    # Render Hover Effects
    self.render_mouse_hover(surface)
