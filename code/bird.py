import pygame
import numpy as np



class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    
    def __init__(self, game):
        self.game = game
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-upflap.png').convert_alpha())
        
        self.bird_index = 0
        self.bird_y_incre = 0
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, game.screen_height // 2))
        self.width = 0  
        self.height = 0
    
        
        self.tick = 0 # jump once the tick set to zero
        
        self.tilt = 0 # the degree of tilt 
        self.vel = -10.5
        
        self.status = True
   
    # member functions
    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird_surface, self.tilt, 1)
        return new_bird

    # todo smooth the animation
    def bird_animation(self):
        new_surface = self.bird_frames[self.bird_index]
        new_bird_rect = new_surface.get_rect(center=(100, self.bird_rect.centery))
        return new_surface, new_bird_rect
    
    # bird jumping up
    def jump(self):
        self.tick = 0
        
        
    # bird moving downward to a destination
    def move_down_to(self, rotated_bird):
        
        if self.status == False:
            return 
        tick = self.tick
        d = self.vel * tick  + 0.5*(3)*(tick)**2
      
        if d <= 0:
            d =  -1
        
        if d >= 16:
            d = (d / abs(d)) * 16
        
        self.bird_rect.centery += d
        # print(f'(tick = ) {tick} ( -self.game.pipe_vel )* tick { (- self.game.pipe_vel )* tick} 1.5 * (tick ** 2) {1.5 * (tick ** 2)}')
        # print(d)
       
        # if d < 0 or self.bird_rect.centery < self.bird_rect.centery + 10:
        #     if self.tilt <  self.MAX_ROTATION:
        #        self.tilt = self.MAX_ROTATION
        # else:
        #     if self.tilt > -90:
        #         self.tilt -= self.ROT_VEL
        
        self.game.screen.blit(rotated_bird, self.bird_rect)
       
            
        

