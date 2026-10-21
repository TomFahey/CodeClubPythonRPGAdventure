from game import run_game
from gui_pure import setup, draw_all
from p5 import run


# Define our rooms :

### Hall has:
# - the Kitchen to the South, 
# - the Dining Room to the East
# - the Office to the West
# - An item named key inside it
Hall = {
    'south' : 'Kitchen',
    'east'  : 'Dining Room',
    'west'  : 'Office',
    'item'  : 'key'
}

Kitchen = {
    'north' : 'Hall',
    'item'  : 'monster'
}

Dining_Room = {
    'west'  : 'Hall',
    'south' : 'Garden',
    'item'  : 'potion'
}

Garden = {
    'north' : 'Dining Room',
    'south' : 'Garage'
}

Garage = {
    'north' : 'Garden'
}

Office = {
    'east' : 'Hall'
}


# Our combined map of all our rooms
rooms = {
    'Hall'        : Hall,
    'Kitchen'     : Kitchen,
    'Dining Room' : Dining_Room,
    'Garden'      : Garden,
    'Garage'      : Garage,
    'Office'      : Office
}


class Player:

    def __init__(self, startingRoom, map):
        self.currentRoom = startingRoom
        self.map = rooms 
        self.inventory = [] # Empty
        #self.health = 3 # 3 hearts

# We create our player object, that records
# which room we are currently in, our inventory
# and which rooms we have visited.
player = Player(
    startingRoom='Hall', 
    map = rooms
)

def draw():
    global gamestate
    draw_all(player)

    
run(frame_rate=1)
# Keep this to run the game loop from game.py 
currentRoom, inventory = run_game(player)
