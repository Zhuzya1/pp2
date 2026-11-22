import pygame
import math
from datetime import datetime


class MickeyClock:
    """Clock that uses Mickey's hands as minute/second hands."""

    def __init__(self, screen, center, right_hand_img, left_hand_img):
        self.screen = screen
        self.center = center
        self.right_hand = right_hand_img   # minutes
        self.left_hand = left_hand_img     # seconds

    def _rotate_hand(self, image, angle_deg):
        """Rotate around the pivot which is assumed to be at the bottom-center."""
        rotated = pygame.transform.rotate(image, -angle_deg)
        # pygame rotates around the center; shift so the base stays at pivot
        rect = rotated.get_rect(center=self.center)
        return rotated, rect

    def draw(self):
        now = datetime.now()
        seconds = now.second
        minutes = now.minute

        # Seconds hand: 360° per 60s -> 6° per second
        sec_angle = seconds * 6
        # Minutes hand: 360° per 60min -> 6° per minute
        min_angle = minutes * 6

        # Draw right (minutes) hand
        r_img, r_rect = self._rotate_hand(self.right_hand, min_angle)
        self.screen.blit(r_img, r_rect)

        # Draw left (seconds) hand
        l_img, l_rect = self._rotate_hand(self.left_hand, sec_angle)
        self.screen.blit(l_img, l_rect)

        # Digital time text
        font = pygame.font.SysFont("arial", 48, bold=True)
        text = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        self.screen.blit(text, (self.center[0] - text.get_width() // 2,
                                self.center[1] + 120))