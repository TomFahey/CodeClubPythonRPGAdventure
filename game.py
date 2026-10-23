from p5 import loop, no_loop

# An inventory, which is initially empty
inventory = []

# Start the player in the Hall
currentRoom = 'Hall'

def showInstructions():
    # Print a main menu and the commands
    print('''
Monster Game
========
Commands:
go [direction]
get [item]
''')


def showStatus(currentRoom, inventory, rooms):
    # Print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    # Print the current inventory
    print('Inventory : ' + str(inventory))
    # Print an item if there is one
    if 'item' in rooms[currentRoom]:
        print('You see a ' + rooms[currentRoom]['item'])
    print('---------------------------')
    
# Run the main game loop using state kept in `main.py`.
def run_game(player):
    showInstructions()

    # Loop forever
    while True:

        currentRoom = player.currentRoom
        inventory = player.inventory
        rooms = player.rooms

        showStatus(currentRoom, inventory, rooms)
        loop()

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
                # Set the current room to the new room
                currentRoom = rooms[currentRoom][move[1]]
            else:
                print('You cannot go that way!')

        # If they type 'get' first
        if move[0] == 'get':
            # If the room contains an item, and the item is the one they want to get
            if 'item' in rooms[currentRoom] and move[1] == rooms[currentRoom]['item']:
                # Add the item to their inventory
                inventory.append(move[1])
                print('You picked up the ' + move[1])
                # Delete the item from the room
                del rooms[currentRoom]['item']
            else:
                # Tell them they can't get it
                print('There is no ' + move[1] + ' here!')

        if 'item' in rooms[currentRoom] and rooms[currentRoom]['item'] == 'monster':
            print('A monster has got you... GAME OVER!')
            break

        # add more game play here

        # Update the player object with the current state
        player.currentRoom = currentRoom
        player.inventory = inventory
        player.rooms = rooms
        no_loop()



    return player.currentRoom, player.inventory

