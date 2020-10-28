import pygame, sys, random
from bird import Bird
from game import Game


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

                bird.bird_movement = 0
                bird.bird_movement -= game.move_up

            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_active == False:
                
                game.game_active = True
                game.pipe_list.clear()
                
                bird.bird_rect.center = (100, game.screen_height // 2)
                bird.bird_movement = 0
                
                game.score = 0

            if event.type == game.SPAWNPIPE:
                if game.game_start:
                    game.pipe_list.extend(game.create_pipe())

            if event.type == game.BIRDFLAP:
                bird.bird_index += 1
                bird.bird_index = bird.bird_index % len(bird.bird_frames)
                bird.bird_surface, bird.bird_rect = bird.bird_animation()

        game.screen.blit(game.bg_surface, (0, 0)) # draw background image 
        if game.game_start == False:
            game.screen.blit(game.game_start_surface, game.game_start_rect)

       
        if game.game_active and game.game_start:
    
            rotated_bird = bird.rotate_bird(bird.bird_surface) # set bird animation
            bird.bird_movement += game.gravity                 # bird falling
            bird.bird_rect.centery += int(bird.bird_movement) 
            game.screen.blit(rotated_bird, bird.bird_rect)

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
