import sys

SIZE = 0
world = []
agent_pos = [0, 0]
has_gold = False
wumpus_alive = True
bump_flag = False
scream_flag = False
kb = []
processed_percepts = {}

def neighbors(x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            yield nx, ny

def init_kb(size):
    global kb, processed_percepts, SIZE
    SIZE = size
    kb = [[{
        'pit': 'unknown',
        'wumpus': 'unknown',
        'pit_count': 0,
        'wumpus_count': 0,
        'safe': False,
        'visited': False
    } for _ in range(size)] for _ in range(size)]
    processed_percepts = {}
    ax, ay = agent_pos
    kb[ax][ay]['safe'] = True
    kb[ax][ay]['pit'] = 'no'
    kb[ax][ay]['wumpus'] = 'no'

def create_world(size):
    global world
    world = [["" for _ in range(size)] for _ in range(size)]
    max_cells = size * size
    reserved = {tuple(agent_pos)}

    while True:
        try:
            max_pits = max_cells - len(reserved) - 2
            num_pits = int(input(f"Enter number of pits (0-{max_pits}): ").strip())
            if 0 <= num_pits <= max_pits: break
            print("Number out of range.")
        except ValueError: print("Invalid input.")

    taken = set(reserved)

    for i in range(num_pits):
        while True:
            try:
                s = input(f"Enter pit {i+1} pos 'r c': ").split()
                x, y = int(s[0]), int(s[1])
                if (0 <= x < size and 0 <= y < size) and (x, y) not in taken:
                    world[x][y] = "P"; taken.add((x, y)); break
                print("Invalid or occupied.")
            except: print("Error.")

    for label in ["Wumpus", "Gold"]:
        while True:
            try:
                s = input(f"Enter {label} pos 'r c': ").split()
                x, y = int(s[0]), int(s[1])
                if (0 <= x < size and 0 <= y < size) and (x, y) not in taken:
                    world[x][y] = label[0]; taken.add((x, y)); break
                print("Invalid or occupied.")
            except: print("Error.")

def display_kb():
    """Modified Display with Borders and Indices"""
    print("\nKnowledge Base Map:")
    col_header = "    " + "  ".join(f"{j}" for j in range(SIZE))
    print(col_header)
    print("   " + "---" * SIZE)
    
    for i in range(SIZE):
        row_cells = []
        for j in range(SIZE):
            if [i, j] == agent_pos:
                symbol = "A"
            else:
                cell = kb[i][j]
                if cell['pit'] == 'confirmed': symbol = "P"
                elif cell['wumpus'] == 'confirmed': symbol = "W"
                elif cell.get('safe', False):
                    symbol = "V" if cell.get('visited', False) else "s"
                elif cell['pit'] == 'possible' and cell['wumpus'] == 'possible':
                    symbol = "?"
                elif cell['pit'] == 'possible': symbol = "p?"
                elif cell['wumpus'] == 'possible': symbol = "w?"
                else: symbol = "."
            row_cells.append(f"{symbol:^3}")
        print(f"{i} |" + "".join(row_cells) + "|")
    
    print("   " + "---" * SIZE)
    print("\nLegend: A:Agent V:Visited s:Safe P:Pit W:Wumpus p?:Maybe Pit w?:Maybe Wumpus\n")

def try_confirm():
    for i in range(SIZE):
        for j in range(SIZE):
            cell = kb[i][j]
            if cell['pit'] != 'confirmed' and cell['pit'] != 'no' and cell['pit_count'] >= 2:
                cell['pit'] = 'confirmed'
            if cell['wumpus'] != 'confirmed' and cell['wumpus'] != 'no' and cell['wumpus_count'] >= 2:
                cell['wumpus'] = 'confirmed'
            if cell['pit'] == 'no' and cell['wumpus'] == 'no' and not cell['safe']:
                cell['safe'] = True

def update_kb_from_percepts(x, y, breeze, stench):
    key = (x, y)
    if key not in processed_percepts:
        processed_percepts[key] = {'breeze': False, 'stench': False}

    if breeze:
        if not processed_percepts[key]['breeze']:
            for nx, ny in neighbors(x, y):
                if [nx, ny] == agent_pos or kb[nx][ny]['visited']: continue
                if kb[nx][ny]['pit'] not in ['no', 'confirmed']:
                    kb[nx][ny]['pit'] = 'possible'
                    kb[nx][ny]['pit_count'] += 1
            processed_percepts[key]['breeze'] = True
    else:
        for nx, ny in neighbors(x, y):
            kb[nx][ny]['pit'] = 'no'

    if stench:
        if not processed_percepts[key]['stench']:
            for nx, ny in neighbors(x, y):
                if [nx, ny] == agent_pos or kb[nx][ny]['visited']: continue
                if kb[nx][ny]['wumpus'] not in ['no', 'confirmed']:
                    kb[nx][ny]['wumpus'] = 'possible'
                    kb[nx][ny]['wumpus_count'] += 1
            processed_percepts[key]['stench'] = True
    else:
        for nx, ny in neighbors(x, y):
            kb[nx][ny]['wumpus'] = 'no'
    
    try_confirm()

def sensor():
    global has_gold, agent_pos
    x, y = agent_pos
    kb[x][y]['visited'] = True
    
    if world[x][y] == "G":
        print("GLITTER! You found the Gold!")
        has_gold = True
    
    breeze = any(world[nx][ny] == "P" for nx, ny in neighbors(x, y))
    stench = any(world[nx][ny] == "W" for nx, ny in neighbors(x, y))
    
    if breeze: print("Percept: You feel a Breeze.")
    if stench: print("Percept: You smell a Stench.")
    
    update_kb_from_percepts(x, y, breeze, stench)

def main():
    global agent_pos
    try:
        s = int(input("Enter grid size: "))
        init_kb(s)
        create_world(s)
    except: return

    while not has_gold:
        display_kb()
        sensor()
        
        move = input("Move (w/a/s/d) or quit (q): ").lower()
        if move == 'q': break
        
        nx, ny = agent_pos[0], agent_pos[1]
        if move == 'w': nx -= 1
        elif move == 's': nx += 1
        elif move == 'a': ny -= 1
        elif move == 'd': ny += 1
        
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            agent_pos = [nx, ny]
            if world[nx][ny] == "P":
                print("FELL IN A PIT! Game Over."); break
            if world[nx][ny] == "W":
                print("EATEN BY WUMPUS! Game Over."); break
        else:
            print("BUMP! Hit a wall.")

if __name__ == "__main__":
    main()

