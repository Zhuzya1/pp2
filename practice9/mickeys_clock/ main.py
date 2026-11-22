import pygame
import sys
import os
from clock import MickeyClock

WIDTH, HEIGHT = 600, 600
FPS = 30

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()

    # Load hands (fallback: draw simple rectangles if images missing)
    base = os.path.dirname(__file__)
    right_path = os.path.join(base, "images", "right_hand.png")
    left_path = os.path.join(base, "images", "left_hand.png")

    try:
        right_img = pygame.image.load(right_path).convert_alpha()
        left_img = pygame.image.load(left_path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        # Fallback: simple colored lines as surfaces
        right_img = pygame.Surface((10, 120), pygame.SRCALPHA)
        pygame.draw.rect(right_img, (0, 0, 0), (4, 0, 2, 120))
        left_img = pygame.Surface((10, 90), pygame.SRCALPHA)
        pygame.draw.rect(left_img, (200, 0, 0), (4, 0, 2, 90))

    center = (WIDTH // 2, HEIGHT // 2 - 50)
    mickey = MickeyClock(screen, center, right_img, left_img)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((240, 230, 200))
        # Draw clock face
        pygame.draw.circle(screen, (255, 255, 255), center, 200)
        pygame.draw.circle(screen, (0, 0, 0), center, 200, 3)
        for i in range(12):
            import math
            ang = i * 30
            x = center[0] + math.sin(math.radians(ang)) * 180
            y = center[1] - math.cos(math.radians(ang)) * 180
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 4)

        mickey.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()