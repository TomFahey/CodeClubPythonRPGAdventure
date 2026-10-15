"""Graphics: the emoji, the room tiles, and the map of the dungeon.

The game in game.py only needs two things from here, ``_showMap`` and
``_showInventory``, so a learner can ignore everything else in this file.

The names in ``icons`` are the item names a learner can use in their room
dictionary -- 'key', 'potion', 'sword' and so on.
"""

import random

import numpy as np

TILE_DTYPE = "U2"      # the widest glyph drawn is an emoji plus a selector
INVENTORY_SIZE = 5     # how many items the inventory bar has room for
ROOM_SIZES = (5, 7)    # the sizes a room may be given, in tiles
MAP_MARGIN = 4         # black tiles kept round the outside of the rooms

DIRECTIONS = ('north', 'south', 'east', 'west')

# Drawn in place of an item name that has no icon in the dictionary below.
UNKNOWN_ITEM = "\N{BLACK QUESTION MARK ORNAMENT}"


icons = {    
    ### Weapons
    "dagger" :          f"\N{DAGGER KNIFE}️",                    ### 🗡 
    "sword" :           "\U0001F5E1\U0000FE0F",                 ### 🗡️
    "shield" :          "\U0001F6E1\U0000FE0F",                 ### 🛡️
    "bow" :             f"\N{BOW AND ARROW}",                   ### 🏹
    "axe" :             f"\N{AXE}",                             ### 🪓
    "torch" :           f"\N{ELECTRIC TORCH}",                  ### 🔦
    ### Consumables
    "potion" :          f"\N{TEST TUBE}",                       ### 🧪
    "key" :             f"\N{KEY}️",                             ### 🔑
    "treasure" :        f"\N{MONEY BAG}",                       ### 💰
    ### Entities
    "player" :          f"\N{STANDING PERSON}",                 ### 🧍
    "monster" :         f"\N{JAPANESE OGRE}",                   ### 👹
    "vampire" :         f"\N{VAMPIRE}",                         ### 🧛
    "zombie" :          f"\N{ZOMBIE}",                          ### 🧟
    "ninja" :           f"\N{NINJA}",                           ### 🥷
    "spider" :          "\U0001F577\U0000FE0F",                 ### 🕷️
    "snake" :           f"\N{SNAKE}",                           ### 🐍
    "lizard" :          f"\N{LIZARD}",                          ### 🦎
    "bat" :             f"\N{BAT}",                             ### 🦇
    "harambe" :         f"\N{GORILLA}",                         ### 🦍
    "shark" :           f"\N{SHARK}",                           ### 🦈
    "crocodile" :       f"\N{CROCODILE}",                       ### 🐊
    ### Obstacles
    "lock" :            f"\N{LOCK}",                            ### 🔒
    "door" :            f"\N{DOOR}",                            ### 🚪
    ### Environment
    "wall" :            f"\N{BRICK}",                           ### 🧱
    "wallpaper" :       f"\N{LARGE BROWN SQUARE}",              ### 🟫
    "black_square" :    f"\N{BLACK LARGE SQUARE}",              ### ⬛
    "white_square" :    f"\N{WHITE LARGE SQUARE}",              ### ⬜
    "floor" :           "\U000025AA\U0000FE0F",                 ### ▪️
    ### Decorations
    "plant" :           f"\N{POTTED PLANT}",                    ### 🪴
    "statue" :          f"\N{MOYAI}",                           ### 🗿
    "cobweb" :          f"\N{SPIDER WEB}",                      ### 🕸️
    ### Miscellaneous
    "question_mark" :   f"\N{WHITE QUESTION MARK ORNAMENT}",    ### ❔
    "empty" :           f""                                     ### 

}

inventory_bar = r"""
■■■■▶ Inventory ◀■■■■
▫ {0} {1} {2} {3} {4} ▫
■■■■■■■■■■■■■■■■■■■■■■
"""

