import pygame
class Game:
    SPAWNPIPE = pygame.USEREVENT
    BIRDFLAP = pygame.USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.gravity = 0.25
        self.bird_movement = 0
        self.screen_width = 576
        self.screen_height = 924
        self.move_up = 12
        self.game_active = True
        self.score = 0
        self.high_score = 0

        self.game_start = False

        self.floor_x_pos = 0

        # 创建字体
        self.font = pygame.font.Font("./assets/04B_19__.TTF", 40)

        self.bg_surface = pygame.image.load('./assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale2x(bg_surface)

        self.floor_surface = pygame.image.load('./assets/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(floor_surface)

        self.game_start_surface = pygame.transform.scale2x(
            pygame.image.load('./assets/message.png').convert_alpha())


        self.game_start_rect = game_start_surface.get_rect(
        center=(screen_width // 2, screen_height // 2))

        self.game_over_surface = pygame.transform.scale2x(
    pygame.image.load('./assets/gameover.png').convert_alpha())
       
        self.game_over_rect = game_over_surface.get_rect(
    center=(screen_width // 2, screen_height // 2))

        self.game_start = False


        # 开始游戏 实例化Game
        def start(self):
            pygame.init()
            pygame.time.set_timer(BIRDFLAP, 200)
            pygame.time.set_timer(SPAWNPIPE,1200
