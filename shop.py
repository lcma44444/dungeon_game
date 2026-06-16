import os
import numpy as np
import cv2
from pydantic import BaseModel

TILE_SIZE = 64

TILE_PATH = os.path.split(__file__)[0] + '/tiles'

GAME_TITLE = "Shop"


SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640

def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    if img is None:
        raise IOError(f"Image not found: '{filename}'")
    img = np.kron(img, np.ones((2, 2, 1), dtype=img.dtype))  # double image size
    return img

def read_images():
    return {
        filename[:-4]: read_image(os.path.join(TILE_PATH, filename))
        for filename in os.listdir(TILE_PATH)
        if filename.endswith(".png")
    }

def draw_tile(frame, x, y, image, xbase=0, ybase=0):
    # calculate screen position in pixels
    xpos = xbase + x * TILE_SIZE
    ypos = ybase + y * TILE_SIZE
    # copy the image to the screen4
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


class Shop(BaseModel):
    size: int
    items: list[str]
    cost: list[int]
    frame_x: int

item_descriptions = {
    "sword": "a super magic sword that gives +2 damage",
}


def draw(game, shop, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    # draw_tile(frame=frame, x=2, y=3, image=images["sword"])
    
    # draw frame
    blue = 255, 150, 150
    frame[100:100 + 5, 200:200 + TILE_SIZE] = blue
    frame[100 + TILE_SIZE:100 + TILE_SIZE + 5, 200:200 + TILE_SIZE] = blue

    cv2.imshow(GAME_TITLE, frame)


def handle_keyboard():
    """keys are mapped to move commands"""
    key = chr(cv2.waitKey(1) & 0xFF)
    MOVES = {
        "a": "left",
        "d": "right",
        "w": "up",
        "s": "down",
    }
    if key in MOVES:
        return MOVES[key]


def visit_shop(game):
    images = read_images()
    shop = ...
    while ...:
        draw(game, shop, images)
        move = handle_keyboard()
        ...  # move could also be None