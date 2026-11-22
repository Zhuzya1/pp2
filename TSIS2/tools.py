import pygame
from collections import deque


# ---------- Base tool ----------
class BaseTool:
    """Abstract base for tools operating on a shared canvas surface."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.color = (0, 0, 0)
        self.size = 5

    def set_color(self, c):
        self.color = c

    def set_size(self, s):
        self.size = s

    def on_mouse_down(self, pos):
        pass

    def on_mouse_move(self, pos, last_pos):
        pass

    def on_mouse_up(self, pos):
        pass

    def draw_preview(self, screen, start, end):
        pass

    def cancel(self):
        pass


# ---------- Pencil ----------
class PencilTool(BaseTool):
    def on_mouse_down(self, pos):
        pygame.draw.circle(self.canvas, self.color, pos, self.size // 2)

    def on_mouse_move(self, pos, last_pos):
        if last_pos is None:
            return
        pygame.draw.line(self.canvas, self.color, last_pos, pos, self.size)
        pygame.draw.circle(self.canvas, self.color, pos, self.size // 2)


# ---------- Straight line with live preview ----------
class LineTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def on_mouse_up(self, pos):
        if self.start:
            pygame.draw.line(self.canvas, self.color, self.start, pos, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            p_start = (self.start[0], self.start[1] + 60)
            p_end = (end[0], end[1])
            pygame.draw.line(screen, self.color, p_start, p_end, self.size)

    def cancel(self):
        self.start = None


# ---------- Rectangle ----------
class RectangleTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def on_mouse_up(self, pos):
        if self.start:
            x1, y1 = self.start
            x2, y2 = pos
            rect = pygame.Rect(min(x1, x2), min(y1, y2),
                               abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(self.canvas, self.color, rect, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            x1, y1 = self.start
            x2, y2 = end
            rect = pygame.Rect(min(x1, x2), min(y1, y2) + 60,
                               abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(screen, self.color, rect, self.size)

    def cancel(self):
        self.start = None


# ---------- Circle ----------
class CircleTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def on_mouse_up(self, pos):
        if self.start:
            x1, y1 = self.start
            x2, y2 = pos
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(self.canvas, self.color, self.start, radius, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            x1, y1 = self.start
            x2, y2 = end
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(screen, self.color,
                               (x1, y1 + 60), radius, self.size)

    def cancel(self):
        self.start = None


# ---------- Eraser ----------
class EraserTool(PencilTool):
    def on_mouse_down(self, pos):
        pygame.draw.circle(self.canvas, (255, 255, 255), pos, self.size * 2)

    def on_mouse_move(self, pos, last_pos):
        if last_pos is None:
            return
        pygame.draw.line(self.canvas, (255, 255, 255), last_pos, pos, self.size * 4)
        pygame.draw.circle(self.canvas, (255, 255, 255), pos, self.size * 2)


# ---------- Square ----------
class SquareTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def on_mouse_up(self, pos):
        if self.start:
            x1, y1 = self.start
            x2, y2 = pos
            side = min(abs(x2 - x1), abs(y2 - y1))
            sx = x1 if x2 >= x1 else x1 - side
            sy = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(self.canvas, self.color,
                             (sx, sy, side, side), self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            x1, y1 = self.start
            x2, y2 = end
            side = min(abs(x2 - x1), abs(y2 - y1))
            sx = x1 if x2 >= x1 else x1 - side
            sy = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(screen, self.color,
                             (sx, sy + 60, side, side), self.size)

    def cancel(self):
        self.start = None


# ---------- Right triangle ----------
class RightTriangleTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def _points(self, p1, p2):
        # right angle at (p2.x, p1.y)
        return [p1, (p2[0], p1[1]), p2]

    def on_mouse_up(self, pos):
        if self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(self.canvas, self.color, pts, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            pts = self._points(self.start, end)
            pts = [(p[0], p[1] + 60) for p in pts]
            pygame.draw.polygon(screen, self.color, pts, self.size)

    def cancel(self):
        self.start = None


# ---------- Equilateral triangle ----------
class EquilateralTriangleTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def _points(self, p1, p2):
        side = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        h = int(side * (3 ** 0.5) / 2)
        return [(p1[0], p1[1]), (p1[0] - side // 2, p1[1] + h),
                (p1[0] + side // 2, p1[1] + h)]

    def on_mouse_up(self, pos):
        if self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(self.canvas, self.color, pts, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            pts = self._points(self.start, end)
            pts = [(p[0], p[1] + 60) for p in pts]
            pygame.draw.polygon(screen, self.color, pts, self.size)

    def cancel(self):
        self.start = None


# ---------- Rhombus ----------
class RhombusTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start = None

    def on_mouse_down(self, pos):
        self.start = pos

    def _points(self, p1, p2):
        cx = (p1[0] + p2[0]) // 2
        cy = (p1[1] + p2[1]) // 2
        return [(cx, p1[1]), (p2[0], cy), (cx, p2[1]), (p1[0], cy)]

    def on_mouse_up(self, pos):
        if self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(self.canvas, self.color, pts, self.size)
        self.start = None

    def draw_preview(self, screen, start, end):
        if self.start:
            pts = self._points(self.start, end)
            pts = [(p[0], p[1] + 60) for p in pts]
            pygame.draw.polygon(screen, self.color, pts, self.size)

    def cancel(self):
        self.start = None


# ---------- Flood fill ----------
class FloodFillTool(BaseTool):
    """
    Scanline-free, BFS flood fill. Uses get_at/set_at as required.
    Stops at any pixel not exactly matching the target color (tolerance=0).
    """

    def on_mouse_down(self, pos):
        # pos is in canvas coordinates already (caller shifts toolbar)
        x0, y0 = pos
        w, h = self.canvas.get_size()
        if not (0 <= x0 < w and 0 <= y0 < h):
            return

        target = self.canvas.get_at((x0, y0))[:3]
        replacement = self.color[:3]
        if target == replacement:
            return

        # Optional: also stop at black outline (like classic paint)
        visited = set()
        queue = deque()
        queue.append((x0, y0))
        visited.add((x0, y0))

        while queue:
            x, y = queue.popleft()
            px = self.canvas.get_at((x, y))[:3]
            if px != target:
                continue
            self.canvas.set_at((x, y), replacement)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


# ---------- Text tool ----------
class TextTool(BaseTool):
    """
    Click to place a cursor; type characters; Enter confirms; Esc cancels.
    The live text is drawn on the screen surface each frame (not into canvas
    until Enter is pressed).
    """

    def __init__(self, canvas, font):
        super().__init__(canvas)
        self.font = font
        self.text = ""
        self.pos = None
        self.active = False

    def on_mouse_down(self, pos):
        # If already editing, confirm previous first
        if self.active and self.text:
            self._commit()
        self.pos = pos
        self.text = ""
        self.active = True

    def handle_key(self, event):
        if not self.active:
            return False
        if event.key == pygame.K_RETURN:
            self._commit()
            return True
        if event.key == pygame.K_ESCAPE:
            self.active = False
            self.text = ""
            return True
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return True
        # printable char
        if event.unicode and event.unicode.isprintable():
            self.text += event.unicode
            return True
        return False

    def _commit(self):
        if self.pos and self.text:
            surf = self.font.render(self.text, True, self.color)
            self.canvas.blit(surf, self.pos)
        self.text = ""
        self.active = False

    def draw_live(self, screen):
        if self.active and self.pos and self.text:
            surf = self.font.render(self.text, True, self.color)
            screen.blit(surf, (self.pos[0], self.pos[1] + 60))
            # cursor
            w = surf.get_width()
            pygame.draw.line(screen, self.color,
                             (self.pos[0] + w, self.pos[1] + 60),
                             (self.pos[0] + w, self.pos[1] + 60 + self.font.get_height()),
                             1)

    def cancel(self):
        self.active = False
        self.text = ""
        self.pos = None