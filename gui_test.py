import pygame
import sys


def main(argv: list[str]):
    if len(argv) != 3:
        print('Invalid arguments')
        print('Usage: python3 gui_test.py <scale_x> <scale_y>')
        return

    scale = (int(argv[1]), int(argv[2]))

    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    screen.fill((50, 50, 50))
    for y in range(scale[1]):
        for x in range(scale[0]):
            print(x, y)
            x1 = (1200 / scale[0]) * x + 1200 / (scale[0] * 2)
            y1 = (800 / scale[1]) * y + 800 / (scale[1] * 2)
            pygame.draw.circle(screen, (255, 125, 0), (x1, y1), 15)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()

if __name__ == '__main__':
    main(sys.argv)