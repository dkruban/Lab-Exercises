import random
class Cell:
    def __init__(self):
        self.wumpus = False
        self.breeze = False
        self.gold = False
        self.stench = False
        self.pit = False
        self.visited = False
        self.scream=False
        self.known_safe = False

class WumpusWorld:
    def __init__(self, size):
        self.size = size
        self.env = [[Cell() for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0,size-1)
        self.wumpus_alive = True
        self.possible_wumpus_locations = {(i, j) for i in range(self.size) for j in range(self.size) if (i, j) != self.agent_pos}
        self.no_pit_locations = set()
        self.inferred_wumpus = None
        self.inferred_pits = set()

    def get_neighbours(self, x, y):
        neigh = []
        if x > 0:
            neigh.append((x - 1, y))
        if x < self.size - 1:
            neigh.append((x + 1, y))
        if y > 0:
            neigh.append((x, y - 1))
        if y < self.size - 1:
            neigh.append((x, y + 1))
        return neigh

    def add_pit(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.env[x][y].pit = True
            for i, j in self.get_neighbours(x, y):
                self.env[i][j].breeze = True
        else:
            print(f"Invalid pit location ({x}, {y}) ignored.")

    def add_wumpus(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.env[x][y].wumpus = True
            for i, j in self.get_neighbours(x, y):
                self.env[i][j].stench = True
        else:
            print(f"Invalid wumpus location ({x}, {y}) ignored.")

    def add_gold(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.env[x][y].gold = True
        else:
            print(f"Invalid gold location ({x}, {y}) ignored.")

    def get_perception(self, x, y):
        cell = self.env[x][y]
        stench = cell.stench
        breeze = cell.breeze
        glitter = cell.gold
        bump = False
        scream=False
        return [stench, breeze, glitter, bump,scream]

    def print_full_world_state(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.agent_pos:
                    print("A", end="")
                elif self.env[i][j].wumpus and self.wumpus_alive:
                    print("W", end="")
                elif self.env[i][j].pit:
                    print("P", end="")
                elif self.env[i][j].gold:
                    print("G", end="")
                else:
                    print("_", end="")
                print("|\t", end="")
            print()

    def print_world_state(self):
        x, y = self.agent_pos
        current_cell = self.env[x][y]
        stench = current_cell.stench
        breeze = current_cell.breeze

        # Get neighbors of current position
        neighbors = self.get_neighbours(x, y)
        neighbors_set = set(neighbors)

        for i in range(self.size):
            for j in range(self.size):
                pos = (i, j)
                if pos == self.agent_pos:
                    # Agent position
                    print("A", end="")
                elif self.env[i][j].visited:
                    # Visited cell display
                    if self.env[i][j].gold:
                        print("G", end="")
                    elif self.env[i][j].breeze and self.env[i][j].stench:
                        print("BS", end="")
                    elif self.env[i][j].breeze:
                        print("B", end="")
                    elif self.env[i][j].stench:
                        print("S", end="")
                    else:
                        print(".", end="")  # Visited safe path
                elif pos == self.inferred_wumpus:
                    print("W?", end="")
                elif pos in self.inferred_pits:
                    print("P?", end="")
                elif stench and (pos in neighbors_set) and (not self.env[i][j].visited):
                    # If current cell has stench, mark neighbors unvisited as possible Wumpus with "W?"
                    print("W?", end="")
                elif breeze and (pos in neighbors_set) and (not self.env[i][j].visited):
                    # If current cell has breeze, mark neighbors unvisited as possible Pit with "P?"
                    print("P?", end="")
                elif self.env[i][j].known_safe:
                    print("O", end="")
                else:
                    # Unknown positions marked with "?"
                    print("?", end="")
                print("|\t", end="")
            print()

    def get_possible_directions(self):
        x, y = self.agent_pos
        possibles = {}
        if x > 0:
            possibles["w"] = (x - 1, y)
        if x < self.size - 1:
            possibles["s"] = (x + 1, y)
        if y > 0:
            possibles["a"] = (x, y - 1)
        if y < self.size - 1:
            possibles["d"] = (x, y + 1)
        return possibles

    def update_kb(self, x, y, has_stench, has_breeze):
        neighbors = self.get_neighbours(x, y)
        self.possible_wumpus_locations.discard((x, y))
        self.no_pit_locations.add((x, y))
        if not has_stench:
            for nx, ny in neighbors:
                self.possible_wumpus_locations.discard((nx, ny))
        else:
            possible_here = set(neighbors)
            self.possible_wumpus_locations &= possible_here
        if not has_breeze:
            for nx, ny in neighbors:
                self.no_pit_locations.add((nx, ny))

    def infer_dangers(self):
        if self.wumpus_alive and len(self.possible_wumpus_locations) == 1:
            pos = next(iter(self.possible_wumpus_locations))
            if self.inferred_wumpus is None:
                self.inferred_wumpus = pos
                print(f"Concluded Wumpus is located at {pos}")

        changed = True
        while changed:
            changed = False
            for vx, vy in [(a, b) for a in range(self.size) for b in range(self.size) if self.env[a][b].visited and self.env[a][b].breeze]:
                neighbors = self.get_neighbours(vx, vy)
                possible_pit_neigh = [(nx, ny) for nx, ny in neighbors if (nx, ny) not in self.no_pit_locations and (nx, ny) not in self.inferred_pits]
                if len(possible_pit_neigh) == 1:
                    pit_pos = possible_pit_neigh[0]
                    if pit_pos not in self.inferred_pits:
                        self.inferred_pits.add(pit_pos)
                        changed = True
                        print(f"Concluded pit is located at {pit_pos}")

        for i in range(self.size):
            for j in range(self.size):
                if not self.env[i][j].visited:
                    is_safe = (
                        (i, j) in self.no_pit_locations and
                        (i, j) not in self.possible_wumpus_locations and
                        (i, j) != self.inferred_wumpus and
                        (i, j) not in self.inferred_pits
                    )
                    self.env[i][j].known_safe = is_safe

    def simulate_start_game(self):
        path = [self.agent_pos]
        x, y = self.agent_pos
        self.env[x][y].visited = True
        self.env[x][y].known_safe = True
        print("\nInitial full grid (all contents visible):")
        self.print_full_world_state()
        i = 0
        while True:
            x, y = self.agent_pos
            perceptions = self.get_perception(x, y)
            self.update_kb(x, y, perceptions[0], perceptions[1])
            self.infer_dangers()

            print(f"\nIteration - {i}")
            i += 1
            self.print_world_state()
            print(f"@({x},{y}) : [Stench: {perceptions[0]}, Breeze: {perceptions[1]}, Glitter: {perceptions[2]}, Bump: {perceptions[3]},scream:False]")

            if perceptions[2]:
                print("Gold found!")
                return path

            if self.env[x][y].wumpus and self.wumpus_alive:
                print("You stepped on the Wumpus! Game over.")
                return None
            if self.env[x][y].pit:
                print("You fell into a pit! Game over.")
                return None

            possible_dirs = self.get_possible_directions()
            if not possible_dirs:
                print("No possible moves!")
                continue
            print("Possible next tiles:")
            for d, pos in possible_dirs.items():
                px, py = pos
                if (px, py) == self.inferred_wumpus:
                    status = "(wumpus!)"
                elif (px, py) in self.inferred_pits:
                    status = "(pit!)"
                elif self.env[px][py].known_safe:
                    status = "(safe)"
                else:
                    status = "(unknown)"
                print(f"{d}: {pos} {status}")
            direction = input("Enter direction to move (w:up / s:down / a:left / d:right): ").lower()
            if direction not in possible_dirs:
                print("Invalid direction!")
                return None
            new_pos = possible_dirs[direction]
            self.agent_pos = new_pos
            self.env[new_pos[0]][new_pos[1]].visited = True
            self.env[new_pos[0]][new_pos[1]].known_safe = True
            path.append(new_pos)

# Main
try:
    n = 4
    if n <= 0:
        raise ValueError("Grid size must be positive.")
    wum_world = WumpusWorld(n)

    n_pits = 3
    if n_pits < 0:
        raise ValueError("Number of pits cannot be negative.")

    valid_positions = [(i, j) for i in range(n) for j in range(n) if (i, j) != (0, n-1)]
    random.shuffle(valid_positions)

    pit_positions = [(2,1),(3,0),(2,3)]
    for x, y in pit_positions:
        wum_world.add_pit(x, y)
        print(f"Pit placed at ({x}, {y})")

    remaining_positions = [(x, y) for x, y in valid_positions if (x, y) not in pit_positions]
    if not remaining_positions:
        raise ValueError("No valid position for wumpus.")
    wumpus_pos = (0,1)
    wum_world.add_wumpus(*wumpus_pos)
    print(f"Wumpus placed at {wumpus_pos}")

    remaining_positions = [(x, y) for x, y in remaining_positions if (x, y) != wumpus_pos]
    if not remaining_positions:
        raise ValueError("No valid position for gold.")
    gold_pos = (1,1)
    wum_world.add_gold(*gold_pos)
    print(f"Gold placed at {gold_pos}")

    path = wum_world.simulate_start_game()
    print("Path taken:", path)

except ValueError as e:
    print(f"Error: {e}")

