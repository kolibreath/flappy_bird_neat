import pygame
import torch
import numpy as np
from torch import nn
from torch.nn import init


class FlattenLayer(torch.nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):  # x shape: (batch, *, *, ...)
        return x.view(x.shape[0], -1)

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
        
        self.distance = 0
        
        self.num_inputs, self.num_outputs = 6, 1
        self.num_hiddens = 10
        
        self.net = nn.Sequential(
            FlattenLayer(),
            nn.Linear(self.num_inputs, self.num_hiddens),
            nn.ReLU(),
            nn.Linear(self.num_hiddens, self.num_outputs)
        )
        
        for param in self.net.parameters():
            init.normal_(param, mean=0, std=0.01)
        
        self.optimizer = torch.optim.SGD(self.net.parameters(), lr = 0.5)
        self.loss = torch.nn.CrossEntropyLoss()
    
        
    # member functions
    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, - self.bird_movement * 3, 1)
        return new_bird


    def bird_animation(self):
        new_surface = self.bird_frames[self.bird_index]
        new_bird_rect = new_surface.get_rect(center=(100, self.bird_rect.centery))
        return new_surface, new_bird_rect

    # todo 
    # get six input params
    def get_inputs(self):
        width_1 = 0
        height_1= 0 
        height_2= 0 
        width_2 = 0
        height_3= 0
        height_4= 0
        
        return width_1, height_1, height_2, width_2, height_3, height_4

    # todo 
    # fitness function
    def distance(self):
        return self.distance