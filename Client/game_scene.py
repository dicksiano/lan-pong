"""Class that handle the view"""
import pygame
from .constants import *
from .scene_base import SceneBase

class GameScene(SceneBase):
    """Menu Scene in Pong-Lan game."""
    def __init__(self):
        SceneBase.__init__(self)
    
    def draw(self, surface, paddle1_pos, paddle2_pos, ball_pos):
        pygame.draw.line(surface, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
        pygame.draw.line(surface, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(surface, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(surface, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

        # Paddles and Ball
        pygame.draw.circle(surface, RED, ball_pos, 20, 0)
        pygame.draw.polygon(surface, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
        pygame.draw.polygon(surface, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)