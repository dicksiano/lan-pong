"""Class of Menu Scene in Pong-Lan game"""
from os import path, getcwd
import pygame
from scene_base import SceneBase

WHITE = (255, 255, 255)

class PongMenu(SceneBase):
  """Menu Scene in Pong-Lan game."""
  def __init__(self):
    SceneBase.__init__(self)

    # PONG title
    font = pygame.font.Font(path.join(getcwd(), "src", "bit5x3.ttf"), 130)
    self.pong_text = font.render("PONG", False, WHITE)

    # Servers title
    font = pygame.font.Font(path.join(getcwd(), "src", "bit5x3.ttf"), 35)
    self.servers_text = font.render("SERVERS", False, WHITE)

    # Play Title
    font = pygame.font.Font(path.join(getcwd(), "src", "bit5x3.ttf"), 45)
    self.play_text = font.render("PLAY", False, WHITE)
    self.play_rect = None

    # Create Server Title
    font = pygame.font.Font(path.join(getcwd(), "src", "bit5x3.ttf"), 45)
    self.create_server_text = font.render("CREATE SERVER", False, WHITE)
    self.create_server_rect = None


  def process_events(self):
    pass

  def update(self):
    pass

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
    rect_height = surface.get_height() * 55 // 100
    border_thick = surface.get_width() // 100

    # Play Title text
    play_x = x_offset + (rect_width-self.play_text.get_width())//2
    self.play_rect = surface.blit(self.play_text, (play_x, \
    y_offset))

    # Play Create Server
    create_server_y = y_offset + self.play_text.get_height()
    create_server_x = x_offset + (rect_width-self.create_server_text.get_width())//2
    surface.blit(self.create_server_text, (create_server_x, \
    create_server_y))

  def render(self, surface):
    #Render PONG title
    surface.blit(self.pong_text, \
    ((surface.get_width()-self.pong_text.get_width())//2, \
    surface.get_height() // 10))

    #Render Sections
    self.render_server_pick(surface)
    self.render_options(surface)
