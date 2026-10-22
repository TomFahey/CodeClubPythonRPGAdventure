# CodeClubPythonRPGAdventure

Coding extension to the ["Escape the Maze"](https://projects.raspberrypi.org/en/projects/editor-rpg/landing) Code Club project, for new Python coders.

<img width="1602" height="1833" alt="image" src="https://github.com/user-attachments/assets/0b81fea6-89a0-4476-adaa-14b6c300330f" />

This extension adds a somewhat more exciting graphical component to the original lesson plan, allowing learners to visually relate the programming concepts they are developing (namely, structured data formats, like Python dictionaries) to a real game world.

## How to use

The easiest way to use this extension is by simply copying the provided `main.py`, `game.py` and `gui.py` files into the Python Code Editor either at the [original lesson page](https://projects.raspberrypi.org/en/projects/editor-rpg/editor) or the [individual projects editor](https://editor.raspberrypi.org/en/projects/) website.

The changes to the original code are described below.

## Main.py 

### Changes

The following import statements are used at the top of `main.py` file to import the relevant graphics rendering functions from `gui.py`.

```python
from gui import setup, draw_all
from p5 import run
```
The following code is also added after the `rooms` dictionary definition:

```python
# A dictionary linking a room to other rooms
rooms = {
...
} # Existing rooms definition

############################################################# New code
class Player:

    def __init__(self, startingRoom, map):
        self.currentRoom = startingRoom
        self.map = rooms 
        self.inventory = [] # Empty
        self.health = 3 # 3 hearts

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
#############################################################
# Keep this to run the game loop from game.py 
currentRoom, inventory = run_game(player)
```
### Explanation

The `Player` class is necessary to allow changes in the game state caused by the code in `game.py` to carry over to changes in the visual output, handled by `gui.py`. Because the original function signature for `run_game()`,

```python
run_game(currentRoom, inventory, rooms)
```

treated the basic game state (`currentRoom`, `inventory`, `rooms`) as local variables inside the function's namespace, changes to these values could not be communicated to the code in `gui.py`. The `player` object therefore provides a globally accessible replacement, which code in both `gui.py` and `game.py` are able to reach.

### Implications

For pedagogical purposes, I think it is reasonable to essentially allow learners to "gloss over" this detail, as functionally speaking, from the point of view of `game.py`, the `player` object just ends up acting as a container object for the previous (`currentRoom`, `inventory`, `rooms`) variables, so `currentRoom -> player.currentRoom`, `inventory -> player.inventory` etc.

In a similar manner, `draw()` and `run()` should simply be treated as black-box functions that implement the graphical output, as they are beyond the scope of the lesson concepts.

## game.py

### Changes

As mentioned above, the change of the function signature for `run_game()` requires modifying any references to `currentRoom`, `inventory` and `rooms` in `game.py`, for `player.currentRoom`, `player.inventory` and `player.map`, i.e

```python
def run_game(currentRoom, inventory, rooms): # old
... 
```
becomes

```python
def run_game(player): # new
...
```

For convenience, these changes are already implemented in the provided `game.py` file, which is otherwise like the original (so it is possible to re-use the original lesson plan).

Alternatively, a more extensively re-worked version of `game.py` is provided in `game-alternative.py` (make sure to rename this to `game.py` in the Code Club editor if you wish to use it), which rearranges the original code in such a way as to (hopefully) make it easier for new learners to understand and add their own modifications to.





