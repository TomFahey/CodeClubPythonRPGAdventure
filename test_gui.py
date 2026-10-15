"""Tests for the graphics library in gui.py.

Run them from the project folder with::

    python -m unittest -v

These are for whoever is working on gui.py, not for the children -- the games
they write are checked by playing them.
"""

import contextlib
import io
import unittest

import gui
from gui import DIRECTIONS, INVENTORY_SIZE, ROOM_SIZES, GameMap, Room, _showInventory

OPPOSITE = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}

# The dungeon from main.py, copied here because importing main.py would start
# the game and wait for someone to type at it.
DUNGEON = {
    'Hall': {'south': 'Kitchen', 'east': 'Dining Room', 'west': 'Office', 'item': 'key'},
    'Kitchen': {'north': 'Hall', 'item': 'monster'},
    'Dining Room': {'west': 'Hall', 'south': 'Garden', 'item': 'potion'},
    'Garden': {'north': 'Dining Room', 'south': 'Garage'},
    'Garage': {'north': 'Garden'},
    'Office': {'east': 'Hall'},
}

# Four rooms in a square, each touching the other three: a hollow loop.
RING = {
    'A': {'east': 'B', 'south': 'D'},
    'B': {'west': 'A', 'south': 'C'},
    'C': {'north': 'B', 'west': 'D'},
    'D': {'north': 'A', 'east': 'C'},
}

# A loop with a room hanging off it, and a plain open corridor.
RING_AND_TAIL = {
    'A': {'east': 'B', 'south': 'D'},
    'B': {'west': 'A', 'south': 'C', 'east': 'E'},
    'C': {'north': 'B', 'west': 'D'},
    'D': {'north': 'A', 'east': 'C'},
    'E': {'west': 'B'},
}
CORRIDOR = {
    'P': {'east': 'Q'},
    'Q': {'west': 'P', 'south': 'R'},
    'R': {'north': 'Q'},
}


def doorway_cell(room, direction):
    """Where a room's doorway sits in the room itself, as (row, column)."""
    if direction == 'north':
        return 0, room.width // 2
    elif direction == 'south':
        return room.height - 1, room.width // 2
    elif direction == 'west':
        return room.height // 2, 0
    elif direction == 'east':
        return room.height // 2, room.width - 1
    raise ValueError(f"unknown direction {direction!r}")


def absolute_doorway(room, direction):
    """Where a room's doorway sits on the whole map, as (row, column)."""
    row, column = doorway_cell(room, direction)
    return room.y + row, room.x + column


def overlapping_pairs(rooms):
    """Pairs of rooms standing on each other rather than just touching."""
    found = []
    for index, first in enumerate(rooms):
        for second in rooms[index + 1:]:
            across = min(first.x + first.width, second.x + second.width) - max(first.x, second.x)
            down = min(first.y + first.height, second.y + second.height) - max(first.y, second.y)
            if across >= 2 and down >= 2:
                found.append((first.name, second.name))
    return found


def inventory_bar_for(items):
    """The inventory bar _showInventory would print for these item names."""
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        _showInventory(items)
    return printed.getvalue()


class RoomTests(unittest.TestCase):
    def test_a_room_is_drawn_at_its_own_size(self):
        room = Room('Hall', x=3, y=4, width=7, height=5)
        self.assertEqual(room.data.shape, (5, 7))

    def test_the_walls_run_round_the_edge(self):
        room = Room('Hall', 0, 0, 5, 5)
        walls = room.walls()
        self.assertTrue(walls[0].all())
        self.assertTrue(walls[-1].all())
        self.assertTrue(walls[:, 0].all())
        self.assertTrue(walls[:, -1].all())
        self.assertFalse(walls[2, 2])

    def test_the_floor_is_everything_inside_the_walls(self):
        room = Room('Hall', 0, 0, 5, 5)
        self.assertFalse((room.walls() & room.floor()).any())
        self.assertTrue((room.walls() | room.floor()).all())

    def test_every_doorway_is_cut_into_a_wall(self):
        room = Room('Hall', 0, 0, 7, 5)
        for direction in DIRECTIONS:
            with self.subTest(direction=direction):
                self.assertTrue(room.walls()[room.doorway(direction)])

    def test_a_rooms_window_matches_where_it_sits(self):
        room = Room('Hall', x=3, y=4, width=7, height=5)
        self.assertEqual(room.window, (slice(4, 9), slice(3, 10)))

    def test_item_slots_are_inside_the_room_but_not_the_middle(self):
        room = Room('Hall', 0, 0, 7, 5)
        slots = room.item_slots()
        self.assertNotIn((2, 3), slots)          # the middle, where the player stands
        self.assertEqual(len(slots), 3 * 5 - 1)  # the whole floor, less the middle
        for slot in slots:
            with self.subTest(slot=slot):
                self.assertTrue(room.floor()[slot])


