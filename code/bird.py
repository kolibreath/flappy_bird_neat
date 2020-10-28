import pygame
class Bird:

    
    def __init__(self, game):
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-upflap.png').convert_alpha())
        
        self.bird_index = 0
        self.bird_movement = 0
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, game.screen_height // 2))
        self.width = 0  
        self.height = 0
        
    
    # member functions

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, - self.bird_movement * 3, 1)
        return new_bird


    def bird_animation(self):
        new_surface = self.bird_frames[self.bird_index]
        new_bird_rect = new_surface.get_rect(center=(100, self.bird_rect.centery))
        return new_surface, new_bird_rect

    
