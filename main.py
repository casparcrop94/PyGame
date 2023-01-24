import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25)

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -25
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump 
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        self.obstacle_speed = 4
        self.frame_index = 0
        self.frames = []

        if type == 'snail':
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300

        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.obstacle_speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: self.kill()


def display_score():
    current_time = round(
        ((pygame.time.get_ticks() - start_time) / 1000)
    )
    score_surf = test_font.render('Score: '+str(current_time), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_spr():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

# Start Pygame config
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

# BGM
bgm_sound = pygame.mixer.Sound('audio/music.wav')
bgm_sound.set_volume(0.5)
bgm_sound.play(loops= -1)

# Declare variables for later use
game_is_active = False
start_time = 0
score = 0
obstacle_speed = 4

# Player Sprite Group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle Group
obstacle_group = pygame.sprite.Group()

# Intro screen player
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_is_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('Restarting...')
                game_is_active = True
                obstacle_speed = 5
                start_time = pygame.time.get_ticks()
                bgm_sound.play(loops= -1)
                
    if game_is_active:
        # Active Game Screen
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf, (0,300))

        # Player
        player.draw(screen)
        player.update()

        #Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Score
        score = display_score()

        # Collision
        game_is_active = collision_spr()

    else:
        bgm_sound.stop()
        # Intro / Game Over Screen
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        
        #Title
        title_surf = test_font.render('Runner Game', False, (64,64,64))
        title_rect = title_surf.get_rect(center = (400, 50))
        screen.blit(title_surf, title_rect)

        # Activating prompt
        prompt_surf = test_font.render('Press [Space] to start running!', False, (64,64,64))
        prompt_rect = prompt_surf.get_rect(center = (400, 350))
        screen.blit(prompt_surf, prompt_rect)

        #Show last score when applicable
        last_score_surf = test_font.render('Last Score: '+str(score), False, (64,64,64))
        last_score_rect = last_score_surf.get_rect(center = (400, 90))
        if score != 0: screen.blit(last_score_surf, last_score_rect)

    #Draw all elements and update everything
    pygame.display.update()
    clock.tick(60)