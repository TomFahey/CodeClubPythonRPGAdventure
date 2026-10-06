from game import *

# A dictionary linking a room to other rooms
rooms = {
    'Hall' : {
        'south' : 'Kitchen',
        'east' : 'Dining Room',
        'items' : ['key'],
        'visited' : False,
        'player' : True
    },
    'Kitchen' : {
        'north' : 'Hall',
        'items' : ['monster'],
        'visited' : False,
        'player' : False
    },
    'Dining Room' : {
        'west' : 'Hall',
        'south' : 'Garden',
        'items' : ['potion'],
        'visited' : False,
        'player' : False
    },
    'Garden' : {
        'north' : 'Dining Room',
        'visited' : False,
        'player' : False
    }
}

currentRoom = 'Hall'
rooms[currentRoom]['player'] = True

# Keep this to run the game loop from game.py 
currentRoom, inventory = run_game(currentRoom, inventory, rooms)
