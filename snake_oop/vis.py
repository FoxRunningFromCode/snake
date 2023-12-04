import numpy as np
import cv2

import grid_game as gg

# bgr
Color = tuple[float, float, float]
BLUE = (1., 0., 0.)
GREEN = (0., 1., 0.) 
RED = (0., 0., 1.)
CYAN = (1., 1., 0.)
MAGENTA = (1., 0., 1.)
YELLOW = (0., 1., 1.)
WHITE = (1., 1., 1.)
BLACK = (0., 0., 0.)
GREY = (0.5,0.5,0.5)


def draw_circle(img: np.ndarray, pos: gg.GridPosition, color: Color, cell_length_px: int, size=1., fill=False):
    x, y = [int((p + 0.5) * cell_length_px) for p in (pos.x, pos.y)]
    radius = int(round(cell_length_px / 2 * size))
    cv2.circle(
        img=img, center=(x, y), radius=radius,
        color=color, thickness=-1 if fill else 2,
    )


def draw_square(img: np.ndarray, top_left: tuple[int, int], side_length: int, color: Color, fill: bool = False):
    x, y = top_left
    if fill:
        cv2.rectangle(img, (x, y), (x + side_length, y + side_length), color, thickness=cv2.FILLED)
    else:
        cv2.rectangle(img, (x, y), (x + side_length, y + side_length), color, thickness=2)