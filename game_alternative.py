from p5 import loop, no_loop


def showIntroduction():
    """Print the message shown at the start of the game"""
    print('''
Really cool sounding game title
===============================

I need to escape the dungeon!
''')



def showInstructions():
    """Print the list of commands available to the player"""
    print('''
Commands: cmd [argument]

go [direction]   # e.g go west
get [item]       # e.g get key
''')



def showStatus(player):
    """Print a message showing the room the player is
    currenly in, as well as any items that are present
    and return the current room they are in.
    """
    print('---------------------------')
    print('You are in the ' + player.currentRoom)
    if 'item' in player.rooms[player.currentRoom]:
        print('You see a ' + player.rooms[player.currentRoom]['item'])
    print('---------------------------')
    player.rooms[player.currentRoom]['visited'] = True

    
def get_player_command():
    """Get the player's next 'move'
    
    .split() breaks it up into the command and argument
    e.g. typing 'go east' would give the result:
    command, argument = ['go','east']
    """
    move = ''
    while move == '':
        move = input('>')
    try:
        command, argument = move.lower().split()
    except ValueError:
        command, argument = move.lower(), None
    return command, argument



def go_command(direction, player):
    """Move the player to a different room if possible

    If there is a room in the *direction* they pick,
    return that room. If not, just return the room they
    are currently in
    """
    # First we get the dictionary containing the room description
    room_description = player.rooms[player.currentRoom]
    # If the direction we has picked is in the room description,
    # we can move to that room
    if direction in room_description: 
        newRoom = player.rooms[player.currentRoom][direction]
        return newRoom
    else:
        print('You cannot go that way!')
        return player.currentRoom



def get_command(item, player):
    """Get the specified *item* from the room

    If the requested *item* is in the room, move it to the
    player's inventory and delete it from the room. If it
    is not in the room, print a message saying so.
    """
    # First we get the dictionary containing the room description
    room_description = player.rooms[player.currentRoom]
    if item is None:
        print("You didn't tell me what to get!")
    elif 'item' in room_description and room_description['item'] == item:
        # Add the item to their inventory
        player.rooms.inventory.insert(0, item)
        print('You picked up the ' + item)
        # Delete the item from the room
        del player.rooms[player.currentRoom]['item']
    else:
        # Tell them they can't get it
        print('There is no ' + item + ' here!')


    

def run_game(player):
    """Run the game! 
    
    Call this from the main.py file, using a Player object to track
    the game's progress.
    """

    showIntroduction() # Show the introduction text
    showInstructions() # Show the instruction text

    # Loop forever
    while True:
        
        ######## Step 1) Show the Player's current status, using the *player* state
        
        ## Get the current state from the player object
        showStatus(player)
        loop()
        

        ######## Step 2) Get the player's command that they have typed in
        
        command, argument = get_player_command()

        

        ######## Step 3) Match the *command* and *argument* to the right function
        
        if command == 'go': # If the command is 'go', run the go_command function
            player.currentRoom = go_command(argument, player)
            
        elif command == 'get': # If the command is 'get', run the get_command function
            get_command(argument, player)
                
        elif command == '?': # If the command is '?', show the instructions again
            showInstructions()
            
        #-------------- Add more commands here... --------------#
        
        else: # Finally, if no commands are recognised, print out a message saying so
            print(f"Sorry, I didn't recognise {command}")

        

        ######## Step 4) Check the game conditions
        
        # Player is in the room with a monster
        currentRoom_description = player.rooms[player.currentRoom]
        if 'item' in currentRoom_description and currentRoom_description['item'] == 'monster':
            print('A monster has got you... GAME OVER!')
            break
            
        #------------- Add more conditions here... ------------#


        no_loop()


    return player.currentRoom, player.inventory