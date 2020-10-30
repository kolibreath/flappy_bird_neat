import pygame, random
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
    birds = [["./assets/bluebird-downflap.png",
              './assets/bluebird-midflap.png', 
              './assets/bluebird-upflap.png'],
             ["./assets/redbird-downflap.png",
              './assets/redbird-midflap.png',
              './assets/redbird-upflap.png'], 
             ["./assets/yellowbird-downflap.png",
              './assets/yellowbird-midflap.png',
              './assets/yellowrd-upflap.png']]
    
    def __init__(self, game):
        self.status = True # is status == True, this bird is alive
        index = random.choice(birds) # random different birds
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load(index[0]).convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load(index[1]).convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load(index[2]).convert_alpha())
        
        self.bird_index = 0
        self.bird_movement = 0
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_index]
        
        self.bird_rect = self.bird_surface.get_rect(center=(100, game.screen_height // 2))
        
        self.width = 0  
        self.height = 0
        
        self.fitness = 0
        
        self.num_inputs, self.num_outputs = 2, 1
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

    # bird flap animation
    def bird_animation(self):
        new_surface = self.bird_frames[self.bird_index]
        new_bird_rect = new_surface.get_rect(center=(100, self.bird_rect.centery))
        return new_surface, new_bird_rect

    # todo 
    # get two input params
    def get_inputs(self):
        width, height = 0, 0
        return width, height

    # fitness function
    def fitness(self, game):
        self.fitness = game.score
    

    