from bird import Bird
import pygame

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
        width =  width.clone().detach().float()
        height = height.clone().detach().float()
        
        # todo test if output is a double between [0, 1]    
        output = bird.net(width, height)
        print(output)
        if output > 0.5:
            notice(bird_index)
                 
        l = bird.loss(output, compute(self, bird))
                 
        bird.optimizer.zero_grad()
        l.backward()
        bird.optimier.step()
                             
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
