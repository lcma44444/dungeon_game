import numpy as np
from pydantic import BaseModel

TILE_SIZE = 64

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