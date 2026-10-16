from gui import _showMap, _showRoom, _showInventory


# An inventory, which is initially empty
inventory = []


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


def showStatus(currentRoom, rooms):
    # Print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    if 'item' in rooms[currentRoom]:
        print('You see a ' + rooms[currentRoom]['item'])
    print('---------------------------')
    _showRoom(currentRoom, rooms)
    rooms[currentRoom]['visited'] = True

    
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
def run_game(currentRoom, inventory, rooms):

    def go_command(direction):
        """Move the player to a different room if possible"""
        # First we check if the direction is valid
        if direction in rooms[currentRoom]:
            # If it is, we move the player to the new room
            newRoom = rooms[currentRoom][direction]
            return newRoom
        else:
            print('You cannot go that way!')
            return currentRoom

    def get_command(item, inventory):
        # If the room contains an item, and the item is the one they want to get
        if 'item' in rooms[currentRoom] and item == rooms[currentRoom]['item']:
            # Add the item to their inventory
            inventory.insert(0, rooms[currentRoom]['item'])
            print('You picked up the ' + item)
            # Delete the item from the room
            del rooms[currentRoom]['item']
        else:
            # Tell them they can't get it
            print('There is no ' + item + ' here!')

    def show_command(view):
        if view == 'map':
            _showMap(currentRoom, rooms)
        elif view == 'inventory':
            _showInventory(inventory)

    showInstructions()


    # Loop forever
    while True:



        showStatus(currentRoom, rooms)

        # Get the player's next command:
        # the first word is the command, the second word is the argument
        # e.g typing 'go east' is equivalent to setting:
        # command = 'go'
        # argument = 'east'
        command, argument = get_player_command()

        # If the command is 'go', run the go_command function
        if command == 'go':
            currentRoom = go_command(direction=argument)

        # If they type 'get'
        if command == 'get':
            get_command(item=argument, inventory=inventory)

        # If they type 'show', show the map or inventory
        if command == 'show':
            show_command(view=argument)

        if 'item' in rooms[currentRoom] and rooms[currentRoom]['item'] == 'monster':
            print('A monster has got you... GAME OVER!')
            break

        # add more game play here


    return currentRoom, inventory