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


    
# Run the main game loop using state kept in `main.py`.
def run_game(gamestate):

    def go_command(direction):
        """Move the player to a different room if possible"""
        # First we check if the direction is valid
        if direction in gamestate.rooms[gamestate.currentRoom]:
            # If it is, we move the player to the new room
            newRoom = gamestate.rooms[gamestate.currentRoom][direction]
            if 'access' in newRoom:
                if newRoom['access'] == 'Locked' and 'key' not in inventory:
                    print('The door is locked. You need a key to enter.')
                    return gamestate.currentRoom
                else:
                    gamestate.rooms[newRoom]['access'] = 'Unlocked'
                    print('You unlocked the door.')
            return newRoom
        else:
            print('You cannot go that way!')
            return gamestate.currentRoom

    def get_command(item, gamestate):
        # If the room contains an item, and the item is the one they want to get
        if 'item' in gamestate.rooms[gamestate.currentRoom] and item == gamestate.rooms[gamestate.currentRoom]['item']:
            # Add the item to their inventory
            gamestate.inventory.insert(0, gamestate.rooms[gamestate.currentRoom]['item'])
            print('You picked up the ' + item)
            # Delete the item from the room
            del gamestate.rooms[gamestate.currentRoom]['item']
        else:
            # Tell them they can't get it
            print('There is no ' + item + ' here!')

    def show_command(view):
        if view == 'map':
            _showMap(gamestate.currentRoom, gamestate.rooms)
        elif view == 'inventory':
            _showInventory(gamestate.inventory)

    showInstructions()

    # Loop forever
    while True:
        showStatus(gamestate)
        loop()
        # Get the player's next command:
        # the first word is the command, the second word is the argument
        # e.g typing 'go east' is equivalent to setting:
        # command = 'go'
        # argument = 'east'
        command, argument = get_player_command()

        # If the command is 'go', run the go_command function
        if command == 'go':
            gamestate.currentRoom = go_command(direction=argument)

        # If they type 'get'
        if command == 'get':
            get_command(item=argument, gamestate=gamestate)

        # If they type 'show', show the map or inventory
        if command == 'show':
            show_command(view=argument)

        if 'item' in gamestate.rooms[gamestate.currentRoom] and gamestate.rooms[gamestate.currentRoom]['item'] == 'monster':
            print('A monster has got you... GAME OVER!')
            break

        no_loop()

        
        # add more game play here


    return gamestate.currentRoom, gamestate.inventory
