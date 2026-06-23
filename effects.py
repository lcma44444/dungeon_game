import numpy as np
from pydantic import BaseModel
import os
import cv2

TILE_SIZE = 64
TILE_PATH = os.path.split(__file__)[0] + '/tiles'

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

class Effect(BaseModel):

    x: int
    y: int
    countdown: int

    def draw(self, frame):
        pass

class RandomBlur(Effect):

    def draw(self, frame):
        random_tile = np.random.randint(0, 255, size=(TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
        frame[self.y * TILE_SIZE: self.y * TILE_SIZE + TILE_SIZE,
            self.x * TILE_SIZE: self.x * TILE_SIZE + TILE_SIZE] = random_tile
        
class Explosion(Effect):
    x: int
    y: int
    max_frame: int = 16
    max_delay: int = 5
    delay: int = 0
    frame: int = 0
    
    def draw(self, frame):
        tile = read_image(os.path.split(__file__)[0] +"/tiles/explosion_pixelfied1.png")
        random_tile = np.random.randint(0, 255, size=(TILE_SIZE, TILE_SIZE, 3), dtype=np.uint8)
        frame[self.y * TILE_SIZE: self.y * TILE_SIZE + TILE_SIZE,
            self.x * TILE_SIZE: self.x * TILE_SIZE + TILE_SIZE] = tile
        
class FadeIn(Effect):

    def draw(self, frame):
        tile = frame[self.y * TILE_SIZE: self.y * TILE_SIZE + TILE_SIZE,
            self.x * TILE_SIZE: self.x * TILE_SIZE + TILE_SIZE]
        tile[tile > (255 - self.countdown)] = 0
        frame[self.y * TILE_SIZE: self.y * TILE_SIZE + TILE_SIZE,
            self.x * TILE_SIZE: self.x * TILE_SIZE + TILE_SIZE] = tile