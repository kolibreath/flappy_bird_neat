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
              './assets/yellowbird-upflap.png']]
    
    def __init__(self, game, index):
        self.status = True # is status == True, this bird is alive
        index = random.choice(self.birds) # random different birds
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load(index[0]).convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load(index[1]).convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load(index[2]).convert_alpha())
        
        # which bird in the pop
        self.pop_index = index
        self.bird_fly_index = 0
        self.bird_movement = 0
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_surface = self.bird_frames[self.bird_fly_index]
        
        self.bird_rect = self.bird_surface.get_rect(center=(100, game.screen_height // 2))
        
        self.width = 0  
        self.height = 0
        
        self.fitness = 0
        self.game = game 
        
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
        new_surface = self.bird_frames[self.bird_fly_index]
        new_bird_rect = new_surface.get_rect(center=(100, self.bird_rect.centery))
        return new_surface, new_bird_rect

    # get two input params
    def get_inputs(self):
        result = self.middle_of_pipes(self.game.pipe_list)
        bird_x = self.bird_rect.topright[0]
        bird_y = self.bird_rect.topright[1]
        
        # when the game is just initialized, result may be -1
        if result == -1:
            return bird_x, bird_y
        
        pipe_x, pipe_y = result[0], result[1] 
        return pipe_x - bird_x, pipe_y - bird_y

    # fitness function
    def fitness(self, game):
        self.fitness = self.game.score
    
    # output the middle of two points


    def middle_of_pipes(self, pipe_list):
        # in the begining the pipes are not generated completely
        if len(pipe_list) == 0:
            return -1
        top, bottom = pipe_list[0][1], pipe_list[0][0]
        return (top.right ,((top.bottomright[1] + bottom.bottomright[1]) // 2))
