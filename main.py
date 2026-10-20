from game import run_game, inventory
from gui_pure import _showMap
from p5 import *



# A dictionary linking a room to other rooms
rooms = {
    'Hall' : {
        'south' : 'Kitchen',
        'east' : 'Dining Room',
        'west' : 'Office',
        'item' : 'key',
    },
    'Kitchen' : {
        'north' : 'Hall',
        'item' : 'monster',
    },
    'Dining Room' : {
        'west' : 'Hall',
        'south' : 'Garden',
        'item' : 'potion',
    },
    'Garden' : {
        'north' : 'Dining Room',
        'south' : 'Garage',
    },
    'Garage' : {
        'access' : 'Locked',
        'north' : 'Garden'
    },
    'Office' : {
        'east' : 'Hall'
    }
}

currentRoom = 'Hall'


class GameState:

    def __init__(self, currentRoom, rooms, inventory=[]):
        self.currentRoom = currentRoom
        self.rooms = rooms
        self.inventory = []

gamestate = GameState(currentRoom, rooms)

def setup():
    size(400, 400)
    no_stroke()
    text_size(15)
    no_loop()

def draw_background():
    BROWN = Color(185, 155, 115)
    BLUE = Color(5, 5, 5)
    background(BLUE) 
    fill(BROWN)

def draw():
    global gamestate
    draw_background()
    game_map = _showMap(gamestate.currentRoom, gamestate.rooms)
    print(gamestate.currentRoom)
    for row_number, row in enumerate(game_map):
        for col_number,character, in enumerate(row):
            text(character, col_number*15,20+row_number*15)


run(frame_rate=1)
# Keep this to run the game loop from game.py 
currentRoom, inventory = run_game(gamestate)
