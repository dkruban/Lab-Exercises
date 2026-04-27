import random

import sys

# === Wumpus World ===
# Real board (hidden from agent)
board = []

# Knowledge board (what the agent knows)
knowledge = []

# Global Game State
curr_pos = [0, 0]
facing = 'RIGHT'
wumpus_alive = True
screamed = False
alive = True
grid_size = 4

moves = {'w': (-1,0), 's': (1,0), 'a': (0,-1), 'd': (0,1)}
move_names = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}

def printGrid(grid, title):
    print(f"\n  {title}")
    n = len(grid)
    w = 12
    for r in range(n):
        print("  +" + (("-" * w + "+") * n))
        line = "  "
        for c in range(n):
            cell = grid[r][c]
            if isinstance(cell, list):
                if not cell: content = "."
                else: content = ",".join(cell)
            else:
                content = cell
            line += "|" + content.center(w)
        line += "|"
        print(line)
    print("  +" + (("-" * w + "+") * n))

def get_current_percepts():
    """Returns a list of percepts at the current position."""
    r, c = curr_pos
    cell_content = board[r][c]
    percepts = []
    
    for item in cell_content:
        if item == 'S': percepts.append('Stench')
        elif item == 'B': percepts.append('Breeze')
        elif item == 'G': percepts.append('Glitter')
    
    if screamed:
        percepts.append('Scream')
        
    return percepts

def update_knowledge(percepts):
    """Update the knowledge grid string for display based on percepts."""
    r, c = curr_pos
    k_content = []
    
    if 'Stench' in percepts: k_content.append('S')
    if 'Breeze' in percepts: k_content.append('B')
    if 'Glitter' in percepts: k_content.append('G')
    if 'Scream' in percepts: k_content.append('Scr')
    
    k_content.append('A')
    knowledge[r][c] = ",".join(k_content)

def add_adjacent_percept(r, c, item):
    """Helper to add 'S' or 'B' to adjacent cells."""
    deltas = [(-1,0), (1,0), (0,-1), (0,1)]
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid_size and 0 <= nc < grid_size:
            if item not in board[nr][nc]:
                board[nr][nc].append(item)

def parse_coordinate(prompt):
    while True:
        try:
            val = input(prompt).strip()
            if not val: return None
            # Support inputs like "3 0" or "3,0"
            parts = val.replace(',', ' ').split()
            if len(parts) != 2:
                print("  Please enter two numbers separated by space or comma.")
                continue
            r, c = map(int, parts)
            if 0 <= r < grid_size and 0 <= c < grid_size:
                return [r, c]
            else:
                print(f"  Coordinates must be between 0 and {grid_size-1}.")
        except ValueError:
            print("  Invalid input. Please enter numbers.")