class SizingTests(unittest.TestCase):
    def test_rooms_that_touch_agree_on_the_size_they_share(self):
        for config in (DUNGEON, RING, RING_AND_TAIL, CORRIDOR):
            built = GameMap(config).rooms
            for room in built.values():
                for way, other in room.neighbours.items():
                    with self.subTest(config=sorted(config), room=room.name, way=way):
                        if way in ('north', 'south'):
                            self.assertEqual(room.width, other.width)
                        else:
                            self.assertEqual(room.height, other.height)

    def test_every_size_is_one_of_the_allowed_choices(self):
        for name, room in GameMap(RING).rooms.items():
            with self.subTest(name=name):
                self.assertIn(room.width, ROOM_SIZES)
                self.assertIn(room.height, ROOM_SIZES)

    def test_the_same_dungeon_always_looks_the_same(self):
        # This is what lets the map be redrawn every time the player types
        # 'map' without the rooms changing size underneath them.
        first, second = GameMap(DUNGEON), GameMap(DUNGEON)
        self.assertEqual(
            {name: (r.x, r.y, r.width, r.height) for name, r in first.rooms.items()},
            {name: (r.x, r.y, r.width, r.height) for name, r in second.rooms.items()},
        )

    def test_a_different_seed_can_give_different_sizes(self):
        sizes = {
            GameMap(RING, seed=seed).rooms['A'].width
            for seed in range(50)
        }
        self.assertEqual(sizes, set(ROOM_SIZES))

    def test_the_map_is_larger_than_the_rooms_inside_it(self):
        for config in (DUNGEON, RING, RING_AND_TAIL):
            game_map = GameMap(config)
            rooms = list(game_map.rooms.values())
            span_x = max(room.x + room.width for room in rooms)
            span_y = max(room.y + room.height for room in rooms)
            with self.subTest(config=sorted(config)):
                self.assertGreater(game_map.cols, span_x)
                self.assertGreater(game_map.rows, span_y)
                self.assertGreater(min(room.x for room in rooms), 0)
                self.assertGreater(min(room.y for room in rooms), 0)

    def test_the_first_room_sits_in_the_middle_of_the_map(self):
        # The player starts in the first room, and should see themselves in the
        # middle of a map of black tiles rather than jammed into a corner.
        for config in (DUNGEON, RING, RING_AND_TAIL, CORRIDOR):
            game_map = GameMap(config)
            first = next(iter(game_map.rooms.values()))
            with self.subTest(config=sorted(config)):
                self.assertLessEqual(
                    abs(first.x + first.width // 2 - game_map.cols // 2), 1)
                self.assertLessEqual(
                    abs(first.y + first.height // 2 - game_map.rows // 2), 1)


class GeometryTests(unittest.TestCase):
    def test_neighbours_stand_against_the_wall_they_share(self):
        for config in (DUNGEON, RING, RING_AND_TAIL, CORRIDOR):
            built = GameMap(config).rooms
            for room in built.values():
                for way, other in room.neighbours.items():
                    with self.subTest(config=sorted(config), room=room.name, way=way):
                        if way == 'east':
                            expected = (room.x + room.width - 1, room.y)
                        elif way == 'west':
                            expected = (room.x - (other.width - 1), room.y)
                        elif way == 'south':
                            expected = (room.x, room.y + room.height - 1)
                        else:
                            expected = (room.x, room.y - (other.height - 1))
                        self.assertEqual((other.x, other.y), expected)

    def test_a_shared_doorway_is_the_same_cell_in_both_rooms(self):
        for config in (DUNGEON, RING, RING_AND_TAIL, CORRIDOR):
            built = GameMap(config).rooms
            for room in built.values():
                for way, other in room.neighbours.items():
                    with self.subTest(config=sorted(config), room=room.name, way=way):
                        self.assertEqual(
                            absolute_doorway(room, way),
                            absolute_doorway(other, OPPOSITE[way]),
                        )
                        self.assertEqual(room.data[doorway_cell(room, way)], gui.icons['door'])

    def test_no_two_rooms_ever_stand_on_each_other(self):
        for config in (DUNGEON, RING, RING_AND_TAIL, CORRIDOR):
            for seed in range(100):
                rooms = list(GameMap(config, seed=seed).rooms.values())
                with self.subTest(config=sorted(config), seed=seed):
                    self.assertEqual(overlapping_pairs(rooms), [])

    def test_no_two_rooms_disagree_about_a_cell_they_share(self):
        # This is what makes it safe to draw the rooms over each other in turn.
        rooms = GameMap(DUNGEON).rooms
        seen = {}
        for room in rooms.values():
            for row in range(room.height):
                for column in range(room.width):
                    cell = (room.y + row, room.x + column)
                    glyph = room.data[row, column]
                    with self.subTest(room=room.name, cell=cell):
                        self.assertEqual(seen.setdefault(cell, glyph), glyph)


class ValidationTests(unittest.TestCase):
    def test_a_mistyped_room_name_is_reported(self):
        with self.assertRaises(ValueError) as caught:
            GameMap({'Hall': {'north': 'Kitchne'}})
        self.assertIn('Kitchne', str(caught.exception))

    def test_a_room_that_cannot_be_reached_is_reported(self):
        config = {'Hall': {'north': 'Kitchen'}, 'Kitchen': {'south': 'Hall'}, 'Cellar': {}}
        with self.assertRaises(ValueError) as caught:
            GameMap(config)
        self.assertIn('Cellar', str(caught.exception))


class GameMapTests(unittest.TestCase):
    def test_a_room_with_no_item_has_nothing_in_it(self):
        rooms = GameMap(DUNGEON).rooms
        self.assertEqual(rooms['Garden'].items, [])
        self.assertEqual(rooms['Hall'].items, ['key'])

    def test_a_room_counts_as_unvisited_unless_the_dictionary_says_otherwise(self):
        rooms = GameMap(DUNGEON).rooms
        self.assertFalse(rooms['Hall'].visited)

        rooms = GameMap({**DUNGEON, 'Hall': {**DUNGEON['Hall'], 'visited': True}}).rooms
        self.assertTrue(rooms['Hall'].visited)

    def test_a_room_knows_the_rooms_next_door(self):
        rooms = GameMap(DUNGEON).rooms
        self.assertIs(rooms['Hall'].south, rooms['Kitchen'])
        self.assertIs(rooms['Hall'].east, rooms['Dining Room'])
        self.assertIsNone(rooms['Hall'].north)
        self.assertEqual(rooms['Hall'].doors, {'south', 'east', 'west'})

    def test_the_picture_is_as_big_as_the_map(self):
        game_map = GameMap(DUNGEON)
        self.assertEqual(game_map.render().shape, (game_map.rows, game_map.cols))

    def test_the_tiles_round_the_outside_are_black(self):
        game_map = GameMap(DUNGEON)
        picture = game_map.render()
        corners = [(0, 0), (0, game_map.cols - 1),
                   (game_map.rows - 1, 0), (game_map.rows - 1, game_map.cols - 1)]
        for cell in corners:
            with self.subTest(cell=cell):
                self.assertEqual(picture.data[cell], gui.icons['black_square'])

    def test_no_cell_is_left_empty(self):
        # A cell holding an empty string vanishes when the row is joined into a
        # printable line, which leaves the map looking ragged and out of line.
        for config in (DUNGEON, RING):
            picture = GameMap(config).render().filled()
            with self.subTest(config=sorted(config)):
                self.assertFalse((picture == '').any())

    def test_rooms_not_visited_yet_are_hidden(self):
        game_map = GameMap(DUNGEON)
        game_map.rooms['Hall'].visited = True
        picture = game_map.render()
        for name, room in game_map.rooms.items():
            inside = (slice(room.y + 1, room.y + room.height - 1),
                      slice(room.x + 1, room.x + room.width - 1))
            with self.subTest(name=name):
                if room.visited:
                    self.assertFalse(picture.mask[inside].any())
                else:
                    self.assertTrue(picture.mask[inside].all())

    def test_the_wall_shared_with_a_visited_room_stays_visible(self):
        game_map = GameMap(DUNGEON)
        game_map.rooms['Hall'].visited = True
        picture = game_map.render()
        shared = absolute_doorway(game_map.rooms['Hall'], 'south')
        self.assertFalse(picture.mask[shared])

    def test_the_player_is_drawn_where_they_are(self):
        game_map = GameMap(DUNGEON)
        hall = game_map.rooms['Hall']
        game_map.current_room = hall
        picture = game_map.render()
        self.assertEqual(
            picture[hall.y + hall.height // 2, hall.x + hall.width // 2],
            gui.icons['player'],
        )


class InventoryTests(unittest.TestCase):
    def test_the_bar_has_room_for_five_items_and_starts_empty(self):
        bar = inventory_bar_for([])
        self.assertIn(gui.icons['white_square'] * INVENTORY_SIZE, bar.replace(' ', ''))

    def test_item_names_are_matched_to_their_icons(self):
        bar = inventory_bar_for(['key', 'sword'])
        self.assertIn(gui.icons['key'], bar)
        self.assertIn(gui.icons['sword'], bar)

    def test_a_name_with_no_icon_still_shows_something(self):
        bar = inventory_bar_for(['banana'])
        self.assertIn(gui.UNKNOWN_ITEM, bar)

    def test_only_the_first_few_items_are_shown(self):
        bar = inventory_bar_for(['key'] * (INVENTORY_SIZE + 3))
        self.assertEqual(bar.count(gui.icons['key']), INVENTORY_SIZE)


if __name__ == "__main__":
    unittest.main()
