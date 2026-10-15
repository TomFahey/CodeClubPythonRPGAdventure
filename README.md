# CodeClubPythonRPGAdventure

Coding extension to the ["Escape the Maze"](https://projects.raspberrypi.org/en/projects/editor-rpg/landing) Code Club project, for new Python coders.

Adding `gui_pure.py` to the Project files will allow you to import the `_showMap` and `_showInventory` functions.

```python
from gui import _showMap, _showInventory  # Add this at the top of game.py
```

`game.py` shows a simple example of how to include these functions in the game,

```python
def run_game(currentRoom, inventory, rooms):
    showInstructions()

    # Loop forever
    while True:

        showStatus(currentRoom, rooms)

        ...

        # If they type 'map', show the map
        if move[0] == 'map':
            _showMap(currentRoom, rooms)

        # If they type 'inventory', show the inventory
        if move[0] == 'inventory':
            _showInventory(inventory)
```

however students are encouraged to explore their own unique ways of including this graphical feature in whichever manner they desire!

### _showMap

`_showMap(currentRoom, rooms)` takes two arguments, the current room the player is in and the global `rooms` dictionary specified in `main.py`. Calling it will print out a emoji-based grid of the player's maze design, which hides the room the player hasn't discovered.


⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱🧱🧱🧱🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱🔑️▪️▪️🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🚪▪️🧍▪️🚪⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛🧱🧱🚪🧱🧱⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛


Various items can be added to rooms by including them under the `item` key for a given room in the `rooms` dictionary - a fairly comprehensive list of item names that will print a corresponding emoji can be found at the top of the `gui_pure.py` file:

```python
icons = {
    "key" :             "\U0001F511\U0000FE0F",      ### 🔑
    "dagger" :          "\U0001F5E1\U0000FE0F",      ### 🗡 
    "sword" :           "\U0001F5E1\U0000FE0F",      ### 🗡️
    "shield" :          "\U0001F6E1\U0000FE0F",      ### 🛡️
    "potion" :          "\U0001F9EA",                ### 🧪
    "bow" :             "\U0001F3F9",                ### 🏹
    "axe" :             "\U0001FA93",                ### 🪓
    "player" :          "\U0001F9CD",                ### 🧍
    "monster" :         "\U0001F479",                ### 👹
    "treasure" :        "\U0001F4B0",                ### 💰
    "door" :            "\U0001F6AA",                ### 🚪
    "wall" :            "\U0001F9F1",                ### 🧱
    "wallpaper" :       "\U0001F7EB",                ### 🟫
    "black_square" :    "\U00002B1B",                ### ⬛
    "white_square" :    "\U00002B1C",                ### ⬜
    "lock" :            "\U0001F512",                ### 🔒
    "floor" :           "\U000025AA\U0000FE0F",      ### ▪️
    "empty" :           "",                          ### 
}
```

### _showInventory

`_showInventory(inventory)` takes the player's `inventory` list and shows the following bar, populated with the matching emojis:

■■■■▶ Inventory ◀■■■■
▫ 🧪 🔑️ ⬜ ⬜ ⬜ ▫
■■■■■■■■■■■■■■■■■■■■■■

When an item is picked up from a room, it will visibly disappear from the map

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🔑️▪️▪️🧱🧪▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🚪▪️▪️▪️🚪▪️▪️🧍▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🧱🚪🧱🧱🧱🧱🚪🧱🧱🧱⬛⬛⬛⬛

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🔑️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🚪▪️▪️▪️🚪▪️▪️🧍▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱▪️▪️▪️🧱▪️▪️▪️▪️▪️🧱⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🧱🧱🚪🧱🧱🧱🧱🚪🧱🧱🧱⬛⬛⬛⬛

Learners can try to implement their own Python code to handle the inventory, such as how many items they are allowed to pick before the inventory bar becomes "full", or what happens to "consumable" items when they get used.

