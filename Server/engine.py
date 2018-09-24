import random

import sys
sys.path.append('../')
import constants

class Engine:
    def __init__(self):
        self.self.paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT/2]
        self.self.paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT/2]
        self.self.l_score = 0
        self.self.r_score = 0
        if random.randrange(0,2) == 0:
            ball_init(True)
        else:
            ball_init(False)

    def ball_init(self,right):
        self.self.ball_pos = [WIDTH//2,HEIGHT//2]
        horz = random.randrange(1,2) 
        vert = random.randrange(1,2) 
        
        if right == False:
            horz = - horz
            
        self.self.ball_vel = [horz,-vert]

    def update(self):
        if self.paddle1_pos[1] > HALF_PAD_HEIGHT and self.paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == HALF_PAD_HEIGHT and self.paddle1_vel > 0:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self.paddle1_vel < 0:
            self.paddle1_pos[1] += self.paddle1_vel
        
        if self.paddle2_pos[1] > HALF_PAD_HEIGHT and self.paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == HALF_PAD_HEIGHT and self.paddle2_vel > 0:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self.paddle2_vel < 0:
            self.paddle2_pos[1] += self.paddle2_vel

        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        if int(self.ball_pos[1]) <= BALL_RADIUS:
            self.ball_vel[1] = - self.ball_vel[1]
        if int(self.ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            self.ball_vel[1] = -self.ball_vel[1]
        
        if int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(self.ball_pos[1]) in range(self.paddle1_pos[1] - HALF_PAD_HEIGHT,self.paddle1_pos[1] + HALF_PAD_HEIGHT,1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            self.r_score += 1
            ball_init(True)
            
        if int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(self.ball_pos[1]) in range(self.paddle2_pos[1] - HALF_PAD_HEIGHT,self.paddle2_pos[1] + HALF_PAD_HEIGHT,1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.0
            self.ball_vel[1] *= 1.0
        elif int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            self.l_score += 1
            ball_init(False)
        
    def keydown(event):        
        if event.key == K_UP:
            self.paddle2_vel = -PAD_VEL
        elif event.key == K_DOWN:
            self.paddle2_vel = PAD_VEL
        elif event.key == K_w:
            self.paddle1_vel = -PAD_VEL
        elif event.key == K_s:
            self.paddle1_vel = PAD_VEL

    def keyup(event):
        if event.key in (K_w, K_s):
            self.paddle1_vel = 0
        elif event.key in (K_UP, K_DOWN):
            self.paddle2_vel = 0

    def get_state():
        return [self.paddle1_pos, self.paddle2_pos, self.ball_pos, self.l_score, self.r_score]        