from gui_pure import _showMap, _showRoom, _showInventory
# An inventory, which is initially empty
inventory = []
from p5 import loop, no_loop


# Start the player in the Hall

def showInstructions():
    # Print a main menu and the commands
    print('''
Monster Game
========
Commands:
go [direction]
get [item]
show [map, inventory]
''')


def showStatus(gamestate):
    # Print the player's current status
    print('---------------------------')
    print('You are in the ' + gamestate.currentRoom)
    if 'item' in gamestate.rooms[gamestate.currentRoom]:
        print('You see a ' + gamestate.rooms[gamestate.currentRoom]['item'])
    print('---------------------------')
    _showRoom(gamestate.currentRoom, gamestate.rooms)
    gamestate.rooms[gamestate.currentRoom]['visited'] = True

    
def get_player_command():
    # Get the player's next 'move'
    # .split() breaks it up into an list array
    # e.g. typing 'go east' would give the list:
    # ['go','east']
    move = ''
    while move == '':
        move = input('>')
    command, argument = move.lower().split()
    return command, argument



