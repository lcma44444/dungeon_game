"""
the Dungeon Explorer game logic
"""
from pydantic import BaseModel
from typing import Callable
from moves import Move
import random  # add this on top of game.py
from typing import Literal
from effects import Effect, RandomBlur,Explosion
import time

Direction = Literal["up", "down", "left", "right"]
Position = tuple[int, int]
class Move(BaseModel):
    tile: str
    from_x: int
    from_y: int
    speed_x: int
    speed_y: int
    progress: int = 0
    complete: bool = False
    finished: Callable = None

class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    switches: list[switch_wall] = []
    fireballs: list[Fireball] = []
    skeletons: list[Skeleton] = []
    bats: list[Bat] = []

class DungeonGame(BaseModel):
    current_level: Level
    status: str = "running"
    x: int
    y: int
    moves: list[Move] = []
    items: list[str] = []
    effects: list[Effect] = []
    coins: int = 0
    health: int = 3
    level_number: int = 0

    
class Scary_Monsters(BaseModel):
    x: int
    y: int
    direction: Direction
    move: Move = None

class Teleporter(BaseModel):
    x: int
    y: int
    target_x: int
    target_y: int

class Fireball(Scary_Monsters):
    pass

class Skeleton(Scary_Monsters):
    pass

class Bat(Scary_Monsters):
    pass

class switch_wall(BaseModel):
    x: int 
    y: int
    move : Move = None


def parse_level(level):
    return [list(row) for row in level]



def get_next_position(x: int, y: int, direction: Direction) -> Position:
    
    if direction == "up":
        return (x, y - 1)
    elif direction == "down":
        return (x, y + 1)
    elif direction == "left":
        return (x - 1, y)
    elif direction == "right":
        return (x + 1, y)
def get_speed(direction:Direction):
    if direction == "left":
        return -5,0
    elif direction == "right":
        return 5,0
    elif direction == "up":
        return 0,-5
    elif direction == "down":
        return 0, 5
def get_skeleton_speed(direction:Direction):
    if direction == "left":
        return -1,0
    elif direction == "right":
        return 1,0
    elif direction == "up":
        return 0,-1
    elif direction == "down":
        return 0, 1

def move_fireball(game, fireball):
    new_x, new_y = get_next_position(fireball.x, fireball.y, fireball.direction)
    if game.current_level.level[new_y][new_x] in ".$ke":  # flies over coins and keys
        fireball.x = new_x
        fireball.y = new_y
        check_collision(game,fireball)
    elif fireball.direction == "right":
        fireball.direction = "left"
        
    elif fireball.direction == "left":
        fireball.direction = "right"
        
    elif fireball.direction == "up":
        fireball.direction = "down"
        
    elif fireball.direction == "down":
        fireball.direction = "up"
        
    speed_x, speed_y = get_speed(fireball.direction)
    fireball.move = Move(
        tile="fireball",
        from_x=fireball.x, from_y=fireball.y,
        speed_x = speed_x , speed_y = speed_y
    )
    game.moves.append(fireball.move)
    
def move_skeleton(game, skeleton):  # called by update!
    skeleton.direction = random.choice(["up", "down", "left", "right"])
    new_x, new_y = get_next_position(skeleton.x, skeleton.y, skeleton.direction)
    
    if game.current_level.level[new_y][new_x] in ".$k":  # flies over coins and keys
        speed_x, speed_y = get_skeleton_speed(skeleton.direction)
        skeleton.move = Move(
        tile="skeleton",
        from_x=skeleton.x, from_y=skeleton.y,
        speed_x = speed_x , speed_y = speed_y
    )
        game.moves.append(skeleton.move)
        skeleton.x = new_x
        skeleton.y = new_y
        check_collision(game,skeleton)

def move_bat(game, bat):
    bat.direction = random.choice(["up", "down", "left", "right"])
    new_x, new_y = get_next_position(bat.x, bat.y, bat.direction)
    
    if game.current_level.level[new_y][new_x] not in "#x":  
        speed_x, speed_y = get_skeleton_speed(bat.direction)
        bat.move = Move(
        tile="bat",
        from_x=bat.x, from_y=bat.y,
        speed_x = speed_x , speed_y = speed_y
    )
        game.moves.append(bat.move)
        bat.x = new_x
        bat.y = new_y
        check_collision(game,bat)

def take_damage(game):
    game.health -= 1
    print("damage")
    if game.health <= 0:
        game.effects.append(Explosion(x=game.x, y=game.y, countdown=200))
        game.status = "game over"

def recover(game):
    game.health +=1

