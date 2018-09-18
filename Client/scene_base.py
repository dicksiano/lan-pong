"""Module to SceneBase"""
class SceneBase:
  """Parent class of all scenes in Pong-Lan"""
  def __init__(self):
    pass

  def process_events(self):
    """Process events captured in screen"""
    print("Error: child class didn't override")

  def update(self):
    """Updates scenes states"""
    print("Error: child class didn't override")

  def render(self, surface):
    """Render scene in screen (pygame.display)"""
    print("Error: child class didn't override")
