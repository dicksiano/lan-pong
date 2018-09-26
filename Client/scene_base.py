"""Base class for scenes"""
class SceneBase:
  """Base class for scenes"""
  def __init__(self):
    pass

  def process_input(self, events, pressed_keys):
    """Process inputs"""
    print("uh-oh, you didn't override this in the child class")

  def update(self):
    """Update"""
    print("uh-oh, you didn't override this in the child class")

  def render(self, screen):
    """Render"""
    print("uh-oh, you didn't override this in the child class")
