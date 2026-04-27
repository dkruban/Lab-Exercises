# === Wumpus World ===
# Real board (hidden from agent)

board = [[['S'],[],['B'],['G']],
         [['W'],['S','B'],['P'],['B']],
         [['S','B'],['P'],['B'],[]],
         [['A'],['B'],[],[]]]

# Knowledge board (what the agent knows)
knowledge = [['?'] * 4 for _ in range(4)]

curr_pos = [3, 0]
has_gold = False
alive = True

moves = {'w': (-1,0), 's': (1,0), 'a': (0,-1), 'd': (0,1)}
move_names = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}

def printGrid(grid, title):
    print(f"\n  {title}")
    n = len(grid)
    w = 10
    for r in range(n):
        print("  +" + (("-" * w + "+") * n))
        line = "  "
        for c in range(n):
            cell = grid[r][c]
            if isinstance(cell, list):
                content = ",".join(cell) if cell else "."
            else:
                content = cell
            line += "|" + content.center(w)
        line += "|"
        print(line)
    print("  +" + (("-" * w + "+") * n))

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
        print(knowledge[r][c])
    else:
        knowledge[r][c] = "OK"

def play():
    global curr_pos, has_gold, alive

    print("=" * 50)
    print("       WUMPUS WORLD")
    print("=" * 50)
    print("Controls: w=Up, s=Down, a=Left, d=Right")
    print("          r=Restart, q=Quit")
    print("Symbols:  W=Wumpus, P=Pit, G=Gold")
    print("          S=Stench, B=Breeze, A=Agent")
    print("          OK=Safe, ?=Unknown")
    print("=" * 50)

    # Initial perception
    perceive()
    knowledge[curr_pos[0]][curr_pos[1]] += ",A"

    while True:
        printGrid(knowledge, "KNOWLEDGE GRID")
        print(f"\n  Position: ({curr_pos[0]},{curr_pos[1]})", end="")
        if has_gold:
            print(" | Carrying GOLD!", end="")
        print()

        cmd = input("\n  Move (w/a/s/d/r/q): ").strip().lower()

        if cmd == 'q':
            print("\n  Goodbye!")
            break

        if cmd == 'r':
            # Restart agent position, keep knowledge
            knowledge[curr_pos[0]][curr_pos[1]] = knowledge[curr_pos[0]][curr_pos[1]].replace(",A", "")
            curr_pos = [3, 0]
            has_gold = False
            alive = True
            if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                knowledge[curr_pos[0]][curr_pos[1]] += ",A"
            print("\n  Restarted at (3,0) with current knowledge!")
            continue

        if cmd not in moves:
            print("  Invalid input! Use w/a/s/d/r/q")
            continue

        # Calculate new position
        dr, dc = moves[cmd]
        nr, nc = curr_pos[0] + dr, curr_pos[1] + dc

        if nr < 0 or nr > 3 or nc < 0 or nc > 3:
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
                    curr_pos = [3, 0]
                    has_gold = False
                    alive = True
                    if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                        knowledge[curr_pos[0]][curr_pos[1]] += ",A"
                    print("\n  Restarted at (3,0) with current knowledge!")
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
                    curr_pos = [3, 0]
                    has_gold = False
                    alive = True
                    if ",A" not in knowledge[curr_pos[0]][curr_pos[1]]:
                        knowledge[curr_pos[0]][curr_pos[1]] += ",A"
                    print("\n  Restarted at (3,0) with current knowledge!")
                    break
                elif cmd2 == 'q':
                    print("\n  Goodbye!")
                    return
            continue

        if 'G' in cell:
            has_gold = True
            print("  You found the GOLD!")

        # Perceive and mark agent
        perceive()
        knowledge[nr][nc] += ",A"

        # Check win condition
        if has_gold and curr_pos == [3, 0]:
            printGrid(knowledge, "KNOWLEDGE GRID")
            print("\n  You brought the gold home! YOU WIN!")
            break

play()