class Room:
    """One room of the dungeon.

    ``x`` is the column and ``y`` the row of the room's top-left corner, so a
    room further north has a smaller ``y``.
    """

    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.neighbours = {}   # direction -> Room
        self.items = []        # names of the items lying here
        self.visited = False

    @property
    def doors(self):
        """The directions this room has a doorway in."""
        return set(self.neighbours)

    def walls(self):
        """The one-cell wall around the edge of the room."""
        return np.pad(
            np.zeros((self.height - 2, self.width - 2)), 1, constant_values=1
        ) == 1

    def floor(self):
        """The inside of the room, where items and the player are drawn."""
        return np.logical_not(self.walls())

    def doorway(self, direction):
        """The wall cell that the doorway in ``direction`` is cut through."""

        if direction == 'north':
            return slice(0, 1), slice(self.width // 2, self.width // 2 + 1)
        elif direction == 'south':
            return slice(self.height - 1, self.height), slice(self.width // 2, self.width // 2 + 1)
        elif direction == 'east':
            return slice(self.height // 2, self.height // 2 + 1), slice(self.width - 1, self.width)
        elif direction == 'west':
            return slice(self.height // 2, self.height // 2 + 1), slice(0, 1)
        raise ValueError(f"unknown direction {direction!r}")

    def item_slots(self):
        """The cells an item can be drawn in, in a fixed order.

        The middle cell is left out, because that is where the player stands.
        """
        middle = (self.height // 2, self.width // 2)
        return [
            tuple(cell) for cell in np.argwhere(self.floor())
            if tuple(cell) != middle
        ]

    def room_tile(self):
        """This room drawn as its own small grid of glyphs."""
        tile = np.full((self.height, self.width), "", dtype=TILE_DTYPE)
        tile[self.walls()] = icons['wall']
        tile[self.floor()] = icons['floor']
        for direction in self.doors:
            tile[self.doorway(direction)] = icons['door']
        for cell, item in zip(self.item_slots(), self.items):
            tile[cell] = icons.get(item, UNKNOWN_ITEM)
        return tile

    @property
    def data(self):
        """This room drawn as its own small grid of glyphs."""
        return self.room_tile()

    @property
    def window(self):
        """The part of the whole map that this room fills."""
        return np.s_[self.y:self.y + self.height, self.x:self.x + self.width]

    @property
    def north(self):
        """The room to the north, or None."""
        return self.neighbours.get('north')

    @property
    def south(self):
        """The room to the south, or None."""
        return self.neighbours.get('south')

    @property
    def east(self):
        """The room to the east, or None."""
        return self.neighbours.get('east')

    @property
    def west(self):
        """The room to the west, or None."""
        return self.neighbours.get('west')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Room({self.name!r}, x={self.x}, y={self.y}, {self.width}x{self.height})"


class GameMap:
    """The whole dungeon: every room, already sized and placed.

    Build one straight from the room dictionary in main.py::

        game_map = GameMap(rooms)
        print(game_map)
    """

    def __init__(self, rooms, seed=None):
        self.rooms = self.parse(rooms, seed)
        self.current_room = next(iter(self.rooms.values()))

    def parse(self, rooms, seed=None):
        """Work out how big each room is and where it goes.

        Two rooms joined north/south have to be the same width, and two rooms
        joined east/west the same height -- otherwise the wall between them
        would not line up.  So widths and heights are worked out separately:
        every group of rooms that has to match is given one size, and the whole
        group shares it.  That keeps the sizes agreeing whether the rooms form a
        tree or a circle.
        """
        # The same dungeon always gets the same sizes, so a redraw never changes
        # the map underfoot.  The seed is a number worked out from the room
        # names, because `random.seed` on the target editor handles a number but
        # may not manage a string.
        if seed is None:
            seed = sum(ord(character) for character in ''.join(sorted(rooms)))
        random.seed(seed)

        for name, room in rooms.items():
            for way in DIRECTIONS:
                there = room.get(way)
                if there is not None and there not in rooms:
                    raise ValueError(
                        f"room '{name}' says '{there}' is to the {way}, but there "
                        f"is no room called '{there}'"
                    )

        def groups(ways):
            """The rooms that can reach each other using these exits."""
            found, seen = [], set()
            for name in rooms:
                if name in seen:
                    continue
                group, to_visit = [], [name]
                seen.add(name)
                while to_visit:
                    here = to_visit.pop()
                    group.append(here)
                    for way in ways:
                        there = rooms[here].get(way)
                        if there is not None and there not in seen:
                            seen.add(there)
                            to_visit.append(there)
                found.append(group)
            return found

        # 1. North/south neighbours have to share a width, so one width is given
        #    to each group of rooms joined that way...
        widths = {}
        for group in groups(('north', 'south')):
            width = random.choice(ROOM_SIZES)
            for name in group:
                widths[name] = width

        #    ...and one height to each group of rooms joined east/west.
        heights = {}
        for group in groups(('east', 'west')):
            height = random.choice(ROOM_SIZES)
            for name in group:
                heights[name] = height

        # 2. Walk the map from the first room, standing each neighbour against
        #    the wall it shares with the room we came from.
        start = next(iter(rooms))
        spots = {start: (0, 0)}
        to_visit = [start]
        while to_visit:
            here = to_visit.pop(0)
            x, y = spots[here]
            for way in DIRECTIONS:
                there = rooms[here].get(way)
                if there is None or there in spots:
                    continue
                there_width, there_height = widths[there], heights[there]
                if way == 'north':
                    spots[there] = (x, y - there_height + 1)
                elif way == 'south':
                    spots[there] = (x, y + heights[here] - 1)
                elif way == 'east':
                    spots[there] = (x + widths[here] - 1, y)
                elif way == 'west':
                    spots[there] = (x - there_width + 1, y)
                to_visit.append(there)

        unreachable = [name for name in rooms if name not in spots]
        if unreachable:
            raise ValueError(
                f"{unreachable} cannot be reached from '{start}'; every room "
                f"needs an exit joining it to the rest of the map"
            )

        # 3. Move the map into place: first so its top-left corner is at (0, 0),
        #    then so the first room -- the one the player starts in -- sits in
        #    the middle of a bigger map, with a border of black tiles round the
        #    rooms.
        left = min(x for x, _ in spots.values())
        top = min(y for _, y in spots.values())
        spots = {name: (x - left, y - top) for name, (x, y) in spots.items()}

        span_x = max(x + widths[name] for name, (x, _) in spots.items())
        span_y = max(y + heights[name] for name, (_, y) in spots.items())
        middle_x = spots[start][0] + widths[start] // 2
        middle_y = spots[start][1] + heights[start] // 2

        self.cols = max(2 * max(middle_x, span_x - middle_x) + 1, span_x + 2 * MAP_MARGIN)
        self.rows = max(2 * max(middle_y, span_y - middle_y) + 1, span_y + 2 * MAP_MARGIN)
        spots = {
            name: (x + self.cols // 2 - middle_x, y + self.rows // 2 - middle_y)
            for name, (x, y) in spots.items()
        }

        # 4. Build the rooms, then link each one to the rooms next door.
        built = {}
        for name, room in rooms.items():
            x, y = spots[name]
            built[name] = Room(name, x, y, widths[name], heights[name])
            if 'item' in room:
                built[name].items.append(room['item'])
            built[name].visited = room.get('visited', False)

        for name, room in rooms.items():
            neighbours = {}
            for way in DIRECTIONS:
                there = room.get(way)
                if there is not None:
                    neighbours[way] = built[there]
            built[name].neighbours = neighbours

        return built

    def render(self, current_room=None):
        """Draw the whole map, hiding the rooms not visited yet.

        Everything starts out black -- the tiles outside the rooms as well as
        the rooms not found yet -- so the player sees themselves in the middle
        of an unexplored map.  A cell stays visible if any room covering it has
        been visited, so the wall shared with a room next door is not blocked
        out.
        """
        if current_room is None:
            current_room = self.current_room
        rows, cols = self.rows, self.cols
        map_data = np.full((rows, cols), icons['black_square'], dtype=TILE_DTYPE)
        owner = np.full((rows, cols), -1, dtype=int)
        found = np.zeros((rows, cols), dtype=bool)

        for index, room in enumerate(self.rooms.values()):
            map_data[room.window] = room.data
            owner[room.window] = index
            # The room the player is standing in is always on show anyway.
            if room.visited or room is current_room:
                found[room.window] = True

        map_data[current_room.y + current_room.height // 2,
                 current_room.x + current_room.width // 2] = icons['player']

        return np.ma.MaskedArray(
            map_data,
            mask=(owner >= 0) & ~found,
            fill_value=icons['black_square'],
        )

    @property
    def map_array(self):
        return self.render(self.current_room)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.map_array.filled(icons['black_square'])])

    def __repr__(self):
        return f"GameMap({len(self.rooms)} rooms, {self.cols}x{self.rows})"


def _showInventory(inventory):
    """Draw the inventory bar.  ``inventory`` holds the names of items picked up.

    This is one of the two calls game.py needs.
    """
    picked_up = [icons.get(item, UNKNOWN_ITEM) for item in inventory[:INVENTORY_SIZE]]
    picked_up += [icons['white_square']] * (INVENTORY_SIZE - len(picked_up))
    print(inventory_bar.format(*picked_up))

def _showRoom(currentRoom, rooms):
    """Draw the current room in isolation."""
    game_map = GameMap(rooms)
    current_room = game_map.rooms[currentRoom]
    data = current_room.data
    data[current_room.height // 2][current_room.width // 2] = icons['player']
    for row in data:
        print(''.join(row))


def _showMap(currentRoom, rooms):
    """Draw the whole dungeon.  This is the other call game.py needs."""
    game_map = GameMap(rooms)
    game_map.current_room = game_map.rooms[currentRoom]
    for row in game_map.render().filled(icons['black_square']):
        print(''.join(row))
