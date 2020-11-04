import pygame, sys, random
from bird import Bird
from game import Game

# remove pipes from list that get out of the screen
def remove_pipes(pipe_list):
    for pipe_rect in pipe_list:
        if pipe_rect[0].bottomright[0] < 0 or pipe_rect[1].bottomright[0] < 0:
            pipe_list.remove(pipe_rect)
 
# 计算两个柱子之间的终点
def middle_of_pipes(pipe_list):
    # in the begining the pipes are not generated completely
    if len(pipe_list) == 0 : return -1
    top, bottom = pipe_list[0][1], pipe_list[0][0]
    return (top.bottomright[1] + bottom.bottomright[1]) // 2
    
# where the game begins
if __name__ == "__main__":
    
    game = Game()  # initialize Game instance
    game.start()  # set timer
    bird = Bird(game)  # initialize one bird
    
    
    # Game Logic
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                  # quit the game
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:       # fly the bird a bit
                if game.game_start == False:
                    game.game_start = True

                bird.bird_index += 1
                bird.bird_index = bird.bird_index % len(bird.bird_frames)
                bird.bird_surface, bird.bird_rect = bird.bird_animation()
               
                bird.jump()
                
            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_active == False:
                
                game.game_active = True
                game.pipe_list.clear()
                
                bird.bird_rect.center = (100, game.screen_height // 2)
                bird.bird_y_incre = 0
                
                game.score = 0

            if event.type == game.SPAWNPIPE:
                
                if game.game_start:
                    game.pipe_list.append(game.create_pipe())
                    remove_pipes(game.pipe_list)
                    
            if event.type == game.BIRDFLAP:
                # bird.bird_index += 1
                # bird.bird_index = bird.bird_index % len(bird.bird_frames)
                # bird.bird_surface, bird.bird_rect = bird.bird_animation()
                bird.tick += 1
                # a = 
            
        

        game.screen.blit(game.bg_surface, (0, 0)) # draw background image 
        if game.game_start == False:
            game.screen.blit(game.game_start_surface, game.game_start_rect)

       
        if game.game_active and game.game_start:
    
            rotated_bird = bird.rotate_bird() # set bird animation
            bird.move_down_to(rotated_bird)
            
            # Pipes
            game.pipe_list = game.move_pipes(game.pipe_list)
            game.draw_pipes(game.pipe_list)

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
