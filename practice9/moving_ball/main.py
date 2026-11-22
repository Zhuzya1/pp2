import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 800, 600
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()

    ball = Ball(screen, WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -ball.STEP)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, ball.STEP)
                elif event.key == pygame.K_LEFT:
                    ball.move(-ball.STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(ball.STEP, 0)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((255, 255, 255))
        ball.draw()

        # hint text
        font = pygame.font.SysFont("arial", 16)
        hint = font.render("Arrow keys to move. ESC to quit.", True, (120, 120, 120))
        screen.blit(hint, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()