def move_player(game: DungeonGame, direction: str) -> None:
    """Things that happen when the player walks on stuff"""

    new_x, new_y = get_next_position(game.x, game.y, direction)
    print(game.x, game.y)
    if game.current_level.level[new_y][new_x] == "$":
        game.current_level.level[new_y][new_x] = "."
        game.coins += 1
    
    if game.current_level.level[new_y][new_x] == "c":
        game.current_level.level[new_y][new_x] = "."
        game.coins += 10
    
    if game.current_level.level[new_y][new_x] == "e":
        game.current_level.level[new_y][new_x] = "."
        game.coins -= 5

    if game.current_level.level[new_y][new_x] == "k" :
        game.current_level.level[new_y][new_x] = "."
        game.items.append("key")
    
    if game.current_level.level[new_y][new_x] == "t" :
        game.current_level.level[new_y][new_x] = "."
        take_damage(game)

    if game.current_level.level[new_y][new_x] == "h" :
        game.current_level.level[new_y][new_x] = "."
        recover(game)

    if "key" in game.items and game.current_level.level[new_y][new_x] == "D":  # check whether there is a door
        game.items.remove("key")     # key can be used once
        game.current_level.level[new_y][new_x] = "d"                     # replace the closed door by an open one

    if game.current_level.level[new_y][new_x] in ".d":  # place all tiles on which you can walk here
        game.x = new_x
        game.y = new_y
    
    if game.current_level.level[new_y][new_x] == "*" :
        game.current_level.level[new_y][new_x] = "."
    #check_collision(game)

    if game.current_level.level[new_y][new_x] == "x":
        game.level_number += 1
    if game.level_number < len(LEVELS):
        # move to next level
        game.current_level = LEVELS[game.level_number]
    else:
        # no more levels left
        game.status = "finished"
    
    if game.current_level.level[new_y][new_x] == "u":
        game.level_number -= 1
        if game.level_number > len(LEVELS):
        # move to next level
            game.current_level = LEVELS[game.level_number]
        elif game.level_number<0:
        # no more levels left
            game.status = "finished"
    
    check_teleporters(game)

    if game.current_level.level[new_y][new_x] == "s" :
        game.current_level.level[new_y][new_x] = "."
        for s in game.current_level.switches:
            game.current_level.level[s.y][s.x] = "."
            move = Move(tile="wall",
                from_x=s.x, from_y=s.y,
                speed_x = 0, speed_y = 2
                ) 
        game.moves.append(move)
    
    if game.current_level.level[new_y][new_x] == "g" :
        game.current_level.level[new_y][new_x] = "."
        game.effects.append(RandomBlur(x=8, y=1, countdown=500))

    if game.x == 1 and game.y == 1 and game.current_level.level[7][1] == "#":
        game.current_level.level[7][1] = "."  # wall in row 4 column 3
        move = Move(tile="wall",
                from_x=1, from_y=7,
                speed_x = 0, speed_y = 2
                )
        game.moves.append(move)
        
def check_teleporters(game):
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y == t.y:
            game.x = t.target_x
            game.y = t.target_y

def check_collision(game,f):
    
        if f.x == game.x and f.y == game.y:
            take_damage(game)
            
            

def update(game):
    for f in game.current_level.fireballs:
        if f.move is None or f.move.complete:
            move_fireball(game, f)
        
    for s in game.current_level.skeletons:
        if s.move is None or s.move.complete:
            move_skeleton(game, s)

    for s in game.current_level.bats:
        if s.move is None or s.move.complete:
            move_bat(game, s)
        

def handle_secret_doors(game:DungeonGame, new_x: int, new_y: int):
    print("hi")
LEVEL_ONE = Level(
    level=parse_level([
    "###########",        
    "#hk.$.tk..#",
    "#..t..D...#",
    "#..e......#",
    "#.g.|D|...#",
    "#.s.|c|...#",
    "#...|||...#",
    "x#......t.#",
    "#.....t..u#",
    "###########",
    ]),
    
    teleporters=[Teleporter(x=1, y=2, target_x=1, target_y=8),],
    fireballs=[Fireball(x=7, y=3, direction = "left"),
            Fireball(x=7, y=7, direction = "left"),],
    skeletons=[Skeleton(x=2, y=8, direction = "right")],
    switches=[switch_wall(x=4, y=4)]
)
LEVEL_TWO = Level(
    level=parse_level([
    "##########",        
    "#......x.#",
    "#........#",
    "#........#",
    "#........#",
    "#........#",
    "#u.......#",
    "#........#",
    "#........#",
    "##########",
    ]),
    
    teleporters=[Teleporter(x=3, y=4, target_x=6, target_y=6),],
    fireballs=[Fireball(x=1, y=1, direction = "left"),
            Fireball(x=4, y=7, direction = "up"),],
    skeletons=[Skeleton(x=5, y=8, direction = "right"),
               Skeleton(x=8, y=1, direction = "right")],
    bats=[Bat(x=2, y=4, direction = "up")],
)
LEVEL_THREE = Level(
    level=parse_level([
    "##########",        
    "#.e....x.#",
    "#......e.#",
    "#..$$$...#",
    "#..$$$...#",
    "#..$$$...#",
    "#.e......#",
    "#......e.#",
    "#x.......#",
    "##########",
    ]),
    
    fireballs=[Fireball(x=1, y=1, direction = "left"),
            Fireball(x=4, y=7, direction = "up"),],
    skeletons=[Skeleton(x=5, y=8, direction = "right"),
               Skeleton(x=8, y=1, direction = "right")],
    bats=[Bat(x=2, y=4, direction = "up")],
)
def start_game():
    
    
    return DungeonGame(
    x=8,
    y=1,
    current_level = LEVEL_ONE,
    level_number = 0
)
        
LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE]

