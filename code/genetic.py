from bird import Bird
import pygame, torch
import torch.nn as nn
import random
import numpy as np

class Genetic :
  
    def __init__(self, game, pop_size, generation):
        self.game = game
        self.pop_size = pop_size
        self.generation = generation 
        self.pop_list = []
        
        self.F = 0.8
        self.CR = 0.5
        
    def init_pop(self):
        for i in range(self.pop_size):
            self.pop_list.append(Bird(self.game, i))
        return self.pop_list

    # genetic algorithm frame for one time
    def run_GA(self):
        for bird in self.pop_list:
            if bird.status == False:
                continue
            self.train(bird)
            
    # fitness function 
    def fitness(self, bird):
        return bird.fitness()

    
    # train one bird in one generation
    def train(self, bird):
        # iterate array
        width, height = bird.get_inputs()
        
        lr = 0.03
        net = bird.linreg
        loss = bird.squared_loss
        input = torch.tensor([width, height]).float()
        
        result = bird.middle_of_pipes(self.game.pipe_list)
        pipe_middle_y = result[1]
        if bird.bird_rect.centery > pipe_middle_y:
            y = (bird.bird_rect.centery - pipe_middle_y ) / (self.game.screen_height - pipe_middle_y - self.game.floor_height)
        else :
            y = 0

        output = net(input, bird.w1, bird.w2, bird.b1, bird.b2)
        
        # todo the flight of the bird is still not normal
        # print(f'output {output.data}')
        if output > 0.5 :
            self.notice(bird.pop_index)
          
        l = loss(output, torch.tensor(y).float())
        l.backward()
        bird.sgd([bird.w1, bird.w2, bird.b1, bird.b2], lr ,1)
        
        bird.w1.grad.data.zero_() 
        bird.w2.grad.data.zero_() 
        bird.b1.grad.data.zero_() 
        bird.b2.grad.data.zero_()
        
                             
    # check if all birds are dead and dead birds are not shown in the screen any longer
    def check_alive(self):
        alive_birds = []
        for index, bird in enumerate(self.pop_list):
            if bird.status:
                alive_birds.append((index, bird))
        return alive_birds

    # send event to notice a bird should fly up a bit
    def notice(self, bird_index):
        flyup = pygame.event.Event(pygame.USEREVENT + 2, index= bird_index)
        pygame.event.post(flyup)
   
    # reset the bird group
    def reset(self):
        for b in self.pop_list:
            b.bird_rect = b.bird_surface.get_rect(center=(100, self.game.screen_height // 2))
            b.movement = 0

    # if all birds are dead 
    def generate_new_birds(self):
        new_birds = []
        self.pop_list.sort(key=lambda bird : bird.fitness)
        best_birds = self.pop_list[0: int(self.pop_size * 0.5)]
        worse_birds = self.pop_list[int(self.pop_size * 0.5 ):]
        parent_num = len(best_birds)
        for i in range( self.pop_size):
            bird = Bird(self.game, i)
            parent_1 = random.choice(best_birds)
            parent_2 = random.choice(worse_birds)
            
            bird.w1 = torch.from_numpy(np.array([self.F]) * parent_1.w1.detach().numpy() 
                                       + np.array([1-self.F]) * (parent_2.w1.detach().numpy())).float()
            bird.w2 = torch.from_numpy(np.array([self.F]) * parent_1.w2.detach().numpy() 
                                       + np.array([1-self.F]) * (parent_2.w2.detach().numpy())).float()
            bird.b1 = torch.from_numpy(np.array([self.F]) * parent_1.b1.detach().numpy() 
                                       + np.array([1-self.F]) * (parent_2.b1.detach().numpy())).float()
            bird.b2 = torch.from_numpy(np.array([self.F]) * parent_1.b2.detach().numpy() 
                                       + np.array([1- self.F]) * (parent_2.b2.detach().numpy())).float()
            bird.init_params()
            new_birds.append(bird)
        
        self.pop_list.clear()
        self.pop_list = new_birds
    
                    
