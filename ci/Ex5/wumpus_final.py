# === Wumpus World ===
import random

n = int(input("Enter size of board: "))

def makeBoard(n):
    board = [[[] for _ in range(n)] for _ in range(n)]
    
    num_pits = max(1, (n * n) // 8)
    num_gold = max(1, (n * n) // 16)
    
    all_positions = [(r, c) for r in range(n) for c in range(n)]
    random.shuffle(all_positions)
    
    agent_pos = all_positions.pop()
    board[agent_pos[0]][agent_pos[1]].append('A')
    
    wumpus_pos = all_positions.pop()
    board[wumpus_pos[0]][wumpus_pos[1]].append('W')
    
    # Place Pits
    pit_positions = []
    for _ in range(num_pits):
        if all_positions:
            pit_pos = all_positions.pop()
            board[pit_pos[0]][pit_pos[1]].append('P')
            pit_positions.append(pit_pos)
    
    # Place Gold
    for _ in range(num_gold):
        if all_positions:
            gold_pos = all_positions.pop()
            board[gold_pos[0]][gold_pos[1]].append('G')
    
    # Add Stench around Wumpus
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = wumpus_pos[0] + dr, wumpus_pos[1] + dc
        if 0 <= nr < n and 0 <= nc < n:
            if 'S' not in board[nr][nc]:
                board[nr][nc].append('S')
    
    # Add Breeze around Pits
    for pit_pos in pit_positions:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = pit_pos[0] + dr, pit_pos[1] + dc
            if 0 <= nr < n and 0 <= nc < n:
                if 'B' not in board[nr][nc]:
                    board[nr][nc].append('B')
    
    return board, agent_pos

board, start_pos = makeBoard(n)

# Knowledge board (what the agent knows)
knowledge = [['?'] * n for _ in range(n)]

curr_pos = list(start_pos)
has_gold = False
alive = True

moves = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
move_names = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}

def printGrid(grid, title):
    print(f"\n  {title}")
    size = len(grid)
    w = 10
    for r in range(size):
        print("  +" + (("-" * w + "+") * size))
        line = "  "
        for c in range(size):
            cell = grid[r][c]
            if isinstance(cell, list):
                content = ",".join(cell) if cell else "."
            else:
                content = cell
            line += "|" + content.center(w)
        line += "|"
        print(line)
    print("  +" + (("-" * w + "+") * size))

def perceive():
    """Update knowledge at current position"""
    r, c = curr_pos
    cell = board[r][c]
    percepts = []
    for item in cell:
        if item == 'S':
            percepts.append('S')
        elif item == 'B':
            percepts.append('B')
        elif item == 'G':
            percepts.append('G')
    if percepts:
        knowledge[r][c] = ",".join(percepts)
    else:
        knowledge[r][c] = "OK"

def play():
    global curr_pos, has_gold, alive

    print("=" * 50)
    print("       WUMPUS WORLD")
    print("=" * 50)
    print(f"Board size: {n}x{n}")
    print(f"Start position: {start_pos}")
    print("Controls: w=Up, s=Down, a=Left, d=Right")
    print("          r=Restart, q=Quit")
    print("Symbols:  W=Wumpus, P=Pit, G=Gold")
    print("          S=Stench, B=Breeze, A=Agent")
    print("          OK=Safe, ?=Unknown")
    print("Goal: Find gold and return to start!")
    print("=" * 50)

    # Initial perception
    perceive()
    knowledge[curr_pos[0]][curr_pos[1]] += ",A"
    # Mark start position
    knowledge[start_pos[0]][start_pos[1]] = knowledge[start_pos[0]][start_pos[1]].replace("OK", "HOME")

    while True:
        printGrid(knowledge, "KNOWLEDGE GRID")
        print(f"\n  Position: ({curr_pos[0]},{curr_pos[1]})", end="")
        print(f" | Home: {start_pos}", end="")
        if has_gold:
            print(" | Carrying GOLD!", end="")
        print()

        cmd = input("\n  Move (w/a/s/d/r/q): ").strip().lower()

        if cmd == 'q':
            print("\n  Goodbye!")
            break

        if cmd == 'm':
            printGrid(board, "REAL BOARD (CHEAT)")
            continue

        if cmd == 'r':
            # Restart agent position, keep knowledge
            knowledge[curr_pos[0]][curr_pos[1]] = knowledge[curr_pos[0]][curr_pos[1]].replace(",A", "")
            curr_pos = list(start_pos)
            has_gold = False
            alive = True
            if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                knowledge[curr_pos[0]][curr_pos[1]] += ",A"
            print(f"\n  Restarted at {start_pos} with current knowledge!")
            continue

        if cmd not in moves:
            print("  Invalid input! Use w/a/s/d/r/q/m")
            continue

        # Calculate new position
        dr, dc = moves[cmd]
        nr, nc = curr_pos[0] + dr, curr_pos[1] + dc

        if nr < 0 or nr >= n or nc < 0 or nc >= n:
            print("  You hit a wall! Move not done.")
            continue

        # Remove agent marker from old position
        knowledge[curr_pos[0]][curr_pos[1]] = knowledge[curr_pos[0]][curr_pos[1]].replace(",A", "")

        # Move agent
        curr_pos = [nr, nc]
        print(f"\n  Moved {move_names[cmd]} to ({nr},{nc})")

        # Check what's in the cell
        cell = board[nr][nc]

        if 'W' in cell:
            perceive()
            knowledge[nr][nc] = "W,DEAD"
            printGrid(knowledge, "KNOWLEDGE GRID")
            print("\n  The Wumpus got you! GAME OVER!")
            print("  Press 'r' to restart or 'q' to quit.")
            alive = False
            while True:
                cmd2 = input("\n  (r/q): ").strip().lower()
                if cmd2 == 'r':
                    knowledge[nr][nc] = "W"
                    curr_pos = list(start_pos)
                    has_gold = False
                    alive = True
                    if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                        knowledge[curr_pos[0]][curr_pos[1]] += ",A"
                    print(f"\n  Restarted at {start_pos} with current knowledge!")
                    break
                elif cmd2 == 'q':
                    print("\n  Goodbye!")
                    return
            continue

        if 'P' in cell:
            perceive()
            knowledge[nr][nc] = "P,DEAD"
            printGrid(knowledge, "KNOWLEDGE GRID")
            print("\n  You fell into a pit! GAME OVER!")
            print("  Press 'r' to restart or 'q' to quit.")
            alive = False
            while True:
                cmd2 = input("\n  (r/q): ").strip().lower()
                if cmd2 == 'r':
                    knowledge[nr][nc] = "P"
                    curr_pos = list(start_pos)
                    has_gold = False
                    alive = True
                    if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                        knowledge[curr_pos[0]][curr_pos[1]] += ",A"
                    print(f"\n  Restarted at {start_pos} with current knowledge!")
                    break
                elif cmd2 == 'q':
                    print("\n  Goodbye!")
                    return
            continue

        if 'G' in cell and not has_gold:
            has_gold = True
            board[nr][nc].remove('G')
            print("  You found the GOLD!")

        # Perceive and mark agent
        perceive()
        # Keep HOME marker if at start
        if curr_pos == list(start_pos) and "HOME" not in knowledge[nr][nc]:
            knowledge[nr][nc] = "HOME"
        knowledge[nr][nc] += ",A"

        # Check win condition
        if has_gold and curr_pos == list(start_pos):
            printGrid(knowledge, "KNOWLEDGE GRID")
            print("\n  You brought the gold home! YOU WIN!")
            break

play()
