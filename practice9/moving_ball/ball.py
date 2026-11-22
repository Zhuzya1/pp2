import pygame


class Ball:
    """A red ball that moves by 20px per keypress, bounded by the screen."""

    RADIUS = 25
    STEP = 20

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (255, 0, 0)

    def _bounds(self):
        w, h = self.screen.get_size()
        return w, h

    def _can_move(self, dx, dy):
        w, h = self._bounds()
        nx = self.x + dx
        ny = self.y + dy
        return (self.RADIUS <= nx <= w - self.RADIUS and
                self.RADIUS <= ny <= h - self.RADIUS)

    def move(self, dx, dy):
        if self._can_move(dx, dy):
            self.x += dx
            self.y += dy

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.RADIUS)