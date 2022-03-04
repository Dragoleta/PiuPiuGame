import pygame
import sys

screen = pygame.display.set_mode((600, 600))
color = (255, 255, 0)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

    screen.fill('white')
    pygame.display.flip()
    main()


if __name__ == '__main__':
    main()