def setup_game():
    global board, knowledge, curr_pos, grid_size, wumpus_alive, screamed, alive
    
    print("=== Custom Wumpus Map Setup ===")
    
    # 1. Grid Size
    while True:
        try:
            sz_str = input("Enter grid size N (default 4): ").strip()
            if not sz_str:
                grid_size = 4
            else:
                grid_size = int(sz_str)
                if grid_size < 2:
                    print("  Size must be at least 2.")
                    continue
            break
        except ValueError:
            print("  Invalid number.")

    # 2. Mode Selection
    while True:
        mode = input("Map Generation: (M)anual or (R)andom? ").strip().lower()
        if mode in ['m', 'r']:
            break
        print("  Please enter 'm' or 'r'.")

    # Initialize Boards
    board = [[[] for _ in range(grid_size)] for _ in range(grid_size)]
    knowledge = [['?'] * grid_size for _ in range(grid_size)]
    
    if mode == 'm':
        # Manual Mode
        # Agent Location
        print(f"Grid is {grid_size}x{grid_size}. Coordinates are 0-indexed (0 to {grid_size-1}).")
        pos = parse_coordinate("Enter Agent start (row col): ")
        curr_pos = pos if pos else [grid_size-1, 0]
        
        # Gold Location (1)
        g_pos = parse_coordinate("Enter Gold location (row col): ")
        if not g_pos: g_pos = [0, grid_size-1] 
        board[g_pos[0]][g_pos[1]].append('G')
        
        # Wumpus Location (1)
        w_pos = parse_coordinate("Enter Wumpus location (row col): ")
        if not w_pos: w_pos = [0, 0] 
        board[w_pos[0]][w_pos[1]].append('W')
        add_adjacent_percept(w_pos[0], w_pos[1], 'S')
        
        # Pit Locations (20%)
        num_pits = int(0.2 * grid_size * grid_size)
        print(f"\nTime to place {num_pits} pits (20% of {grid_size*grid_size} cells).")
        
        for i in range(num_pits):
            p_pos = parse_coordinate(f"Enter Pit #{i+1} loc (row col): ")
            if p_pos:
                if 'P' not in board[p_pos[0]][p_pos[1]]:
                    board[p_pos[0]][p_pos[1]].append('P')
                    add_adjacent_percept(p_pos[0], p_pos[1], 'B')
                else:
                    print("  Pit already there.")
    else:
        # Random Mode
        print("\n  >> Randomly generating map...")
        
        # Agent Start (Random)
        curr_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
        
        # Helper for random empty spots (excluding Agent start for safety)
        def get_random_pos(exclude_list):
            while True:
                r = random.randint(0, grid_size-1)
                c = random.randint(0, grid_size-1)
                if [r, c] not in exclude_list:
                    return [r, c]

        # Gold (1) - can be anywhere not start
        g_pos = get_random_pos([curr_pos])
        board[g_pos[0]][g_pos[1]].append('G')
        
        # Wumpus (1) - anywhere not start
        w_pos = get_random_pos([curr_pos])
        board[w_pos[0]][w_pos[1]].append('W')
        add_adjacent_percept(w_pos[0], w_pos[1], 'S')
        
        # Pits (20%) - anywhere not start
        num_pits = int(0.2 * grid_size * grid_size)
        pits_placed = 0
        while pits_placed < num_pits:
            r = random.randint(0, grid_size-1)
            c = random.randint(0, grid_size-1)
            if [r, c] != curr_pos:
                if 'P' not in board[r][c]:
                    board[r][c].append('P')
                    add_adjacent_percept(r, c, 'B')
                    pits_placed += 1

    # Reset game state
    curr_pos = curr_pos # Set
    wumpus_alive = True
    screamed = False
    alive = True
    
    print("\nMap Setup Complete!")
    # Remove 'A' marker logic from board (handled by curr_pos)

def play():
    global curr_pos, facing, screamed

    setup_game()

    print("=" * 50)
    print("       WUMPUS WORLD (Custom)")
    print("=" * 50)
    print("Controls: w=Up, s=Down, a=Left, d=Right")
    print("          q=Quit")
    print("Goal:     Reach the Gold.")
    print("=" * 50)

    # Initial update
    update_knowledge(get_current_percepts())

    while True:
        # 1. Get Percepts
        current_percepts = get_current_percepts()
        
        # 2. Display Game State
        printGrid(knowledge, "KNOWLEDGE GRID")
        print(f"\n  Position: {curr_pos}, Facing: {facing}")
        print(f"  Percepts: {current_percepts}")
        
        # 3. Check Game Over/Win Conditions
        r, c = curr_pos
        cell = board[r][c]
        
        if 'P' in cell:
            print("\n  You fell into a pit! GAME OVER")
            break
        
        if 'W' in cell and wumpus_alive:
            print("\n  You were eaten by the Wumpus! GAME OVER")
            break
            
        if 'G' in cell:
            print("\n  You found the GOLD! YOU WIN!")
            break

        # 4. Input
        cmd = input("\n  Action (w/a/s/d/q): ").strip().lower()

        if screamed: screamed = False

        if cmd == 'q':
            print("\n  Goodbye!")
            break

        if cmd in moves:
            new_facing = move_names[cmd]
            facing = new_facing
            
            dr, dc = moves[cmd]
            nr, nc = curr_pos[0] + dr, curr_pos[1] + dc

            if nr < 0 or nr >= grid_size or nc < 0 or nc >= grid_size:
                print("  >> Bump! You hit a wall.")
            else:
                old_k = knowledge[curr_pos[0]][curr_pos[1]].split(",")
                if 'A' in old_k: old_k.remove('A')
                if not old_k: knowledge[curr_pos[0]][curr_pos[1]] = "OK"
                else: knowledge[curr_pos[0]][curr_pos[1]] = ",".join(old_k)

                curr_pos = [nr, nc]
                print(f"  >> Moved {facing} to ({nr},{nc})")
                update_knowledge(get_current_percepts())
                
        else:
            print("  Invalid command.")

if __name__ == "__main__":
    play()
