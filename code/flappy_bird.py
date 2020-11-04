import pygame, sys, random
from bird import Bird
from game import Game
import neat
import os

# generation
gen = 0

# remove pipes from list that get out of the screen
def remove_pipes(pipe_list):
    for pipe_rect in pipe_list:
        if pipe_rect[0].bottomright[0] < 0 or pipe_rect[1].bottomright[0] < 0:
            pipe_list.remove(pipe_rect)
 
def pipe_pos(pipe_list):
    # in the begining the pipes are not generated completely
    if len(pipe_list) == 0 : return (0,0)
    top, bottom = pipe_list[0][1], pipe_list[0][0]
    return (top.bottomleft[1],bottom.topleft[1]) 

# set up config 
def start(config_file, game):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    # create output in the terminal
    output = neat.Population(config)
    
    output.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    output.add_reporter(stats)
    
    # run(function, generation)
    winner = output.run(train, 50)
   
# train: in this function, the image will be draw on the scree with the output of nerual network
def train(genomes, config):
    global gen
    
    gen += 1
    birds = []
    nets = []
    ge = []
 
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(game))
        ge.append(genome)
    
     # Game Logic
    while True and len(birds) != 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:                  # quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:       # fly the bird a bit
                if game.game_start == False:
                    game.game_start = True

              

                # bird.jump()


            if event.type == game.SPAWNPIPE:

                if game.game_start:
                    game.pipe_list.append(game.create_pipe())
                    remove_pipes(game.pipe_list)

      
        game.screen.blit(game.bg_surface, (0, 0))  # draw background image
        if game.game_start == False:
            game.screen.blit(game.game_start_surface, game.game_start_rect)

        if game.game_active and game.game_start:
            # Pipes
            game.pipe_list = game.move_pipes(game.pipe_list)
            game.draw_pipes(game.pipe_list)

            # increment fitness to every bird
            for i, bird in enumerate(birds):
                
                ge[birds.index(bird)].fitness += 0.05
                # todo not rotated
                if bird.status:
                    bird.move_down_to(bird.bird_surface)
    
                # todo no rotate
                rotated_bird = bird.bird_surface  # set bird animation
                top_y, bottom_y = pipe_pos(game.pipe_list)
                output = nets[birds.index(bird)].activate((bird.bird_rect.topright[0],
                                                           (bird.bird_rect.y - top_y), ( bottom_y - bird.bird_rect.y)))
                

                if output[0] > 0.5:
                    bird.jump()
   
                bird.status = game.check_collision(game.pipe_list, bird)
                
            for bird in birds:
                if bird.status == False:
                    ge[birds.index(bird)].fitness -= -1
                    # print(f'fitness {ge[birds.index(bird)].fitness}')
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    bird.status = False 
                   
           

        # 计算分数
        game.score += 0.01
        game.score_display('main_game',gen)

        if game.game_active == False and game.game_start:
            if game.score > game.high_score:
                high_score = game.score
            game.screen.blit(game.game_over_surface, game.game_over_rect)
            game.score_display('game_over')

        # Floor
        game.draw_floor()

        pygame.display.update()
        game.clock.tick(120)
        
    # clear every pipe before quit
    game.pipe_list.clear()
    
    
# where the game begins
if __name__ == "__main__":
    
    game = Game()  # initialize Game instance
    game.start()  # set timer
    bird = Bird(game)  # initialize one bird
    
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, 'config_feedforward.txt')
   
    start(path, game) 
   
