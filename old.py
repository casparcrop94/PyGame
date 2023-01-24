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

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

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

# def obstacle_movement(obstacle_list, obstacle_speed):
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= obstacle_speed
#             # if snail_rect.right <= 0: snail_rect.left = 800
#             if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
#             else: screen.blit(fly_surf, obstacle_rect)
#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
#         return obstacle_list
#     else: return []

# def player_animation():
#     global player_surf, player_index

#     if player_rect.bottom < 300:
#         player_surf = player_jump 
#     else:
#         player_index += 0.1
#         if player_index >= len(player_walk): player_index = 0
#         player_surf = player_walk[int(player_index)]

def display_score():
    current_time = round(
        ((pygame.time.get_ticks() - start_time) / 1000)
    )
    score_surf = test_font.render('Score: '+str(current_time), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collissions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect): return False
    return True

# Start Pygame config
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

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

# # Snail
# snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_frame_1,snail_frame_2]
# snail_frame_index = 0
# snail_surf = snail_frames[snail_frame_index]

# # Fly
# fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
# fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
# fly_frames = [fly_frame_1,fly_frame_2]
# fly_frame_index = 0
# fly_surf = fly_frames[fly_frame_index]

# Obstacles
obstacle_rect_list = []

# Player
# player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1,player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

# player_surf = player_walk[player_index]
# player_rect = player_surf.get_rect(midbottom = (80,300))
# player_gravity = 0

# Intro screen player
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale(player_stand,(100,200))
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500)

# fly_animation_timer =  pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_is_active:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
            #         player_gravity -= 25

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
            #             player_gravity -= 25
            
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail', 'snail', 'snail'])))
                # if randint(0,2):
                #     # obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                #     obstacle_group.add(Obstacle('snail'))
                # else:
                #     # obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))
                #     obstacle_group.add(Obstacle('fly'))
            
            # if event.type == snail_animation_timer:
            #     if snail_frame_index == 0: snail_frame_index = 1
            #     else: snail_frame_index = 0
            #     snail_surf = snail_frames[snail_frame_index]
            # if event.type == fly_animation_timer:
            #     if fly_frame_index == 0: fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surf = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('Restarting...')
                game_is_active = True
                # player_rect.right = 100
                obstacle_speed = 5
                start_time = pygame.time.get_ticks()
                

        # if event.type == pygame.KEYUP:
        #     print('key up')

    if game_is_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf, (0,300))

        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('Jump!')

        # line_tlbr = pygame.draw.line(screen, 'Red', (0,0),(800,400),3)
        # line_bltr = pygame.draw.line(screen, 'Red', (0,400),(800,0),3)
        # screen.blit(screen, line_tlbr)
        # screen.blit(screen, line_bltr)
        # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))

        # screen.blit(snail_surf, snail_rect)
        # if snail_speed == 0:
        #     snail_speed = 3 
        # else:
        #     snail_rect.x -= snail_speed
        # if snail_rect.right <= 0: snail_rect.left = 800

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # # player_rect.left += 2
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        #     player_gravity = 0
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        #Obstacle Movement
        # obstacle_movement(obstacle_rect_list,obstacle_speed)

        obstacle_group.draw(screen)
        obstacle_group.update()

        # if player_rect.colliderect(snail_rect):
        #     print('Collission')
        # else:
        #     print('Free to run')

        # if player_rect.left >= 800:
        #     player_rect.right = 50
        #     obstacle_speed += 1

        # mouse_pos = pygame.mouse.get_pos()

        score = display_score()

        # Collision
        # if snail_rect.colliderect(player_rect):
        #     game_is_active = False
        #     start_time = pygame.time.get_ticks()
        # game_is_active = collissions(player_rect, obstacle_rect_list)
        
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        obstacle_rect_list.clear()
        # player_rect.midbottom = (80,300)
        player_gravity = 0
        
        title_surf = test_font.render('Runner Game', False, (64,64,64))
        title_rect = title_surf.get_rect(center = (400, 50))
        screen.blit(title_surf, title_rect)

        prompt_surf = test_font.render('Press [Space] to start running!', False, (64,64,64))
        prompt_rect = prompt_surf.get_rect(center = (400, 350))
        screen.blit(prompt_surf, prompt_rect)

        last_score_surf = test_font.render('Last Score: '+str(score), False, (64,64,64))
        last_score_rect = last_score_surf.get_rect(center = (400, 90))
        if score != 0: screen.blit(last_score_surf, last_score_rect)


    #Draw all elements and update everything
    pygame.display.update()
    clock.tick(60)