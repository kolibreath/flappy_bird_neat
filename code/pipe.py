import pygame

class Pipe:
    pipe_surface = pygame.image.load("./assets/pipe-green.png").convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)

    pipe_list = []
    pipe_height = [400, 600, 800]

    def create_pipe():
        random_pipe_pos = random.choice(pipe_height)
        bottom_pipe = pipe_surface.get_rect(midtop=(screen_width, random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom=(screen_width, random_pipe_pos - 300))
        return bottom_pipe, top_pipe
        
    def move_pipes(pipes):
        for pipe in pipes:
            #向左边移动
            pipe.centerx -= 5
        return pipes


    def draw_pipes(pipes):
        for pipe in pipes:
            # 生成朝上的管道
            if pipe.bottom >= screen_height:
                screen.blit(pipe_surface, pipe)
            else:
                #生成朝下的管道
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

