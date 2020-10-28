import pygame
class Bird:
    bird_downflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-downflap.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-upflap.png').convert_alpha())
    
    def __init__(self, screen):
        self.bird_index = 0
        bird_movement = 0
        self.bird_frame = [bird_downflap, bird_midflap, bird_upflap]
        self.bird_surface = bird_frame[bird_index]
        self.bird_rect = bird_surface.get_rect(center=(100, scree.screen_height // 2))
        self.width = 0  
        self.height = 0
    