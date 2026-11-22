import pygame
import sys
from datetime import datetime
from tools import (
    PencilTool, LineTool, FloodFillTool, TextTool,
    RectangleTool, CircleTool, EraserTool,
    SquareTool, RightTriangleTool, EquilateralTriangleTool, RhombusTool,
)

# ---------- Configuration ----------
WIDTH, HEIGHT = 1000, 700
TOOLBAR_H = 60
CANVAS_RECT = pygame.Rect(0, TOOLBAR_H, WIDTH, HEIGHT - TOOLBAR_H)

BG_COLOR = (255, 255, 255)
TOOLBAR_COLOR = (230, 230, 230)
ACTIVE_COLOR = (100, 160, 255)

SIZES = {1: 2, 2: 5, 3: 10}  # keyboard 1/2/3 -> px

# ---------- Init ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 16)
font_small = pygame.font.SysFont("arial", 13)

# Canvas is a separate surface so drawing is persistent
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill(BG_COLOR)

# ---------- State ----------
current_color = (0, 0, 0)
current_size = 5           # default medium
active_tool_name = "pencil"

# Register all tools
tools = {
    "pencil":  PencilTool(canvas),
    "line":    LineTool(canvas),
    "rect":    RectangleTool(canvas),
    "circle":  CircleTool(canvas),
    "eraser":  EraserTool(canvas),
    "square":  SquareTool(canvas),
    "rtri":    RightTriangleTool(canvas),
    "etri":    EquilateralTriangleTool(canvas),
    "rhombus": RhombusTool(canvas),
    "fill":    FloodFillTool(canvas),
    "text":    TextTool(canvas, font),
}

# Palette for the color picker
PALETTE = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 128, 0),
    (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128),
]

# ---------- Toolbar buttons ----------
# Each button: (rect, label, tool_name)
def build_buttons():
    buttons = []
    x = 10
    y = 10
    for name in ["pencil", "line", "rect", "circle", "eraser",
                 "square", "rtri", "etri", "rhombus", "fill", "text"]:
        label = name[:4]
        w = 55
        buttons.append((pygame.Rect(x, y, w, 20), label, name))
        x += w + 5
    # size buttons row
    x = 10
    y = 35
    for k, px in SIZES.items():
        buttons.append((pygame.Rect(x, y, 55, 20), f"{k}:{px}px", f"size{k}"))
        x += 60
    return buttons

buttons = build_buttons()

# Color swatch rects
def build_swatches():
    sw = []
    x = 260
    y = 12
    for c in PALETTE:
        sw.append((pygame.Rect(x, y, 22, 22), c))
        x += 28
    return sw

swatches = build_swatches()


def draw_toolbar():
    pygame.draw.rect(screen, TOOLBAR_COLOR, (0, 0, WIDTH, TOOLBAR_H))
    for rect, label, name in buttons:
        active = False
        if name == active_tool_name:
            active = True
        elif name.startswith("size") and int(name[-1]) in SIZES:
            if SIZES[int(name[-1])] == current_size:
                active = True
        color = ACTIVE_COLOR if active else (200, 200, 200)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1, border_radius=4)
        text = font_small.render(label, True, (0, 0, 0))
        screen.blit(text, (rect.x + 4, rect.y + 3))

    for rect, c in swatches:
        pygame.draw.rect(screen, c, rect)
        border = ACTIVE_COLOR if c == current_color else (80, 80, 80)
        pygame.draw.rect(screen, border, rect, 2)

    # current color + size preview
    pygame.draw.rect(screen, current_color, (WIDTH - 60, 12, 30, 30))
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 60, 12, 30, 30), 1)
    pygame.draw.circle(screen, current_color, (WIDTH - 90, 27), current_size // 2)


def save_canvas():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{ts}.png"
    pygame.image.save(canvas, filename)
    print(f"[saved] {filename}")


# ---------- Main loop ----------
running = True
mouse_down = False
last_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---- Keyboard shortcuts ----
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

            if ctrl and event.key == pygame.K_s:
                save_canvas()
                continue

            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                current_size = SIZES[int(event.unicode)]
                for t in tools.values():
                    t.size = current_size
                continue

            # Text tool events (Enter/Escape handled here)
            if active_tool_name == "text":
                handled = tools["text"].handle_key(event)
                if handled:
                    continue

            # Escape cancels other in-progress ops
            if event.key == pygame.K_ESCAPE:
                for t in tools.values():
                    t.cancel()

        # ---- Mouse events ----
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my < TOOLBAR_H:
                # toolbar click
                for rect, label, name in buttons:
                    if rect.collidepoint(mx, my):
                        if name.startswith("size"):
                            current_size = SIZES[int(name[-1])]
                            for t in tools.values():
                                t.size = current_size
                        else:
                            active_tool_name = name
                        break
                for rect, c in swatches:
                    if rect.collidepoint(mx, my):
                        current_color = c
                        break
                continue
            # canvas click
            cpos = (mx, my - TOOLBAR_H)
            mouse_down = True
            last_pos = cpos
            tool = tools[active_tool_name]
            tool.set_color(current_color)
            tool.set_size(current_size)
            tool.on_mouse_down(cpos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_down and last_pos is not None:
                tool = tools[active_tool_name]
                tool.on_mouse_up(last_pos)
            mouse_down = False
            last_pos = None

        elif event.type == pygame.MOUSEMOTION and mouse_down:
            mx, my = event.pos
            if my >= TOOLBAR_H:
                cpos = (mx, my - TOOLBAR_H)
                tool = tools[active_tool_name]
                tool.on_mouse_move(cpos, last_pos)
                last_pos = cpos

    # ---------- Render ----------
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, TOOLBAR_H))

    # Live preview for line/shapes
    if mouse_down and last_pos is not None:
        tool = tools[active_tool_name]
        tool.draw_preview(screen, last_pos, pygame.mouse.get_pos())
    # Text tool live render
    if active_tool_name == "text":
        tools["text"].draw_live(screen)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
sys.exit()