"""Graphics for the dungeon, using nothing but the standard library.

A stand-in for gui.py for places that have no numpy -- the editor on
projects.raspberrypi.org, for instance, which runs Python 3.7 and has no
third-party packages at all.  It offers the same things gui.py does, so game.py
only has to change which one it imports:

    from gui_pure import _showMap, _showInventory

The map is held as lists of lists of strings instead of a numpy array.  As a
bonus no glyph is ever cut short to fit a fixed-width cell, which numpy's
two-code-point tile dtype insisted on.

The editor there also has only a cut-down standard library: it provides
`random.seed` and `random.choice`, but not `random.Random`.  So this file
imports `random` and nothing else.
"""

import random as ran


INVENTORY_SIZE = 5     # how many items the inventory bar has room for
ROOM_SIZES = (5, 7)    # the sizes a room may be given, in tiles
MAP_MARGIN = 4         # black tiles kept round the outside of the rooms

DIRECTIONS = ('north', 'south', 'east', 'west')

# Drawn in place of an item name that has no icon in the dictionary below.
UNKNOWN_ITEM = "\U00002753"    # ❓

icons = {
    ### Weapons
    "dagger" :          "\U0001F5E1\U0000FE0F",                 ### 🗡 
    "sword" :           "\U0001F5E1\U0000FE0F",                 ### 🗡️
    "shield" :          "\U0001F6E1\U0000FE0F",                 ### 🛡️
    "bow" :             "\U0001F3F9",                           ### 🏹
    "axe" :             "\U0001FA93",                           ### 🪓
    "torch" :           "\U0001F526",                           ### 🔦
    ### Consumables
    "potion" :          "\U0001F9EA",                           ### 🧪
    "key" :             "\U0001F511\U0000FE0F",                 ### 🔑
    "treasure" :        "\U0001F4B0",                           ### 💰
    ### Entities
    "player" :          "\U0001F9CD",                           ### 🧍
    "monster" :         "\U0001F479",                           ### 👹
    "vampire" :         "\U0001F9DB",                           ### 🧛
    "zombie" :          "\U0001F9DF",                           ### 🧟
    "ninja" :           "\U0001F977",                           ### 🥷
    "spider" :          "\U0001F577\U0000FE0F",                 ### 🕷️
    "snake" :           "\U0001F40D",                           ### 🐍
    "lizard" :          "\U0001F98E",                           ### 🦎
    "bat" :             "\U0001F987",                           ### 🦇
    "harambe" :         "\U0001F98D",                           ### 🦍
    "shark" :           "\U0001F988",                           ### 🦈
    "crocodile" :       "\U0001F40A",                           ### 🐊
    ### Obstacles
    "lock" :            "\U0001F512",                           ### 🔒
    "door" :            "\U0001F6AA",                           ### 🚪
    ### Environment
    "wall" :            "\U0001F9F1",                           ### 🧱
    "wallpaper" :       "\U0001F7EB",                           ### 🟫
    "black_square" :    "\U00002B1B",                           ### ⬛
    "white_square" :    "\U00002B1C",                           ### ⬜
    "floor" :           " ",                 ### ▪️
    ### Decorations
    "plant" :           "\U0001FAB4",                           ### 🪴
    "statue" :          "\U0001F5FF",                           ### 🗿
    "cobweb" :          "\U0001F578",                           ### 🕸️
    ### Miscellaneous
    "question_mark" :   "\U00002754",                           ### ❔
    "empty" :           "",                                     ### 

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
        """A grid that is True wherever the wall runs round the edge."""
        return [
            [row == 0 or row == self.height - 1
             or column == 0 or column == self.width - 1
             for column in range(self.width)]
            for row in range(self.height)
        ]

    def floor(self):
        """A grid that is True for the inside of the room."""
        return [[not wall for wall in wall_row] for wall_row in self.walls()]

    def doorway(self, direction):
        """The single wall cell the doorway in ``direction`` is cut through."""
        if direction == 'north':
            return 0, self.width // 2
        elif direction == 'south':
            return self.height - 1, self.width // 2
        elif direction == 'east':
            return self.height // 2, self.width - 1
        elif direction == 'west':
            return self.height // 2, 0
        raise ValueError(f"unknown direction {direction!r}")

    def item_slots(self):
        """The cells an item can be drawn in, in a fixed order.

        The middle cell is left out, because that is where the player stands.
        """
        inside = self.floor()
        middle = (self.height // 2, self.width // 2)
        return [
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if inside[row][column] and (row, column) != middle
        ]

    def room_tile(self):
        """This room drawn as its own small grid of glyphs."""
        walls = self.walls()
        # Tile wall and floor areas with their respective icons
        tile = [
            [icons['wall'] if walls[row][column] else icons['floor']
             for column in range(self.width)]
            for row in range(self.height)
        ]
        # Tile doorways with the door icon
        for direction in self.doors:
            row, column = self.doorway(direction)
            tile[row][column] = icons['door']
        slots = self.item_slots()
        # Tile items with their respective icons
        for item in self.items:
            # Pseudo-random placement of item based on its name
            index = sum(ord(c) for c in item) % len(slots)
            row, column = slots.pop(index)
            tile[row][column] = icons.get(item, UNKNOWN_ITEM)
        return tile

    @property
    def data(self):
        """This room drawn as its own small grid of glyphs."""
        return self.room_tile()

    @property
    def window(self):
        """Where this room sits on the map, as (top, left, bottom, right)."""
        return self.y, self.x, self.y + self.height, self.x + self.width

    def draw_onto(self, map_data):
        """Copy this room's glyphs onto the map grid."""
        top, left, bottom, right = self.window
        tile = self.data
        for row in range(top, bottom):
            for column in range(left, right):
                map_data[row][column] = tile[row - top][column - left]

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
        ran.seed(seed)

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
            width = ran.choice(ROOM_SIZES)
            for name in group:
                widths[name] = width

        #    ...and one height to each group of rooms joined east/west.
        heights = {}
        for group in groups(('east', 'west')):
            height = ran.choice(ROOM_SIZES)
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
        """Draw the whole map, with everything not found yet left black.

        Starting from black means the tiles outside the rooms and the rooms not
        visited yet come out the same, so the player sees themselves in the
        middle of an unexplored map.  A room is shown if the player has been in
        it, or is standing in it now.
        """
        if current_room is None:
            current_room = self.current_room
        map_data = [[icons['black_square']] * self.cols for _ in range(self.rows)]

        for room in self.rooms.values():
            if room.visited or room is current_room:
                room.draw_onto(map_data)

        map_data[current_room.y + current_room.height // 2][
            current_room.x + current_room.width // 2] = icons['player']

        return map_data

    @property
    def map_array(self):
        """The map as a plain grid of glyphs.  The same as render()."""
        return self.render()

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.map_array])

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
    return game_map.render()
