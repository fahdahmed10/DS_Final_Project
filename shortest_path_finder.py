import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import deque
import random
import heapq
import math
from PIL import Image, ImageTk

class Graph:
    def __init__(self):
        self.adjacent_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacent_list:
            self.adjacent_list[vertex] = {}
    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacent_list[u][v] = weight
        self.adjacent_list[v][u] = weight  

    def bfs(self, start, end):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None
        queue = deque([[start]])
        visited = set()
        if start == end:
            return [start]
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node not in visited:
                visited.add(node)
                for adj in self.adjacent_list[node]:
                    new_path = list(path)
                    new_path.append(adj)
                    if adj == end:
                        return new_path
                    queue.append(new_path)
        return None

    def dijkstra(self, start, end):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None
        
        Costs = {v: float('inf') for v in self.adjacent_list}
        Costs[start] = 0
        Visited = {}
        pq = [(0, start)]
        
        while pq:
            Weight, node = heapq.heappop(pq)
            
            if node == end:
                break
                
            for nbr in self.adjacent_list[node]:
                # FIX: Use actual edge weight instead of hardcoded 1
                edge_weight = self.adjacent_list[node][nbr]
                new_cost = Weight + edge_weight
                
                if new_cost < Costs[nbr]:
                    Costs[nbr] = new_cost
                    Visited[nbr] = node
                    heapq.heappush(pq, (new_cost, nbr))
        
        # Reconstruct path
        path = []
        cur = end
        while cur in Visited:
            path.insert(0, cur)
            cur = Visited[cur]
        
        if path:
            path.insert(0, start)
        
        return path if path and path[0] == start else None

    def dfs(self, start, end):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None

        stack = [[start]]
        visited = set()

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == end:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor in self.adjacent_list.get(node, []):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        stack.append(new_path)

        return None

class PathfindingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Interactive Pathfinding Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')

        # Grid settings
        self.grid_size = 20
        self.canvas_width = 1000
        self.canvas_height = 600
        self.rows = self.canvas_height // self.grid_size
        self.cols = self.canvas_width // self.grid_size

        # Initialize variables
        self.start_pos = None
        self.end_pos = None
        self.obstacles = set()
        self.path = []
        self.visited = set()
        self.backtrack = set()
        self.dragging = None
        self.graph = Graph()
        self.weight_type = tk.StringVar(value="equal")
        
        # Drone images
        self.start_drone_image = None
        self.end_drone_image = None
        self.drone_size = self.grid_size * 0.8

        self.setup_ui()
        self.create_grid()

    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg='#1a1a2e', padx=20, pady=20)
        main_container.pack(fill='both', expand=True)

        # Top section with title and controls
        top_frame = tk.Frame(main_container, bg='#1a1a2e')
        top_frame.pack(fill='x', pady=(0, 20))

        # Title with modern styling
        title_label = tk.Label(top_frame, 
                             text="🎯 Interactive Pathfinding Visualizer",
                             font=('Segoe UI', 24, 'bold'),
                             bg='#1a1a2e',
                             fg='#ffffff')
        title_label.pack(side='left')

        # Right panel for controls
        right_panel = tk.Frame(main_container, bg='#1a1a2e', padx=20)
        right_panel.pack(side='right', fill='y')

        # Algorithm selection with modern styling
        algorithm_frame = tk.Frame(right_panel, bg='#1a1a2e', pady=10)
        algorithm_frame.pack(fill='x')
        
        tk.Label(algorithm_frame, 
                text="Algorithm:",
                font=('Segoe UI', 12),
                bg='#1a1a2e',
                fg='#ffffff').pack(side='left', padx=(0, 10))
        
        self.algorithm = ttk.Combobox(algorithm_frame, 
                                    values=["BFS", "DFS", "Dijkstra"],
                                    state="readonly",
                                    width=15)
        self.algorithm.set("BFS")
        self.algorithm.pack(side='left')

        # Weight type selection
        weight_frame = tk.Frame(right_panel, bg='#1a1a2e', pady=10)
        weight_frame.pack(fill='x')
        
        tk.Label(weight_frame,
                text="Edge Weights:",
                font=('Segoe UI', 12),
                bg='#1a1a2e',
                fg='#ffffff').pack(side='left', padx=(0, 10))
        
        equal_radio = tk.Radiobutton(weight_frame,
                                   text="Equal (1)",
                                   variable=self.weight_type,
                                   value="equal",
                                   bg='#1a1a2e',
                                   fg='#ffffff',
                                   selectcolor='#2c3e50',
                                   activebackground='#1a1a2e',
                                   activeforeground='#ffffff')
        equal_radio.pack(side='left', padx=(0, 10))
        
        random_radio = tk.Radiobutton(weight_frame,
                                    text="Random (1-15)",
                                    variable=self.weight_type,
                                    value="random",
                                    bg='#1a1a2e',
                                    fg='#ffffff',
                                    selectcolor='#2c3e50',
                                    activebackground='#1a1a2e',
                                    activeforeground='#ffffff')
        random_radio.pack(side='left')

        # Steps counter with modern styling
        steps_frame = tk.Frame(right_panel, bg='#1a1a2e', pady=10)
        steps_frame.pack(fill='x')
        
        self.steps_label = tk.Label(steps_frame,
                                  text="Steps: 0",
                                  font=('Segoe UI', 12),
                                  bg='#1a1a2e',
                                  fg='#ffffff')
        self.steps_label.pack(side='left')
        
        self.cost_label = tk.Label(steps_frame,
                                 text="",
                                 font=('Segoe UI', 12),
                                 bg='#1a1a2e',
                                 fg='#ffffff')
        self.cost_label.pack(side='left', padx=(20, 0))

        # Control buttons with modern styling
        button_frame = tk.Frame(right_panel, bg='#1a1a2e', pady=10)
        button_frame.pack(fill='x')
        
        # Style for buttons
        button_style = {
            'font': ('Segoe UI', 10),
            'bg': '#2c3e50',
            'fg': '#ffffff',
            'activebackground': '#34495e',
            'activeforeground': '#ffffff',
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }

        # Find Path button
        find_button = tk.Button(button_frame, 
                              text="Find Path",
                              command=self.find_path,
                              **button_style)
        find_button.pack(fill='x', pady=(0, 5))

        # Reset button
        reset_button = tk.Button(button_frame,
                               text="Reset",
                               command=self.reset_all,
                               **button_style)
        reset_button.pack(fill='x', pady=(0, 5))

        # Generate Obstacles button
        obstacles_button = tk.Button(button_frame,
                                   text="Generate Obstacles",
                                   command=self.generate_random_obstacles,
                                   **button_style)
        obstacles_button.pack(fill='x', pady=(0, 5))

        # How It Works button
        how_it_works_button = tk.Button(button_frame,
                                      text="How It Works",
                                      command=self.show_algorithm_explanation,
                                      **button_style)
        how_it_works_button.pack(fill='x')

        # Add drone image selection buttons
        drone_frame = tk.Frame(right_panel, bg='#1a1a2e', pady=10)
        drone_frame.pack(fill='x')
        
        tk.Label(drone_frame,
                text="Drone Images:",
                font=('Segoe UI', 12),
                bg='#1a1a2e',
                fg='#ffffff').pack(side='left', padx=(0, 10))
        
        start_drone_btn = tk.Button(drone_frame,
                                  text="Start Drone",
                                  command=lambda: self.load_drone_image('start'),
                                  bg='#2c3e50',
                                  fg='#ffffff',
                                  activebackground='#34495e',
                                  activeforeground='#ffffff',
                                  relief='flat',
                                  padx=10,
                                  pady=5)
        start_drone_btn.pack(side='left', padx=(0, 5))
        
        end_drone_btn = tk.Button(drone_frame,
                                text="End Drone",
                                command=lambda: self.load_drone_image('end'),
                                bg='#2c3e50',
                                fg='#ffffff',
                                activebackground='#34495e',
                                activeforeground='#ffffff',
                                relief='flat',
                                padx=10,
                                pady=5)
        end_drone_btn.pack(side='left')

        # Canvas for grid
        self.canvas = tk.Canvas(main_container,
                              width=self.canvas_width,
                              height=self.canvas_height,
                              bg='#ecf0f1',
                              highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True, padx=(0, 20))

        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

        # Status bar with modern styling
        status_bar = tk.Frame(main_container, bg='#2c3e50', height=30)
        status_bar.pack(fill='x', pady=(20, 0))
        
        self.status_var = tk.StringVar(value="Click to place start point (red)")
        status_label = tk.Label(status_bar,
                              textvariable=self.status_var,
                              font=('Segoe UI', 10),
                              bg='#2c3e50',
                              fg='#ffffff')
        status_label.pack(side='left', padx=10)

    def create_grid(self):
        """Create a map-like grid with subtle lines."""
        self.canvas.delete("grid")
        for x in range(0, self.canvas_width, self.grid_size):
            for y in range(0, self.canvas_height, self.grid_size):
                # Draw subtle grid lines
                self.canvas.create_line(x, 0, x, self.canvas_height,
                                      fill='#1a1a2e',  # Very dark blue
                                      tags="grid")
                self.canvas.create_line(0, y, self.canvas_width, y,
                                      fill='#1a1a2e',
                                      tags="grid")

    def get_grid_pos(self, x, y):
        return (x // self.grid_size, y // self.grid_size)

    def get_canvas_pos(self, grid_x, grid_y):
        return (grid_x * self.grid_size, grid_y * self.grid_size)

    def draw_circle(self, grid_x, grid_y, color, size_factor=0.8, tag=""):
        x, y = self.get_canvas_pos(grid_x, grid_y)
        radius = self.grid_size * size_factor / 2
        center_x = x + self.grid_size / 2
        center_y = y + self.grid_size / 2
        shadow_offset = 2
        self.canvas.create_oval(center_x - radius + shadow_offset,
                               center_y - radius + shadow_offset,
                               center_x + radius + shadow_offset,
                               center_y + radius + shadow_offset,
                               fill='#7f8c8d', outline='', tags=tag)
        return self.canvas.create_oval(center_x - radius, center_y - radius,
                                      center_x + radius, center_y + radius,
                                      fill=color, outline='white', width=2, tags=tag)

    def draw_square(self, grid_x, grid_y, color, tag=""):
        """Draw a square with modern styling and shadow effect."""
        x, y = self.get_canvas_pos(grid_x, grid_y)
        padding = 2
        shadow_offset = 2
        
        # Draw shadow
        self.canvas.create_rectangle(
            x + padding + shadow_offset,
            y + padding + shadow_offset,
            x + self.grid_size - padding + shadow_offset,
            y + self.grid_size - padding + shadow_offset,
            fill='#1a1a2e',  # Shadow color
            outline='',
            tags=tag
        )
        
        # Draw main square
        return self.canvas.create_rectangle(
            x + padding,
            y + padding,
            x + self.grid_size - padding,
            y + self.grid_size - padding,
            fill=color,
            outline='#ffffff',  # White border
            width=1,
            tags=tag
        )

    def draw_drone(self, grid_x, grid_y, color, tag=""):
        """Draw a drone with custom image or default design."""
        x, y = self.get_canvas_pos(grid_x, grid_y)
        center_x = x + self.grid_size / 2
        center_y = y + self.grid_size / 2
        
        # Check if we have a custom image
        if tag == "start" and self.start_drone_image:
            self.canvas.create_image(
                center_x, center_y,
                image=self.start_drone_image,
                tags=tag
            )
        elif tag == "end" and self.end_drone_image:
            self.canvas.create_image(
                center_x, center_y,
                image=self.end_drone_image,
                tags=tag
            )
        else:
            # Draw default drone design
            size = self.grid_size * 0.8
            
            # Draw shadow
            self.canvas.create_oval(
                center_x - size/3 + 2, center_y - size/3 + 2,
                center_x + size/3 + 2, center_y + size/3 + 2,
                fill='#1a1a2e',
                outline='',
                tags=tag
            )
            
            # Draw drone body
            self.canvas.create_oval(
                center_x - size/3, center_y - size/3,
                center_x + size/3, center_y + size/3,
                fill=color,
                outline='#ffffff',
                width=2,
                tags=tag
            )
            
            # Draw propellers
            propeller_length = size/4
            for angle in [0, 90, 180, 270]:
                rad = angle * 3.14159 / 180
                end_x = center_x + math.cos(rad) * propeller_length
                end_y = center_y + math.sin(rad) * propeller_length
                self.canvas.create_line(
                    center_x, center_y,
                    end_x, end_y,
                    fill='#ffffff',
                    width=2,
                    tags=tag
                )
            
            # Draw center dot
            self.canvas.create_oval(
                center_x - size/8, center_y - size/8,
                center_x + size/8, center_y + size/8,
                fill='#ffffff',
                outline='',
                tags=tag
            )

    def draw_obstacle(self, x, y, tag=""):
        """Draw a wall obstacle."""
        canvas_x, canvas_y = self.get_canvas_pos(x, y)
        size = self.grid_size
        
        # Draw wall shadow
        self.canvas.create_rectangle(
            canvas_x + 2, canvas_y + 2,
            canvas_x + size - 2, canvas_y + size - 2,
            fill='#2c3e50', outline='', tags=tag
        )
        
        # Draw wall
        self.canvas.create_rectangle(
            canvas_x, canvas_y,
            canvas_x + size - 2, canvas_y + size - 2,
            fill='#34495e', outline='#2c3e50', width=2, tags=tag
        )
        
        # Add brick pattern
        brick_width = size // 4
        brick_height = size // 4
        for i in range(4):
            for j in range(4):
                if (i + j) % 2 == 0:  # Create alternating pattern
                    self.canvas.create_rectangle(
                        canvas_x + i * brick_width,
                        canvas_y + j * brick_height,
                        canvas_x + (i + 1) * brick_width,
                        canvas_y + (j + 1) * brick_height,
                        fill='#2c3e50', outline='', tags=tag
                    )

    def on_click(self, event):
        grid_x, grid_y = self.get_grid_pos(event.x, event.y)
        if self.start_pos and self.start_pos == (grid_x, grid_y):
            self.dragging = 'start'
            return
        elif self.end_pos and self.end_pos == (grid_x, grid_y):
            self.dragging = 'end'
            return
        if (grid_x, grid_y) in self.obstacles:
            self.obstacles.remove((grid_x, grid_y))
            self.update_display()
            self.status_var.set("Obstacle removed!")
            return
        if not self.start_pos:
            self.start_pos = (grid_x, grid_y)
            self.status_var.set("Start point placed! Now place the end point (blue).")
        elif not self.end_pos:
            self.end_pos = (grid_x, grid_y)
            self.status_var.set("End point placed! Click to place obstacles.")
        else:
            # Place obstacle
            self.obstacles.add((grid_x, grid_y))
            self.status_var.set("Obstacle placed!")
        self.update_display()

    def on_drag(self, event):
        if self.dragging:
            grid_x, grid_y = self.get_grid_pos(event.x, event.y)
            grid_x = max(0, min(grid_x, self.cols - 1))
            grid_y = max(0, min(grid_y, self.rows - 1))
            if self.dragging == 'start':
                self.start_pos = (grid_x, grid_y)
            elif self.dragging == 'end':
                self.end_pos = (grid_x, grid_y)
            self.update_display()

    def on_release(self, event):
        self.dragging = None
        if self.start_pos and self.end_pos:
            self.status_var.set("Ready to find path! Click 'Find Shortest Path' button.")

    def on_hover(self, event):
        if not self.dragging:
            grid_x, grid_y = self.get_grid_pos(event.x, event.y)
            self.canvas.configure(cursor='hand2' if self.is_interactive_cell(grid_x, grid_y) else 'arrow')

    def is_interactive_cell(self, grid_x, grid_y):
        return (self.start_pos == (grid_x, grid_y) or
                self.end_pos == (grid_x, grid_y) or
                (grid_x, grid_y) in self.obstacles)

    def generate_random_obstacles(self):
        """Generate a maze-like pattern using recursive backtracking."""
        self.obstacles.clear()
        
        # Initialize the grid with all cells as walls
        grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        
        def carve_path(x, y):
            grid[y][x] = 0  # Mark current cell as path
            
            # Define possible directions (right, down, left, up)
            directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.cols and 0 <= ny < self.rows and 
                    grid[ny][nx] == 1):
                    # Carve path through the wall
                    grid[y + dy//2][x + dx//2] = 0
                    carve_path(nx, ny)
        
        # Start from a random even position
        start_x = random.randrange(0, self.cols, 2)
        start_y = random.randrange(0, self.rows, 2)
        carve_path(start_x, start_y)
        
        # Convert grid to obstacles
        for y in range(self.rows):
            for x in range(self.cols):
                if grid[y][x] == 1:  # If it's a wall
                    pos = (x, y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)
        
        # Ensure there's a path between start and end
        self.ensure_path_exists()
        self.update_display()
        self.status_var.set("Maze generated! Try finding a path.")

    def ensure_path_exists(self):
        """Ensure there's a path between start and end points."""
        if not self.start_pos or not self.end_pos:
            return
            
        # Clear a path between start and end if they exist
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        
        # Clear obstacles in a zigzag pattern
        current_x, current_y = x1, y1
        while (current_x, current_y) != (x2, y2):
            if current_x < x2:
                current_x += 1
            elif current_x > x2:
                current_x -= 1
            if current_y < y2:
                current_y += 1
            elif current_y > y2:
                current_y -= 1
                
            pos = (current_x, current_y)
            if pos in self.obstacles:
                self.obstacles.remove(pos)

    def build_graph(self):
        self.graph = Graph()
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in self.obstacles:
                    self.graph.add_vertex((x, y))
        
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in self.obstacles:
                                    # Suggested:
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    ...
                    for dx, dy in directions:
                        noubour_x, noubour_y = x + dx, y + dy
                        if (0 <= noubour_x < self.cols and 0 <= noubour_y < self.rows and
                            (noubour_x, noubour_y) not in self.obstacles):
                            # Use weight based on selection
                            if self.weight_type.get() == "equal":
                                weight = 1
                            else:
                                weight = random.randint(1, 15)

                            self.graph.add_edge((x, y), (noubour_x, noubour_y), weight)

    def find_path(self):
        if not self.start_pos or not self.end_pos:
            messagebox.showwarning("Warning", "Please place both start and end points!")
            return
        self.build_graph()
        used_algo = self.algorithm.get()
        
        # Clear previous path and visited nodes
        self.path = []
        self.visited.clear()
        self.backtrack.clear()
        
        if used_algo == "BFS":
            path = self.graph.bfs(self.start_pos, self.end_pos)
            self.animate_bfs_exploration()
        elif used_algo == "DFS":
            path = self.graph.dfs(self.start_pos, self.end_pos)
            self.animate_dfs_exploration()
        else:
            path = self.graph.dijkstra(self.start_pos, self.end_pos)
            self.animate_dijkstra_exploration()
            
        if path:
            self.path = path
            # Calculate total cost for all algorithms
            total_cost = 0
            for i in range(len(path) - 1):
                total_cost += self.graph.adjacent_list[path[i]][path[i + 1]]
            # Update steps and cost labels
            self.steps_label.config(text=f"Steps: {len(path)}")
            self.cost_label.config(text=f"Total Cost: {total_cost}")
            self.status_var.set(f"{used_algo} Path found!")
        else:
            messagebox.showinfo("No Path", f"No path found using {used_algo}!")
            self.status_var.set("No path found! Try removing some obstacles.")
            self.steps_label.config(text="Steps: 0")
            self.cost_label.config(text="Total Cost: 0")

    def animate_bfs_exploration(self):
        """Animate BFS exploration before showing the final path."""
        queue = deque([(self.start_pos, [self.start_pos])])
        visited = set([self.start_pos])
        
        def explore_step():
            if queue:
                current, path = queue.popleft()
                
                # Draw exploration
                if current != self.start_pos and current != self.end_pos:
                    self.draw_exploration_circle(current[0], current[1])
                
                if current == self.end_pos:
                    self.path = path
                    self.root.after(100, self.animate_final_path)  # Faster transition
                    return
                
                # Explore neighbors
                for neighbor in self.graph.adjacent_list[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
                
                self.root.after(10, explore_step)  # Much faster exploration
            else:
                self.animate_final_path()
        
        explore_step()

    def animate_dfs_exploration(self):
        """Animate DFS exploration before showing the final path."""
        stack = [(self.start_pos, [self.start_pos])]
        visited = set([self.start_pos])
        
        def explore_step():
            if stack:
                current, path = stack.pop()
                
                # Draw exploration
                if current != self.start_pos and current != self.end_pos:
                    self.draw_exploration_circle(current[0], current[1])
                
                if current == self.end_pos:
                    self.path = path
                    self.root.after(100, self.animate_final_path)  # Faster transition
                    return
                
                # Explore neighbors
                for neighbor in self.graph.adjacent_list[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        stack.append((neighbor, new_path))
                
                self.root.after(10, explore_step)  # Much faster exploration
            else:
                self.animate_final_path()
        
        explore_step()

    def animate_dijkstra_exploration(self):
        """Animate Dijkstra's exploration before showing the final path."""
        costs = {v: float('inf') for v in self.graph.adjacent_list}
        costs[self.start_pos] = 0
        visited = {}
        pq = [(0, self.start_pos, [self.start_pos])]
        
        def explore_step():
            if pq:
                cost, current, path = heapq.heappop(pq)
                
                # Draw exploration
                if current != self.start_pos and current != self.end_pos:
                    self.draw_exploration_circle(current[0], current[1])
                
                if current == self.end_pos:
                    self.path = path
                    self.root.after(100, self.animate_final_path)  # Faster transition
                    return
                
                # Explore neighbors
                for neighbor in self.graph.adjacent_list[current]:
                    new_cost = cost + self.graph.adjacent_list[current][neighbor]
                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        visited[neighbor] = current
                        new_path = path + [neighbor]
                        heapq.heappush(pq, (new_cost, neighbor, new_path))
                
                self.root.after(10, explore_step)  # Much faster exploration
            else:
                self.animate_final_path()
        
        explore_step()

    def draw_exploration_circle(self, x, y):
        """Draw a circle to show exploration progress."""
        canvas_x, canvas_y = self.get_canvas_pos(x, y)
        center_x = canvas_x + self.grid_size / 2
        center_y = canvas_y + self.grid_size / 2
        radius = self.grid_size * 0.4
        
        # Draw exploration circle with fade effect
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill='#f1c40f',  # Yellow color for exploration
            outline='#f39c12',
            width=2,
            tags="exploration"
        )
        
        # Add a pulsing effect
        def pulse(step=0):
            if step < 3:  # Pulse 3 times
                radius = self.grid_size * (0.4 + 0.1 * step)
                self.canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    fill='',  # Transparent fill
                    outline='#f1c40f',
                    width=1,
                    tags="exploration"
                )
                self.root.after(100, lambda: pulse(step + 1))
        
        pulse()

    def animate_final_path(self):
        """Animate the final path after exploration."""
        self.canvas.delete("exploration")  # Clear exploration circles
        
        def draw_path_step(step):
            if step < len(self.path):
                x, y = self.path[step]
                if (x, y) != self.start_pos and (x, y) != self.end_pos:
                    self.draw_circle(x, y, '#2ecc71', 0.6, "path")
                self.root.after(20, lambda: draw_path_step(step + 1))  # Much faster path drawing
            else:
                self.draw_path_lines()
        
        draw_path_step(0)

    def draw_path_lines(self):
        if len(self.path) < 2:
            return
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            canvas_x1, canvas_y1 = self.get_canvas_pos(x1, y1)
            canvas_x2, canvas_y2 = self.get_canvas_pos(x2, y2)
            center_x1 = canvas_x1 + self.grid_size / 2
            center_y1 = canvas_y1 + self.grid_size / 2
            center_x2 = canvas_x2 + self.grid_size / 2
            center_y2 = canvas_y2 + self.grid_size / 2
            
            # Draw path line with shadow
            self.canvas.create_line(
                center_x1 + 2, center_y1 + 2,
                center_x2 + 2, center_y2 + 2,
                fill='#1a1a2e',  # Shadow color
                width=6,
                tags="path"
            )
            self.canvas.create_line(
                center_x1, center_y1,
                center_x2, center_y2,
                fill='#00ff9f',  # Bright green
                width=4,
                tags="path"
            )
            
            # Show weight if using random weights
            if self.weight_type.get() == "random":
                weight = self.graph.adjacent_list[(x1, y1)][(x2, y2)]
                mid_x = (center_x1 + center_x2) / 2
                mid_y = (center_y1 + center_y2) / 2
                # Draw weight background
                self.canvas.create_oval(
                    mid_x - 15, mid_y - 15,
                    mid_x + 15, mid_y + 15,
                    fill='#2c3e50',
                    outline='#ffffff',
                    width=2,
                    tags="path"
                )
                # Draw weight text
                self.canvas.create_text(
                    mid_x, mid_y,
                    text=str(weight),
                    fill='#ffffff',
                    font=('Arial', 10, 'bold'),
                    tags="path"
                )

    def update_display(self):
        """Update the display with modern styling."""
        self.canvas.delete("all")
        self.create_grid()
        
        # Draw obstacles
        for x, y in self.obstacles:
            self.draw_obstacle(x, y, "obstacle")
        
        # Draw path with modern styling
        if self.path:
            for x, y in self.path:
                if (x, y) != self.start_pos and (x, y) != self.end_pos:
                    self.draw_circle(x, y, '#00ff9f', 0.6, "path")
        
        # Draw start and end points as drones
        if self.start_pos:
            self.draw_drone(self.start_pos[0], self.start_pos[1], '#ff2e63', tag="start")
        if self.end_pos:
            self.draw_drone(self.end_pos[0], self.end_pos[1], '#4cc9f0', tag="end")
        
        # Draw path lines
        if len(self.path) >= 2:
            self.draw_path_lines()

    def reset_all(self):
        """Reset all variables and clear the display."""
        self.start_pos = None
        self.end_pos = None
        self.obstacles.clear()
        self.path = []
        self.visited.clear()
        self.backtrack.clear()
        self.start_drone_image = None
        self.end_drone_image = None
        self.canvas.delete("all")
        self.canvas.delete("exploration")
        self.create_grid()
        self.status_var.set("Reset complete! Click to place start point.")
        self.steps_label.config(text="Steps: 0")
        self.cost_label.config(text="")

    def show_algorithm_explanation(self):
        algorithm = self.algorithm.get()
        
        # Algorithm-specific details
        if algorithm == "BFS":
            details = """
🎯 BREADTH-FIRST SEARCH (BFS)

📝 DESCRIPTION:
• Explores all nodes at the current depth before moving to the next level
• Uses a queue data structure
• Guarantees the shortest path in terms of number of steps
• Perfect for unweighted graphs

⚙️ HOW IT WORKS:
1. Start at the source node (red)
2. Add all unvisited neighbors to a queue
3. Process nodes in the order they were discovered
4. Continue until the target is found or all nodes are visited

🔍 KEY CHARACTERISTICS:
• Level-by-level exploration
• Shortest path guaranteed
• Memory intensive for large graphs
• No consideration of edge weights

⏱️ COMPLEXITY:
• Time: O(V + E) where V = vertices, E = edges
• Space: O(V) for the queue

✅ BEST FOR:
• Finding shortest path in unweighted graphs
• When path length (steps) is more important than cost
• When memory is not a constraint
"""
        elif algorithm == "DFS":
            details = """
🎯 DEPTH-FIRST SEARCH (DFS)

📝 DESCRIPTION:
• Explores as far as possible along each branch before backtracking
• Uses a stack data structure (recursion or explicit stack)
• May not find the shortest path
• Good for exploring all possible paths

⚙️ HOW IT WORKS:
1. Start at the source node (red)
2. Explore one path as far as possible
3. Backtrack when reaching a dead end
4. Continue until target is found or all paths explored

🔍 KEY CHARACTERISTICS:
• Deep exploration before backtracking
• Memory efficient
• May find longer paths
• No consideration of edge weights

⏱️ COMPLEXITY:
• Time: O(V + E) where V = vertices, E = edges
• Space: O(V) for the recursion stack

✅ BEST FOR:
• Exploring all possible paths
• When memory is limited
• When complete traversal is needed
"""
        else:  # Dijkstra
            details = """
🎯 DIJKSTRA'S ALGORITHM

📝 DESCRIPTION:
• Finds the shortest path considering edge weights
• Uses a priority queue
• Guarantees the lowest-cost path
• Works with weighted graphs

⚙️ HOW IT WORKS:
1. Start at the source node (red)
2. Keep track of lowest cost to reach each node
3. Always explore the node with lowest current cost
4. Update costs when better paths are found
5. Continue until target is reached

🔍 KEY CHARACTERISTICS:
• Considers edge weights
• Guarantees lowest total cost path
• More complex than BFS/DFS
• Cannot handle negative weights

⏱️ COMPLEXITY:
• Time: O((V + E)logV) with binary heap
• Space: O(V) for the priority queue

✅ BEST FOR:
• Finding lowest-cost paths
• Weighted graphs
• When path cost matters more than steps
"""

        # Create and configure the explanation window
        explanation_window = tk.Toplevel(self.root)
        explanation_window.title(f"🧠 {algorithm} Algorithm Explanation")
        explanation_window.geometry("600x700")
        explanation_window.configure(bg='#2c3e50')
        explanation_window.transient(self.root)
        explanation_window.grab_set()

        # Create text frame with scrollbar
        text_frame = tk.Frame(explanation_window, bg='#2c3e50')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Arial', 11),
                             bg='#ecf0f1', fg='#2c3e50', padx=15, pady=15)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Insert the algorithm-specific explanation
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        
        # Add close button
        close_btn = tk.Button(explanation_window, text="✅ Got It!",
                             command=explanation_window.destroy,
                             bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                             padx=20, pady=10)
        close_btn.pack(pady=10)

    def load_drone_image(self, drone_type):
        """Load a custom image for the drone."""
        file_path = filedialog.askopenfilename(
            title=f"Select {drone_type} drone image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Load and resize image
                image = Image.open(file_path)
                image = image.resize((int(self.drone_size), int(self.drone_size)), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                if drone_type == 'start':
                    self.start_drone_image = photo
                else:
                    self.end_drone_image = photo
                
                # Update display if drones are already placed
                self.update_display()
                self.status_var.set(f"{drone_type.capitalize()} drone image loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

def main():
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()
