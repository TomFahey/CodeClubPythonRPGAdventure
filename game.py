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
map
inventory
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
    
# Run the main game loop using state kept in `main.py`.
def run_game(currentRoom, inventory, rooms):
    showInstructions()

    # Loop forever
    while True:

        showStatus(currentRoom, rooms)

        # Get the player's next 'move'
        # .split() breaks it up into an list array
        # e.g. typing 'go east' would give the list:
        # ['go','east']
        move = ''
        while move == '':
            move = input('>')

        move = move.lower().split()

        # If they type 'go' first
        if move[0] == 'go':
            # Check that they are allowed wherever they want to go
            if move[1] in rooms[currentRoom]:
                rooms[currentRoom]['player'] = False
                # Set the current room to the new room
                currentRoom = rooms[currentRoom][move[1]]
                rooms[currentRoom]['player'] = True
            else:
                print('You cannot go that way!')

        # If they type 'get' first
        if move[0] == 'get':
            # If the room contains an item, and the item is the one they want to get
            if 'item' in rooms[currentRoom] and move[1] == rooms[currentRoom]['item']:
                # Add the item to their inventory
                inventory.insert(0, rooms[currentRoom]['item'])
                print('You picked up the ' + move[1])
                # Delete the item from the room
                del rooms[currentRoom]['item']
            else:
                # Tell them they can't get it
                print('There is no ' + move[1] + ' here!')

        # If they type 'map', show the map
        if move[0] == 'map':
            _showMap(currentRoom, rooms)

        # If they type 'inventory', show the inventory
        if move[0] == 'inventory':
            _showInventory(inventory)

        if 'item' in rooms[currentRoom] and rooms[currentRoom]['item'] == 'monster':
            print('A monster has got you... GAME OVER!')
            break

        # add more game play here


    return currentRoom, inventory

