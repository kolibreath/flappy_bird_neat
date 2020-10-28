import pygame, sys, random
from bird import Bird
from pipe import Pipe
from game import Game
pygame.init()

# 游戏背景设置长宽高

screen = pygame.display.set_mode(( screen_width, screen_height))
clock = pygame.time.Clock()

# 字体
game_font = pygame.font.Font("./assets/04B_19__.TTF", 40)

# 加载背景图片比并且放大
bg_surface = pygame.image.load('./assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('./assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

floor_x_pos = 0

# 使用动画加载
bird_downflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-downflap.png').convert_alpha())
bird_midflap =  pygame.transform.scale2x(pygame.image.load('./assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('./assets/bluebird-upflap.png').convert_alpha())

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, screen_height // 2))

pipe_surface = pygame.image.load("./assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = []
# 各种不同的高度
pipe_height = [400, 600, 800]

# 自定义的事件
SPAWNPIPE = pygame.USEREVENT
BIRDFLAP = pygame.USEREVENT + 1

pygame.time.set_timer(BIRDFLAP, 200)
pygame.time.set_timer(SPAWNPIPE, 1200)

game_start_surface = pygame.transform.scale2x(pygame.image.load('./assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center=( screen_width // 2, screen_height // 2))

game_over_surface = pygame.transform.scale2x(pygame.image.load('./assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=( screen_width // 2, screen_height // 2))

game_start = False

# 124是下面floor的宽度
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, screen_height - 124))
    #控制移动 将另外一个floor放在左边
    screen.blit(floor_surface, (floor_x_pos + screen_width, screen_height - 124))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(screen_width, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_width, random_pipe_pos - 300))
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

# 检查碰撞柱子 检查碰撞边缘
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= screen_height - 124:
        return False

    return True

# 动画
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_surface = bird_frames[bird_index]
    new_bird_rect = new_surface.get_rect(center=(100, bird_rect.centery))
    return new_surface, new_bird_rect


# 显示字体
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {str(int(score))}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(score_surface, score_rect)

        high_surface = game_font.render(f'High score: {str(int(high_score))}', True, (255, 255, 255))
        high_rect = high_surface.get_rect(center=(screen_width // 2, screen_height-200))
        screen.blit(high_surface, high_rect)


# where the game begins
if __name__ == "__main__":
    
    game = new Game()  # initialize Game instance
    bird = new Bird()  # initialize one bird
    
    # Game Logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_start == False:
                    game.game_start = True

                bird.bird_movement = 0
                bird.bird_movement -= move_up

            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_active == False:
                game.game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height // 2)
                bird_movement = 0
                score = 0

            if event.type == SPAWNPIPE:
                if game_start:
                    pipe_list.extend(create_pipe())

            if event.type == BIRDFLAP:
                bird_index += 1
                bird_index = bird_index % len(bird_frames)
                bird_surface, bird_rect = bird_animation()

    # 先显示是否开始游戏
    screen.blit(bg_surface, (0, 0))
    if game_start == False:
        screen.blit(game_start_surface, game_start_rect)

    # 如果鸟没有碰撞（没有死亡）
    # game_active 表示是否还是有效的游戏 即 是否死亡
    if game_active and game_start:
        #Birds
        # 设置重力 小鸟会掉落
        rotated_bird = rotate_bird(bird_surface)
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)

        # 计算分数
        score += 0.01
        score_display('main_game')

    if game_active == False and game_start:
        if score > high_score:
            high_score = score
        screen.blit(game_over_surface, game_over_rect)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    screen.blit(floor_surface, (floor_x_pos, screen_height - 124))

    draw_floor()
    if floor_x_pos <= - screen_width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
