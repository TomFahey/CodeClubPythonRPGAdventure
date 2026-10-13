import numpy as np
from main import rooms

room_map = """
🧱🧱🧱🧱🧱{N}🧱🧱🧱🧱
🧱                    🧱
🧱                    🧱
🧱                    🧱
{W}⠀       🧍         {E}
🧱                    🧱
🧱                    🧱
🧱                    🧱
🧱🧱🧱🧱{S}🧱🧱🧱🧱🧱

{name:^25}
"""
# print(room_map.format(**(room_pos['Office'].info)))


"""
🧱🧱🧱🧱🧱🧱🧱🧱🧱
🧱🟫🟫🟫🧱🟫🟫🟫🧱
🧱🟫🟫🟫🧱🟫🟫🟫🧱
🧱🟫🟫🟫🧱🟫🟫🟫🧱
🧱🧱🚪🧱🧱🧱🚪🧱🧱
🧱🟫🟫🟫🧱🟫🟫🟫🧱
🚪🟫🟫🟫🚪🟫🟫🟫🧱
🧱🟫🟫🟫🧱🟫🟫🟫🧱
🧱🧱🧱🧱🧱🧱🧱🧱🧱
"""

walls = np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]]) == 1
floor = np.logical_not(walls)
door_north = np.array([[0,0,1,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]) == 1
door_south = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0]]) == 1
door_west = np.array([[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]) == 1
door_east = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0]]) == 1




room_template = """
🧱🧱{N}🧱🧱
🧱▪️▪️▪️🧱
{W}▪️▪️▪️{E}
🧱▪️▪️▪️🧱
🧱🧱{S}🧱🧱
"""

game_array = np.array([
    ["🧱" for i in range(10)] + [" " for i in range(12)], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱"] + [" " for i in range(20)] + ["🧱"], # 25 width, 20 internal
    ["🧱" for i in range(10)] + [" " for i in range(12)], # 25 width, 20 internal
])

icons = {
    "key" :             f"\N{KEY}️",                 ### 🔑
    "dagger" :          f"\N{DAGGER KNIFE}️",        ### 🗡 
    "sword" :           "\U0001F5E1\U0000FE0F",     ### 🗡️
    "shield" :          "\U0001F6E1\U0000FE0F",     ### 🛡️
    "potion" :          f"\N{TEST TUBE}",           ### 🧪
    "bow" :             f"\N{BOW AND ARROW}",       ### 🏹
    "axe" :             f"\N{AXE}",                 ### 🪓
    "player" :          f"\N{STANDING PERSON}",     ### 🧍
    "monster" :         f"\N{JAPANESE OGRE}",       ### 👹
    "treasure" :        f"\N{MONEY BAG}",           ### 💰
    "door" :            f"\N{DOOR}",                ### 🚪
    "wall" :            f"\N{BRICK}",               ### 🧱
    "wallpaper" :       f"\N{LARGE BROWN SQUARE}",  ### 🟫
    "black_square" :    f"\N{BLACK LARGE SQUARE}",  ### ⬛
    "white_square" :    f"\N{WHITE LARGE SQUARE}",  ### ⬜
    "lock" :            f"\N{LOCK}",                ### 🔒
    "floor" :           "\U000025AA\U0000FE0F",     ### ▪️
    "empty" :           f""                         ### 

}

inventory_bar = r"""
■■■■▶ Inventory ◀■■■■
▫ {0} {1} {2} {3} {4} ▫
■■■■■■■■■■■■■■■■■■■■■■
"""

def _showMap(currentRoom, rooms):
    #room_names = list(rooms.keys())
    #player_icon = {
    #    room: icons["empty"] for room in room_names
    #} 
    #player_icon[currentRoom] = icons["player"]
    print(game_map.format(**rooms))

def _showInventory(inventory):
    print(inventory_bar.format(*inventory))


class Room:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.info = {
            "N" : icons['wall'], 
            "S" : icons['wall'], 
            "E" : icons['wall'], 
            "W" : icons['wall'], 
            'name': name
        }

    def __str__(self):
        return f"Coord(x={self.x}, y={self.y})"

def parse(room_dictionary):
    x, y = 0, 0
    visited = set()
    room_positions = {name: Room(name, 0,0) for name in room_dictionary}
    for name, directions in room_dictionary.items():
        for key,val in directions.items():
            if val not in visited:
                match key:
                    case 'south':
                        room_positions[val].x = room_positions[name].x
                        room_positions[val].y = room_positions[name].y - 1
                        room_positions[val].info["N"] = icons['door']
                        room_positions[name].info["S"] = icons['door']
                    case 'north':
                        room_positions[val].x = room_positions[name].x
                        room_positions[val].y = room_positions[name].y + 1
                        room_positions[val].info["S"] = icons['door']
                        room_positions[name].info["N"] = icons['door']
                    case 'east':
                        room_positions[val].y = room_positions[name].y
                        room_positions[val].x = room_positions[name].x + 1
                        room_positions[val].info["W"] = icons['door']
                        room_positions[name].info["E"] = icons['door']
                    case 'west':
                        room_positions[val].y = room_positions[name].y
                        room_positions[val].x = room_positions[name].x - 1
                        room_positions[val].info["E"] = icons['door']
                        room_positions[name].info["W"] = icons['door']
                    case _:
                        pass
        visited.add(name)
    return room_positions
                    


p = {
    'Hall': {
        'x': 0,
        'y': 0, 
    },
    'Kitchen': {
        'x': 0,
        'y': -1, 
    },
    'Dining Room': {
        'x': 1,
        'y': 0
    },
    'Garden': {
        'x': 0,
        'y': -1
    },
    'Garage': {
        'x': 0,
        'y': -2,
    },
    'Office': {
        'x': -1,
        'y': 0,
    }
}

def generate_world_map(rooms, world_size=30):
    room_positions = parse(rooms)
    world_map_mask = np.ones((world_size,world_size))
    world_map_data = np.zeros((world_size,world_size), dtype='U2')
    room_templates = []
    for room in room_positions.values():
        x, y = room.x, room.y
        room_template = np.zeros((5,5), dtype='U2')
        room_template[walls] = icons['wall']
        room_template[floor] = icons['floor']
        room_template[door_north] = room.info['N']
        room_template[door_south] = room.info['S']
        room_template[door_east] = room.info['E']
        room_template[door_west] = room.info['W']
        pad_width = ((world_size-5)//2, (world_size-5)//2 + 1) if (world_size % 2) else (world_size // 2)
        room_template = np.pad(room_template,((world_size-5)//2, (world_size-5)//2 + 1),mode='empty')
        room_template = np.roll(room_template, shift=(4*x, -4*y), axis=(1,0))
        room_templates.append((room, room_template))
        room_template_prime = room_template.view(np.uint32)
        world_map_prime = world_map_data.view(np.uint32)
        world_map_data = np.bitwise_or(world_map_prime, room_template_prime).view('U2')
    world_map = np.ma.MaskedArray(data=world_map_data, mask=world_map_mask, fill_value='⬛')
    return world_map, room_templates


world_map, room_templates = generate_world_map(rooms)
#world_map.mask[world_map.data!=''] = 0
world_map.mask = 0
[print(''.join(i)) for i in world_map.filled('⬛')];

#[print(''.join(i)) for i in world_map.filled('⬛')];