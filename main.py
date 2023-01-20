import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/Ground.png').convert()

score_surf = test_font.render('My Game', False, (64,64,64))
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (750,300))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

player_gravity = 0



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('Collission!')

        # if event.type == pygame.MOUSEBUTTONUP:
        #     print('Mouse Up!')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                print('Collision!')
                player_gravity -= 20

        if event.type == pygame.KEYDOWN:
            print('key down')
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    print('Jump!')
                    player_gravity -= 20
        # if event.type == pygame.KEYUP:
        #     print('key up')


    screen.blit(sky_surf,(0,0))
    screen.blit(ground_surf, (0,300))

    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
    screen.blit(score_surf, score_rect)

    # keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_SPACE]:
    #     print('Jump!')



    # line_tlbr = pygame.draw.line(screen, 'Red', (0,0),(800,400),3)
    # line_bltr = pygame.draw.line(screen, 'Red', (0,400),(800,0),3)
    # screen.blit(screen, line_tlbr)
    # screen.blit(screen, line_bltr)
    # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))


    screen.blit(snail_surf, snail_rect)
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800

    # Player
    player_gravity += 1
    player_rect.y += player_gravity
    player_rect.left += 2
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
        player_gravity = 0
    screen.blit(player_surf, player_rect)

    # if player_rect.colliderect(snail_rect):
    #     print('Collission')
    # else:
    #     print('Free to run')

    if player_rect.left >= 800: player_rect.right = 50

    # mouse_pos = pygame.mouse.get_pos()

    #Draw all elements and update everything
    pygame.display.update()
    clock.tick(60)