"""Pong game Engine Class"""
import random
from math import floor
from .constants import HEIGHT, WIDTH, HALF_PAD_HEIGHT, HALF_PAD_WIDTH,\
BALL_RADIUS, PAD_WIDTH, PAD_VEL

class Engine:
  """Pong Game Engine"""
  def __init__(self):
    self.paddle1_pos = [HALF_PAD_WIDTH - 1, int(HEIGHT/2)]
    self.paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH, int(HEIGHT/2)]
    self.l_score = 0
    self.r_score = 0
    self.paddle1_vel = 0
    self.paddle2_vel = 0
    if random.randrange(0, 2) == 0:
      self.ball_init(True)
    else:
      self.ball_init(False)

  def ball_init(self, right):
    """Init ball on field, right argument tells\
    the initial ball direction"""
    self.ball_pos = [int(WIDTH//2), int(HEIGHT//2)]
    horz = random.randrange(1, 2)
    vert = random.randrange(1, 2)

    if not right:
      horz = - horz

    self.ball_vel = [horz, -vert]

  def update(self):
    """Update game state"""
    if self.paddle1_pos[1] > HALF_PAD_HEIGHT and self.paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
      self.paddle1_pos[1] += self.paddle1_vel
    elif self.paddle1_pos[1] <= HALF_PAD_HEIGHT and self.paddle1_vel > 0:
      self.paddle1_pos[1] += self.paddle1_vel
    elif self.paddle1_pos[1] >= HEIGHT - HALF_PAD_HEIGHT and self.paddle1_vel < 0:
      self.paddle1_pos[1] += self.paddle1_vel

    if self.paddle2_pos[1] > HALF_PAD_HEIGHT and self.paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
      self.paddle2_pos[1] += self.paddle2_vel
    elif self.paddle2_pos[1] <= HALF_PAD_HEIGHT and self.paddle2_vel > 0:
      self.paddle2_pos[1] += self.paddle2_vel
    elif self.paddle2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT and self.paddle2_vel < 0:
      self.paddle2_pos[1] += self.paddle2_vel

    self.ball_pos[0] += int(self.ball_vel[0])
    self.ball_pos[1] += int(self.ball_vel[1])

    if int(self.ball_pos[1]) <= BALL_RADIUS:
      self.ball_vel[1] = - self.ball_vel[1]
    if int(self.ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
      self.ball_vel[1] = -self.ball_vel[1]

    if int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(self.ball_pos[1]) in \
    range(self.paddle1_pos[1] - HALF_PAD_HEIGHT, self.paddle1_pos[1] + HALF_PAD_HEIGHT, 1):
      self.ball_vel[0] = -self.ball_vel[0]
      self.ball_vel[0] = floor(self.ball_vel[0] * 1.1)
      self.ball_vel[1] = floor(self.ball_vel[1] * 1.1)
    elif int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
      self.r_score += 1
      self.ball_init(True)

    if int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(self.ball_pos[1]) in\
    range(self.paddle2_pos[1] - HALF_PAD_HEIGHT, self.paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
      self.ball_vel[0] = -self.ball_vel[0]
      self.ball_vel[0] *= 1
      self.ball_vel[1] *= 1
    elif int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
      self.l_score += 1
      self.ball_init(False)

  def keydown(self, event, player):
    """Handle keydown event"""
    print("ARROLA")
    if player == 0:
      if event == "K_UP":
        self.paddle1_vel = -PAD_VEL
      elif event == "K_DOWN":
        self.paddle1_vel = PAD_VEL
    else:
      if event == "K_UP":
        self.paddle2_vel = -PAD_VEL
      elif event == "K_DOWN":
        self.paddle2_vel = PAD_VEL


  def keyup(self, player):
    """Handle key up event"""
    if player == 0:
      self.paddle1_vel = 0
    else:
      self.paddle2_vel = 0

  def get_state(self):
    """Return game state"""
    return [self.paddle1_pos, self.paddle2_pos, self.ball_pos, self.l_score, self.r_score]
