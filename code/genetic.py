from bird import Bird

class Genetic :
  
    def __init__(self, game):
        self.pop_size = 10
        
    def init_pop(self, game):
        self.pop_list = []
        for i in range(self.pop_size):
            self.pop_list.append(Bird(game))
        return pop_list

    # fitness function 
    def fitness(self, bird):
        return bird.fitness()

    # todo 
    # compute possbility 
    def compute(self, bird):
        return 0
    
    def train(self, generation ,game):
        pops = self.init_pop(game)
        for i in range(generation):
            # iterate array
            for (width_1, height_1, height_2, width_2, height_3, height_4) in pops[i].get_inputs():
                 width_1_c = width_1.clone().detach().float()
                 height_1_c = height_1.clone().detach().float()
                 height_2_c = height_2.clone().detach().float()
                 
                 width_2_c = width_2.clone().detach().float()
                 height_3_c = height_3.clone().detach().float()
                 height_4_c = height_4.clone().detach().float()
                 
                 output = pops[i].net(width_1_c, height_1_c, height_2_c, width_2_c, height_3_c, height_4_c)
                 
                 # 只需要一个参数？
                 l = pops[i].loss(output, compute(self, pops[i]))
                 
                 pops[i].optimizer.zero_grad()
                 l.backward()
                 pops[i].optimier.step()
                 
                 
             
