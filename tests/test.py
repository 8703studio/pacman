import pygame


pygame.init()
def screen_lock
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

running = True
#(x, y, width, height)
rectangle = pygame.Rect(200, 150, 100, 50)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, 'red', rectangle)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()