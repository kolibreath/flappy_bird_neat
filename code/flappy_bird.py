import pygame, sys, random
from bird import Bird
from game import Game
from genetic import Genetic

def handle_events(game, genetic, birds):
    for event in pygame.event.get():
           if event.type == pygame.QUIT:                  # quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:       # fly the bird a bit
                if game.game_start == False:
                    game.game_start = True

            # flyup event
            if event.type == pygame.USEREVENT + 2:
                index = event.index
                birds[index].bird_movement = 0
                birds[index].bird_movement -= game.move_up

            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_active == False:

                game.game_active = True
                game.pipe_list.clear()

                genetic.reset()

                game.score = 0

            if event.type == game.SPAWNPIPE:
                if game.game_start:
                    game.pipe_list.extend(game.create_pipe())

            # birds flap animation
            if event.type == game.BIRDFLAP:
                # random choose some of the birds to display the animation
                indices = random.shuffle(range(genetic.pop_size))
                for i in range(genetic.pop_size // 2):
                    bird = birds[i]
                    bird.bird_index += 1
                    bird.bird_index = bird.bird_index % len(bird.bird_frames)
                    bird.bird_surface, bird.bird_rect = bird.bird_animation()

# bird rotate animation
def bird_rotate(game,birds):
    for bird in birds:
        rotated_bird = bird.rotate_bird(bird.bird_surface) # set bird animation
        bird.bird_movement += game.gravity                 # bird falling
        bird.bird_rect.centery += int(bird.bird_movement) 
        game.screen.blit(rotated_bird, bird.bird_rect)
# spwan pipes
def spwan_pipes(game):
    game.pipe_list = game.move_pipes(game.pipe_list)
    game.draw_pipes(game.pipe_list)
  
# where the game begins
if __name__ == "__main__":
    
    game = Game()  # initialize Game instance
    game.start()  # set timer
    # bird = Bird(game)  # initialize one bird
    
    genetic = Genetic(game, pop_size= 10 , generation= 30)
    birds = genetic.init_pop()
    
    # Game Logic
    while True:
        game.screen.blit(game.bg_surface, (0, 0)) # draw background image 
        # todo 这句话放到这里应该也没有晚问题吧？
        
        if game.game_start == False:
            game.screen.blit(game.game_start_surface, game.game_start_rect)
            
        # event loop
        handle_events(game, genetic, birds)

        # while the birds don't die out
        if game.game_active and game.game_start:
            bird_rotate(game, birds)
            spwan_pipes(game)
        
            game.game_active = game.check_collision(game.pipe_list, bird)

            # 计算分数
            game.score += 0.01
            game.score_display('main_game')

        if game.game_active == False and game.game_start:
            if game.score > game.high_score:
                high_score = game.score
            game.screen.blit(game.game_over_surface, game.game_over_rect)
            game.score_display('game_over')

        # Floor
        game.draw_floor()
        
        pygame.display.update()
        game.clock.tick(120)
