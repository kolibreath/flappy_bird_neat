from bird import Bird
import pygame, torch

class Genetic :
  
    def __init__(self, game, pop_size, generation):
        self.game = game
        self.pop_size = pop_size
        self.generation = generation 
        
    def init_pop(self):
        self.pop_list = []
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

    # todo 
    # compute possbility 
    def compute(self, bird):
        return 0
    
    # train one bird in one generation
    def train(self, bird):
        # iterate array
        # todo how to train
        width, height = bird.get_inputs()
        
        lr = 0.03
        net = bird.linreg
        loss = bird.squared_loss
        input = torch.tensor([width, height]).float()
        
        # todo set y = 0.3
        # result = bird.middle_of_pipes(self.game.pipe_list)
        # y = [[result[0], result[1]]
        y = 0.3
        
        l = loss(net(input, bird.w1, bird.w2, bird.b1, bird.b2), torch.tensor(y).float())
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
