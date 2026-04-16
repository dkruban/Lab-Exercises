import random
class WumpusWorld:
    def __init__(self):
        self.size = 4
        # Agent always starts at [0, 0]
        self.agent_pos = [0, 0]
        self.agent_dir = "RIGHT" 
        self.has_gold = False
        self.wumpus_alive = True
        self.arrow = True
        self.score = 0
        self.game_over = False
        self.last_action_msg = "Game Started! Use WASD to move/turn."
        
        self._setup_world()

    def _setup_world(self):
        # Generate coordinates excluding (0,0)
        cells = [(r, c) for r in range(4) for c in range(4) if (r, c) != (0, 0)]
        random.shuffle(cells)
        
        self.wumpus_pos = cells.pop()
        self.gold_pos = cells.pop()
        self.pit_positions = [cells.pop() for _ in range(3)]

    def get_percepts(self):
        r, c = self.agent_pos
        percepts = []
        
        # Neighbors for Stench and Breeze
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                if (nr, nc) == self.wumpus_pos and self.wumpus_alive:
                    if "Stench" not in percepts: percepts.append("Stench")
                if (nr, nc) in self.pit_positions:
                    if "Breeze" not in percepts: percepts.append("Breeze")
        
        if tuple(self.agent_pos) == self.gold_pos and not self.has_gold:
            percepts.append("Glitter")
        return percepts

    def get_free_boxes(self):
        # Logical 'Safe' boxes for the agent
        safe = []
        for r in range(4):
            for c in range(4):
                if (r, c) != self.wumpus_pos and (r, c) not in self.pit_positions:
                    safe.append((r, c))
        return safe

    def draw_map(self):
        print("\n" + "="*40)
        print(" SCORE: {} | GOLD: {} | ARROW: {}".format(self.score, self.has_gold, self.arrow))
        print(" PERCEPTS: {}".format(", ".join(self.get_percepts()) if self.get_percepts() else "None"))
        print("="*40)
        
        icons = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
        
        for r in range(3, -1, -1):
            row = "|"
            for c in range(4):
                if [r, c] == self.agent_pos:
                    row += " " + icons[self.agent_dir] + " |"
                else:
                    # Logic to show objects for debugging (Optional: change '.' to hide)
                    char = "."
                    row += " " + char + " |"
            print(row)
            print("-" * 17)
        print("SAFE BOXES: " + str(self.get_free_boxes()))

    def update(self, action):
        action = action.lower()
        if not action: return
        
        self.score -= 1 # Every action costs 1
        
        
        if action == 'w': # Move Forward in current 
            r, c = self.agent_pos
            nr, nc = r, c
	   ::
            if self.agent_dir == "UP": nr += 1
            elif self.agent_dir == "DOWN": nr -= 1
            elif self.agent_dir == "LEFT": nc -= 1
            elif self.agent_dir == "RIGHT": nc += 1
            
            if 0 <= nr < 4 and 0 <= nc < 4:
                self.agent_pos = [nr, nc]
                self.last_action_msg = "Moved to " + str(self.agent_pos)
                if (nr, nc) == self.wumpus_pos and self.wumpus_alive:
                    self.score -= 1000
                    self.game_over = True
                    self.last_action_msg = "GAME OVER: Eaten by Wumpus!"
                elif (nr, nc) in self.pit_positions:
                    self.score -= 1000
                    self.game_over = True
                    self.last_action_msg = "GAME OVER: Fell in a Pit!"
            else:
                self.last_action_msg = "BUMP! You hit a wall."

        # Turning
        elif action == 'a': 
            self.agent_dir = "LEFT"
            self.last_action_msg = "Facing Left"
        elif action == 'd': 
            self.agent_dir = "RIGHT"
            self.last_action_msg = "Facing Right"
        elif action == 's': 
            self.agent_dir = "DOWN"
            self.last_action_msg = "Facing Down"
        elif action == 'u': # Extra key for Up
            self.agent_dir = "UP"
            self.last_action_msg = "Facing Up"

        # Action Keys
        elif action == 'g': # Grab
            if tuple(self.agent_pos) == self.gold_pos:
                self.has_gold = True
                self.last_action_msg = "GLITTER! You grabbed the Gold!"
            else:
                self.last_action_msg = "Nothing here to grab."

        elif action == 'f': # Fire
            if self.arrow:
                self.arrow = False
                self.score -= 10
                r, c = self.agent_pos
                wr, wc = self.wumpus_pos
                hit = False
                if self.agent_dir == "UP" and c == wc and r < wr: hit = True
                elif self.agent_dir == "DOWN" and c == wc and r > wr: hit = True
                elif self.agent_dir == "RIGHT" and r == wr and c < wc: hit = True
                elif self.agent_dir == "LEFT" and r == wr and c > wc: hit = True
                
                if hit:
                    self.wumpus_alive = False
                    self.last_action_msg = "SCREAM! The Wumpus is dead!"
                else:
                    self.last_action_msg = "Arrow missed the target."
            else:
                self.last_action_msg = "Out of arrows!"

        elif action == 'c': # Climb
            if self.agent_pos == [0, 0] and self.has_gold:
                self.score += 1000
                self.game_over = True
                self.last_action_msg = "VICTORY! You climbed out with the gold!"
            else:
                self.last_action_msg = "You can only climb out at (0,0) with gold."

def main():
    game = WumpusWorld()
    print("=== WUMPUS WORLD: HUMAN EDITION ===")
    print("CONTROLS:")
    print("  W: Move Forward      A/S/D/U: Turn Left/Down/Right/Up")
    print("  G: Grab Gold         F: Fire Arrow")
    print("  C: Climb Out         Q: Quit Game")
    
    while not game.game_over:
        game.draw_map()
        print("STATUS: " + game.last_action_msg)
        cmd = input("ENTER COMMAND: ").strip().lower()
        
        if cmd == 'q': break
        game.update(cmd)
        
    game.draw_map()
    print("\n--- FINAL RESULT ---")
    print("MESSAGE: " + game.last_action_msg)
    print("TOTAL SCORE: " + str(game.score))

if __name__ == "__main__":
    main()       

