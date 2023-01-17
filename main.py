import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()
text_surface = test_font.render('My Game', False, 'Black')

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (750,300))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            if player_rect.collidepoint(event.pos):
                print('Collission!')

        if event.type == pygame.MOUSEBUTTONUP:
            print('Mouse Up!')

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (300,50))

    screen.blit(snail_surf, snail_rect)
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800

    player_rect.left += 2
    screen.blit(player_surf, player_rect)

    # if player_rect.colliderect(snail_rect):
    #     print('Collission')
    # else:
    #     print('Free to run')

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print('Collision!')
        print(pygame.mouse.get_pressed())

    #Draw all elements and update everything
    pygame.display.update()
    clock.tick(60)