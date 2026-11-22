import pygame
import sys
import os
from player import MusicPlayer

WIDTH, HEIGHT = 700, 300
FPS = 30


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)

    base = os.path.dirname(__file__)
    player = MusicPlayer(os.path.join(base, "music"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next()
                elif event.key == pygame.K_b:
                    player.previous()
                elif event.key == pygame.K_q:
                    running = False

        screen.fill((30, 30, 40))

        title = font.render("Music Player", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        track = font.render(f"Track: {player.current_track_name()}",
                            True, (200, 200, 255))
        screen.blit(track, (40, 100))

        status = "PLAYING" if player.playing else "STOPPED"
        st = font.render(f"Status: {status}", True, (100, 255, 100) if player.playing else (255, 120, 120))
        screen.blit(st, (40, 150))

        pos, _ = player.progress()
        prog = font_small.render(f"Elapsed: {pos:.1f}s", True, (180, 180, 180))
        screen.blit(prog, (40, 190))

        controls = font_small.render(
            "P = Play   S = Stop   N = Next   B = Previous   Q = Quit",
            True, (150, 150, 150))
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)

    player.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()