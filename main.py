"""
graphics engine for 2D games
"""
import os
import numpy as np
import cv2
from game import start_game, move_player
from game import update
from cutscene import show_cutscene, show_victory
from pygame import mixer

mixer.init()
mixer.music.load("Fight in the Dungeon.mp3")
mixer.music.play(loops=-1)
TILE_PATH = os.path.split(__file__)[0] + '/tiles'



# title of the game window
GAME_TITLE = "Dungeon Explorer"

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 960, 640
TILE_SIZE = 64


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
    # copy the image to the screen
    frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image


def draw_move(frame, move, images):
    draw_tile(frame, x=move.from_x, y=move.from_y, image=images[move.tile], xbase=move.progress * move.speed_x, ybase=move.progress * move.speed_y)
    move.progress += 1


def clean_moves(game, moves):
    result = []
    for m in moves:
        if m.progress * max(abs(m.speed_x), abs(m.speed_y)) < TILE_SIZE:
            result.append(m)
        else:
            m.complete = True
            if m.finished is not None:
                m.finished(game)
    return result

def is_player_moving(moves):
    return any([m for m in moves if m.tile == "player"])

def draw(game, images, moves):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
    
    SYMBOLS = {
    ".": "floor",
    "#": "wall",
    "|": "wall_lower",
    "w": "fountain",
    "x": "stairs_down",
    "$": "coin",
    "k": "key",
    "t": "trap",
    "D": "closed_door",
    "d": "open_door",
    "T": "teleporter",
    "f": "fireball",
    "h": "heart",
    "s": "black_switch",
    "b": "bat",
    "g": "green_switch",
    "c": "chest",
    "u": "stairs_up",
    "e": "eye",
    "r": "red_pix_switch",
    "explosion": read_image("tiles/explosion_pixelfied.png")

    }

    # draw dungeon tiles
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])
    
    for t in game.current_level.teleporters:
        draw_tile(frame, x=t.x, y=t.y, image=images["teleporter"])
    
    while game.moves:
        moves.append(game.moves.pop())
    
    if not is_player_moving(moves):
        draw_tile(frame=frame, x=game.x, y=game.y, image=images["player"])
    
    # draw everything that moves
    for m in moves:
        draw_move(frame=frame, move=m, images=images)
    
    for i in range(game.health):
        draw_tile(frame, xbase=700, ybase=130, x=i, y=0, image=images["heart"])

    for i, item in enumerate(game.items):
        y = i // 2  # floor division: rounded down
        x = i % 2   # modulo: remainder of an integer division
        draw_tile(frame, xbase=645, ybase=200, x=x, y=y, image=images[item])

    draw_tile(frame, x=11, y=1, image=images["coin"])
    cv2.putText(frame,
            str(game.coins),
            org=(780, 110),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1.5,
            color=(255, 128, 128),
            thickness=3,
            )
    
    # draw special effects
    for e in game.effects:
        e.draw(frame)

    # display complete image
    cv2.imshow(GAME_TITLE, frame)

def update_effects(game):
    new_effects = []
    for e in game.effects:
        e.countdown -= 1
        if e.countdown >= 0:
            new_effects.append(e)
    game.effects = new_effects
#sound=mixer.sound("soundname")
def handle_keyboard(game):
    """keys are mapped to move commands"""
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        game.status = "exited"
    return MOVES.get(key)
def clean_explosions(game):
    """updates each explosion in the game"""
    result = []
    ...
    game.explosions = result

def main():
    images = read_images()
    show_cutscene()
    game = start_game()
    queued_move = None
    moves = []
    counter = 200
    while counter>0:
        draw(game, images, moves)
        update_effects(game)
        update(game)
        moves = clean_moves(game, moves)
        queued_move = handle_keyboard(game)
        if not is_player_moving(moves) and queued_move:
            move_player(game, queued_move)
        
        if game.status != "running":
            counter-=1
        
    if game.status == "finished" and game.coins >0:
        show_victory()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
