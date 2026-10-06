game_map = """
🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫
🟫     Hall   🟫   Dining Room  🟫
🪟{Hall:^12s}🚪{Dining Room:^16s}🟫
🟫            🟫                🟫
🟫            🟫                🟫
🟫🟫🟫🚪🟫🟫🟫🟫🟫🟫🟫🚪🟫🟫🟫🟫🟫
🟫   Kitchen  🟫        Garden
🟫{Kitchen:^12s}🟫🥬🟩🟩{Garden}🟩🌳🟩🟩🟩🟩
🟫            🟫🥬🟩🌳🟩🟩🟩🌳🟩🟩
🟫            🟫🥬🟩🟩🟩🌳🟩🟩🟩🟩
🟫🟫🟫🟫🟫🟫🟫🟫🥬🟩🟩🟩🟩🟩🟩🌳🟩
"""

icons = {
    "key" : "🗝️",
    "dagger" : "🗡️",
    "sword" : "🗡️",
    "shield" : "🛡️",
    "potion" : "🧪",
    "bow" : "🏹",
    "axe" : "🪓",
    "player" : "🧍 ",
    "monster" : " 👹 ",
    "treasure" : "💰",
    "door" : "🚪",
    "wall" : "🧱",
    "wallpaper" : "🟫",
    "black_square" : "⬛",
    "white_square" : "⬜",
    "bar" : "░",
    "empty" : " "
}

inventory_bar = r"""
■■■■▶ Inventory ◀■■■■
▫ {0} {1} {2} {3} {4} ▫
■■■■■■■■■■■■■■■■■■■■■■
"""

def _showMap(currentRoom, rooms):
    room_names = list(rooms.keys())
    player_icon = {
        room: icons["empty"] for room in room_names
    } 
    player_icon[currentRoom] = icons["player"]
    print(game_map.format(**player_icon))

def _showInventory(inventory):
    print(inventory_bar.format(*inventory))