from game import *

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
        'north' : 'Garden'
    },
    'Office' : {
        'east' : 'Hall'
    }
}

currentRoom = 'Hall'

# Keep this to run the game loop from game.py 
currentRoom, inventory = run_game(currentRoom, inventory, rooms)
