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
        self.vel = -15
        
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
        self.bird_index += 1
        self.bird_index = self.bird_index % len(self.bird_frames)
        self.bird_surface, self.bird_rect = self.bird_animation()
        
        
    # bird moving downward to a destination
    def move_down_to(self, rotated_bird):
        self.tick += 1
        d = self.vel * self.tick + 1.5*(self.tick)**2
    
        if d < 0:
            d -=  2
        if d < -10:
            d = -10
            
        if d >= 16:
            d = (d / abs(d)) * 16
        
        self.bird_rect.centery += d
        self.game.screen.blit(rotated_bird, self.bird_rect)
       
            
        

