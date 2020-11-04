import pygame
import random
class Game:
    '''
    1. initiliaze necessary elements and font
    2. initiliaze surfaces (background game_start game_over floor pipes)
    3. control floor movement
    4. set timer for user event
    '''
  
    def __init__(self):
        pygame.init()
        
        self.screen_width = 576
        self.screen_height = 924
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.gravity = 0.25
        self.bird_movement = 0
       
        self.move_up = 8
        self.game_active = True
        self.score = 0
        self.high_score = 0

        self.game_start = False

        self.floor_x_pos = 0

        self.game_start = False

        self.pop = []    # bird population
        self.pipe_list = []  # pipes 

        self.SPAWNPIPE = pygame.USEREVENT
        self.BIRDFLAP = pygame.USEREVENT + 1
        
        self.floor_height = 124

        self.pipe_surface = pygame.image.load("./assets/pipe-green.png").convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)

        self.pipe_vel = 5

        self.pipe_height = [400, 600, 800]

        self.font = pygame.font.Font("./assets/04B_19__.TTF", 40)

        self.bg_surface = pygame.image.load('./assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)

        self.floor_surface = pygame.image.load('./assets/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)

        self.game_start_surface = pygame.transform.scale2x(
            pygame.image.load('./assets/message.png').convert_alpha())

        self.game_start_rect = self.game_start_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2))

        self.game_over_surface = pygame.transform.scale2x(
            pygame.image.load('./assets/gameover.png').convert_alpha())

        self.game_over_rect = self.game_over_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2))

        
    # member functions 
    def start(self):
        # pygame.time.set_timer(self.BIRDFLAP, 100)
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
      

    def draw_floor(self):
        self.floor_x_pos -= 1
        self.screen.blit(self.floor_surface, (self.floor_x_pos,
                                              self.screen_height - self.floor_height))
        self.screen.blit(self.floor_surface, (self.floor_x_pos,
                                         self.screen_height - self.floor_height))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + self.screen_width, self.screen_height - self.floor_height))

        if self.floor_x_pos <= - self.screen_width: # reset the floor tile
            self.floor_x_pos = 0

    def check_collision(self, pipes, bird):
        for pipe in pipes:
            if bird.bird_rect.colliderect(pipe[0]) or bird.bird_rect.colliderect(pipe[1]):
                return False

        if bird.bird_rect.top <= -100 or bird.bird_rect.bottom >= self.screen_height - self.floor_height:
            return False

        return True
    
    def score_display(self, game_state):
        if game_state == 'main_game':
            score_surface = self.font.render(
                str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = self.font.render(f'Score: {str(int(self.score))}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.screen_width // 2, 100))
            self.screen.blit(score_surface, score_rect)

            high_surface = self.font.render(f'High score: {str(int(self.high_score))}', True, (255, 255, 255))
            high_rect = high_surface.get_rect(center=(self.screen_width // 2, self.screen_height-200))
            self.screen.blit(high_surface, high_rect)

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(self.screen_width, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(self.screen_width, random_pipe_pos - 300))
        return (bottom_pipe, top_pipe)

    def move_pipes(self, pipes):
        for pipe in pipes:
            #向左边移动
            pipe[0].centerx -= self.pipe_vel
            pipe[1].centerx -= self.pipe_vel
        return pipes


    def draw_pipes(self, pipes):
        for pipe in pipes:
            # 生成朝上的管道
            # if pipe.bottom >= self.screen_height:
            #     self.screen.blit(self.pipe_surface, pipe)
            # else:
            #     #生成朝下的管道
            #     flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
            #     self.screen.blit(flip_pipe, pipe)
            self.screen.blit(self.pipe_surface, pipe[0])
            flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
            self.screen.blit(flip_pipe, pipe[1])
