import pygame
import sys
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import deque
import heapq
import time

# Node class
class Node:
    def __init__(self, pygame_instance, screen, w, h, rows, cols, x, y):
        self.pygame = pygame_instance
        self.screen = screen
        self.w = w
        self.h = h
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.is_obstacle = False
        self.weight = 1
        self.color = None
        
    def show(self, color, border_width=0):
        self.color = color
        x_pixel = self.x * self.w
        y_pixel = self.y * self.h
        
        if border_width > 0:
            # Draw border
            self.pygame.draw.rect(self.screen, (0, 0, 0), 
                                (x_pixel, y_pixel, self.w, self.h), border_width)
        else:
            # Fill the cell
            self.pygame.draw.rect(self.screen, color, 
                                (x_pixel, y_pixel, self.w, self.h))
            # Add subtle border for better visibility
            self.pygame.draw.rect(self.screen, (200, 200, 200), 
                                (x_pixel, y_pixel, self.w, self.h), 1)

# Fixed maze and weights data
fixed_maze = [
    [1] * 50 if i == 0 or i == 49 else 
    [1] + [0] * 48 + [1] if 1 <= i <= 48 else []
    for i in range(50)
]

# Add some internal walls to the fixed maze
for i in range(5, 45, 10):
    for j in range(5, 45):
        if j != 25:  # Leave gaps for paths
            fixed_maze[i][j] = 1

fixed_weights = [
    [random.randint(1, 15) for _ in range(50)]
    for _ in range(50)
]

class Graph:
    def __init__(self, grid, cols, rows):
        self.adjacent_list = {}
        self.grid = grid
        self.cols = cols
        self.rows = rows
        self.build_graph()

    def add_vertex(self, vertex):
        if vertex not in self.adjacent_list:
            self.adjacent_list[vertex] = {}
    
    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacent_list[u][v] = weight
        self.adjacent_list[v][u] = weight  

    def build_graph(self):
        self.adjacent_list.clear()
        self.add_vertices()
        self.add_edges()
 
    def add_vertices(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if not self.grid[x][y].is_obstacle:
                    self.add_vertex((x, y))

    def add_edges(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if not self.grid[x][y].is_obstacle:
                    # Check all four directions
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.cols and 0 <= ny < self.rows and 
                            not self.grid[nx][ny].is_obstacle):
                            self.add_edge((x, y), (nx, ny), self.grid[nx][ny].weight)

    def dijkstra(self, start, end, visualizer):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        costs = {v: float('inf') for v in self.adjacent_list}
        costs[start] = 0
        visited = {}
        pq = [(0, start)]
        open_set = set([start])
        closed_set = set()

        while pq:
            current_cost, node = heapq.heappop(pq)
            
            if node == end:
                path = []
                cur = end
                while cur in visited:
                    path.insert(0, cur)
                    cur = visited[cur]
                if path:
                    path.insert(0, start)
                return path, costs[end]

            if node in closed_set:
                continue
                
            open_set.discard(node)
            closed_set.add(node)
            
            # Animate visited node
            if node != start and visualizer.show_steps:
                visualizer.animate_node(node, visualizer.purple, "visited")

            for neighbor in self.adjacent_list[node]:
                if neighbor not in closed_set:
                    edge_weight = self.adjacent_list[node][neighbor]
                    new_cost = costs[node] + edge_weight
                    
                    if new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        visited[neighbor] = node
                        heapq.heappush(pq, (new_cost, neighbor))
                        
                        if neighbor not in open_set:
                            open_set.add(neighbor)
                            # Animate frontier node
                            if visualizer.show_steps:
                                visualizer.animate_node(neighbor, visualizer.teal, "frontier")
        
        return None, None

    def bfs(self, start, end, visualizer):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        queue = deque([[start]])
        visited = set()
        distances = {start: 0}
        open_set = set([start])
        closed_set = set()

        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node not in visited:
                visited.add(node)
                closed_set.add(node)
                open_set.discard(node)
                
                # Animate visited node
                if node != start and visualizer.show_steps:
                    visualizer.animate_node(node, visualizer.purple, "visited")

                if node == end:
                    return path, distances[node]

                for adj in self.adjacent_list[node]:
                    if adj not in visited:
                        new_path = list(path)
                        new_path.append(adj)
                        queue.append(new_path)
                        distances[adj] = distances[node] + 1
                        
                        if adj not in open_set:
                            open_set.add(adj)
                            # Animate frontier node
                            if visualizer.show_steps:
                                visualizer.animate_node(adj, visualizer.teal, "frontier")
        
        return None, None

    def dfs(self, start, end, visualizer):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        stack = [[start]]
        visited = set()
        open_set = set([start])
        closed_set = set()

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == end:
                return path, len(path)

            if node not in visited:
                visited.add(node)
                open_set.discard(node)
                closed_set.add(node)
                
                # Animate visited node
                if node != start and visualizer.show_steps:
                    visualizer.animate_node(node, visualizer.purple, "visited")

                for neighbor in self.adjacent_list.get(node, []):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        stack.append(new_path)
                        
                        if neighbor not in open_set:
                            open_set.add(neighbor)
                            # Animate frontier node
                            if visualizer.show_steps:
                                visualizer.animate_node(neighbor, visualizer.teal, "frontier")

        return None, None

class PathfindingGameUI:
    def __init__(self, window):
        self.window = window
        self.window.title("🎯 Pathfinding Visualizer Configuration")
        self.window.geometry("500x600")
        self.window.configure(bg='#f0f0f0')
        
        # Make window non-resizable but centered
        self.window.resizable(False, False)
        self.center_window()

        # Variables
        self.algorithm_var = tk.StringVar(value='Dijkstra')
        self.maze_var = tk.StringVar(value='Blank')
        self.weight_var = tk.StringVar(value='All Weights 1')
        self.show_steps_var = tk.IntVar(value=1)
        self.animation_speed_var = tk.IntVar(value=50)

        # Choices
        self.algorithms = ['Dijkstra', 'DFS', 'BFS']
        self.maze_types = ['Blank', 'Fixed Maze', 'Random']
        self.weight_types = ['All Weights 1', 'Fixed Weights', 'Random Weights']

        # Start and end coordinates
        self.start = (5, 5)
        self.end = (45, 45)

        self.setup_ui()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.window, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🚀 Pathfinding Visualizer", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack()

        # Main container
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(padx=30, pady=10, fill='both', expand=True)

        # Coordinates section
        coord_frame = tk.LabelFrame(main_frame, text="📍 Coordinates", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#34495e')
        coord_frame.pack(fill='x', pady=10)

        # Start coordinates
        start_frame = tk.Frame(coord_frame, bg='#f0f0f0')
        start_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(start_frame, text="Start (x,y):", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#27ae60').pack(side='left')
        self.start_entry = tk.Entry(start_frame, font=('Arial', 10), width=15)
        self.start_entry.pack(side='right')
        self.start_entry.insert(0, "5,5")

        # End coordinates
        end_frame = tk.Frame(coord_frame, bg='#f0f0f0')
        end_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(end_frame, text="End (x,y):", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', fg='#e74c3c').pack(side='left')
        self.end_entry = tk.Entry(end_frame, font=('Arial', 10), width=15)
        self.end_entry.pack(side='right')
        self.end_entry.insert(0, "45,45")

        # Algorithm section
        algo_frame = tk.LabelFrame(main_frame, text="🧠 Algorithm", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#34495e')
        algo_frame.pack(fill='x', pady=10)

        for i, algo in enumerate(self.algorithms):
            rb = tk.Radiobutton(algo_frame, text=algo, variable=self.algorithm_var, 
                               value=algo, font=('Arial', 10), bg='#f0f0f0',
                               command=self.on_algorithm_change)
            rb.pack(anchor='w', padx=10, pady=2)

        # Settings section
        settings_frame = tk.LabelFrame(main_frame, text="⚙️ Settings", 
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#34495e')
        settings_frame.pack(fill='x', pady=10)

        # Show steps checkbox
        steps_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        steps_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Checkbutton(steps_frame, text="Show Animation Steps", 
                      variable=self.show_steps_var, font=('Arial', 10), 
                      bg='#f0f0f0').pack(anchor='w')

        # Animation speed
        speed_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(speed_frame, text="Animation Speed:", font=('Arial', 10), 
                bg='#f0f0f0').pack(anchor='w')
        speed_scale = tk.Scale(speed_frame, from_=1, to=100, orient='horizontal',
                              variable=self.animation_speed_var, bg='#f0f0f0')
        speed_scale.pack(fill='x', pady=2)

        # Maze type
        maze_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        maze_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(maze_frame, text="Maze Layout:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        maze_combo = ttk.Combobox(maze_frame, textvariable=self.maze_var, 
                                 values=self.maze_types, state='readonly', width=20)
        maze_combo.pack(anchor='w', pady=2)

        # Weight type
        weight_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        weight_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(weight_frame, text="Weight Configuration:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0').pack(anchor='w')
        self.weight_combo = ttk.Combobox(weight_frame, textvariable=self.weight_var, 
                                        values=self.weight_types, state='readonly', width=20)
        self.weight_combo.pack(anchor='w', pady=2)

        # Instructions
        info_frame = tk.LabelFrame(main_frame, text="ℹ️ Instructions", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#34495e')
        info_frame.pack(fill='x', pady=10)

        instructions = [
            "• Coordinates range: 1 ≤ x,y ≤ 48",
            "• Use mouse to draw/erase walls in the visualizer",
            "• Press SPACE to start the pathfinding",
            "• Green = Start, Red = End, Black = Walls",
            "• Light Blue = Frontier, Purple = Visited, Blue = Path"
        ]

        for instruction in instructions:
            tk.Label(info_frame, text=instruction, font=('Arial', 9), 
                    bg='#f0f0f0', fg='#7f8c8d').pack(anchor='w', padx=10, pady=1)

        # Start button
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="🚀 Start Visualization", 
                                     font=('Arial', 14, 'bold'), bg='#3498db', fg='white',
                                     padx=30, pady=10, command=self.on_submit,
                                     cursor='hand2')
        self.start_button.pack()

    def on_algorithm_change(self):
        # Disable weight options for non-Dijkstra algorithms
        if self.algorithm_var.get() != 'Dijkstra':
            self.weight_combo.configure(state='disabled')
            self.weight_var.set('All Weights 1')
        else:
            self.weight_combo.configure(state='readonly')

    def on_submit(self):
        try:
            # Parse coordinates
            start_coords = self.start_entry.get().strip().split(',')
            end_coords = self.end_entry.get().strip().split(',')
            
            if len(start_coords) != 2 or len(end_coords) != 2:
                raise ValueError("Invalid coordinate format")
            
            start_x, start_y = int(start_coords[0]), int(start_coords[1])
            end_x, end_y = int(end_coords[0]), int(end_coords[1])
            
            # Validate coordinates
            if not (1 <= start_x <= 48 and 1 <= start_y <= 48 and 
                    1 <= end_x <= 48 and 1 <= end_y <= 48):
                raise ValueError("Coordinates out of range")
                
            self.start = (start_x, start_y)
            self.end = (end_x, end_y)
            
            # Close the window
            self.window.quit()
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Input Error", 
                               "Please enter valid coordinates (x,y) between 1 and 48!")

class PathfindingVisualizer:
    def __init__(self):
        pygame.init()
        
        # Screen settings
        self.screen_w = 900
        self.screen_h = 900
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("🎯 Pathfinding Visualizer")
        
        # Grid settings
        self.cols = 50
        self.rows = 50
        self.cell_w = self.screen_w / self.cols
        self.cell_h = self.screen_h / self.rows
        
        # Colors
        self.purple = (155, 89, 182)      # Visited nodes
        self.teal = (52, 152, 219)        # Frontier nodes
        self.blue = (41, 128, 185)        # Final path
        self.black = (44, 62, 80)         # Obstacles
        self.white = (236, 240, 241)      # Background
        self.green = (46, 204, 113)       # Start node
        self.red = (231, 76, 60)          # End node
        self.gray = (149, 165, 166)       # Grid lines
        
        # Weight colors (lighter to darker gray/blue)
        self.weight_colors = []
        for i in range(15):
            intensity = 255 - (i * 12)
            self.weight_colors.append((intensity, intensity, min(255, intensity + 20)))
        
        # Animation settings
        self.animation_delay = 0.05
        self.show_steps = True
        
        # Initialize
        self.grid = []
        self.graph = None
        self.ui = None
        self.start_node = None
        self.end_node = None
        self.clock = pygame.time.Clock()
        
        self.create_grid()

    def create_grid(self):
        self.grid = []
        for x in range(self.cols):
            row = []
            for y in range(self.rows):
                node = Node(pygame, self.screen, self.cell_w, self.cell_h, 
                           self.rows, self.cols, x, y)
                row.append(node)
            self.grid.append(row)
        
        self.graph = Graph(self.grid, self.cols, self.rows)

    def setup_ui(self):
        window = tk.Tk()
        self.ui = PathfindingGameUI(window)
        window.mainloop()

    def draw_grid(self):
        self.screen.fill(self.white)
        
        # Draw all cells
        for x in range(self.cols):
            for y in range(self.rows):
                self.grid[x][y].show(self.white, 0)
        
        # Draw grid lines
        for x in range(self.cols + 1):
            pygame.draw.line(self.screen, self.gray, 
                           (x * self.cell_w, 0), (x * self.cell_w, self.screen_h), 1)
        for y in range(self.rows + 1):
            pygame.draw.line(self.screen, self.gray, 
                           (0, y * self.cell_h), (self.screen_w, y * self.cell_h), 1)

    def draw_borders(self):
        for i in range(self.rows):
            # Borders
            for border_cell in [(0, i), (self.cols-1, i), (i, 0), (i, self.rows-1)]:
                if 0 <= border_cell[0] < self.cols and 0 <= border_cell[1] < self.rows:
                    self.grid[border_cell[0]][border_cell[1]].is_obstacle = True
                    self.grid[border_cell[0]][border_cell[1]].show(self.black, 0)

    def apply_maze_layout(self):
        if self.ui.maze_var.get() == 'Random':
            for i in range(1, self.cols-1):
                for j in range(1, self.rows-1):
                    if (random.choice([1, 2, 3, 4, 5]) == 2 and 
                        (i, j) != self.ui.start and (i, j) != self.ui.end):
                        self.grid[i][j].is_obstacle = True
                        self.grid[i][j].show(self.black, 0)
        elif self.ui.maze_var.get() == 'Fixed Maze':
            for i in range(self.cols):
                for j in range(self.rows):
                    if (j < len(fixed_maze) and i < len(fixed_maze[j]) and
                        fixed_maze[j][i] == 1 and 
                        (i, j) != self.ui.start and (i, j) != self.ui.end):
                        self.grid[i][j].is_obstacle = True
                        self.grid[i][j].show(self.black, 0)

    def apply_weights(self):
        if self.ui.weight_var.get() == 'Random Weights':
            for i in range(1, self.cols-1):
                for j in range(1, self.rows-1):
                    if (not self.grid[i][j].is_obstacle and 
                        (i, j) != self.ui.start and (i, j) != self.ui.end):
                        weight = random.randint(1, 15)
                        self.grid[i][j].weight = weight
                        color = self.weight_colors[weight-1]
                        self.grid[i][j].show(color, 0)
        elif self.ui.weight_var.get() == 'Fixed Weights':
            for i in range(self.cols):
                for j in range(self.rows):
                    if (not self.grid[i][j].is_obstacle and 
                        (i, j) != self.ui.start and (i, j) != self.ui.end and
                        j < len(fixed_weights) and i < len(fixed_weights[j])):
                        weight = fixed_weights[j][i]
                        self.grid[i][j].weight = weight
                        color = self.weight_colors[weight-1]
                        self.grid[i][j].show(color, 0)

    def animate_node(self, pos, color, node_type):
        if not self.show_steps:
            return
            
        x, y = pos
        self.grid[x][y].show(color, 0)
        
        # Update display
        pygame.display.update()
        
        # Control animation speed
        time.sleep(self.animation_delay)
        
        # Handle events to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run_pathfinding(self):
        start_pos = self.ui.start
        end_pos = self.ui.end
        
        # Set animation parameters
        self.show_steps = bool(self.ui.show_steps_var.get())
        self.animation_delay = (101 - self.ui.animation_speed_var.get()) / 1000.0

        path, cost = None, None

        if self.ui.algorithm_var.get() == 'Dijkstra':
            path, cost = self.graph.dijkstra(start_pos, end_pos, self)
        elif self.ui.algorithm_var.get() == 'BFS':
            path, cost = self.graph.bfs(start_pos, end_pos, self)
        elif self.ui.algorithm_var.get() == 'DFS':
            path, cost = self.graph.dfs(start_pos, end_pos, self)

        return path, cost

    def display_path(self, path):
        if path:
            # Animate path drawing
            for i, (x, y) in enumerate(path):
                if i == 0:
                    self.grid[x][y].show(self.green, 0)  # Start
                elif i == len(path) - 1:
                    self.grid[x][y].show(self.red, 0)    # End
                else:
                    self.grid[x][y].show(self.blue, 0)   # Path
                
                pygame.display.update()
                time.sleep(0.1)  # Path animation delay

    def handle_mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if mouse_pressed[0] or mouse_pressed[2]:  # Left or right click
            grid_x = int(mouse_pos[0] // self.cell_w)
            grid_y = int(mouse_pos[1] // self.cell_h)
            
            if (0 < grid_x < self.cols-1 and 0 < grid_y < self.rows-1 and
                (grid_x, grid_y) != self.ui.start and (grid_x, grid_y) != self.ui.end):
                
                if mouse_pressed[0]:  # Left click - add wall
                    self.grid[grid_x][grid_y].is_obstacle = True
                    self.grid[grid_x][grid_y].show(self.black, 0)
                elif mouse_pressed[2]:  # Right click - remove wall
                    self.grid[grid_x][grid_y].is_obstacle = False
                    self.grid[grid_x][grid_y].show(self.white, 0)
                
                # Rebuild graph when walls change
                self.graph.build_graph()

    def show_result(self, path, cost):
        if path:
            algorithm = self.ui.algorithm_var.get()
            if algorithm == 'Dijkstra':
                message = f"Shortest weighted path found!\nTotal cost: {cost}"
            else:
                message = f"Path found using {algorithm}!\nPath length: {cost} steps"
            
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askyesno('🎉 Path Found!', 
                                       f'{message}\n\nWould you like to run another visualization?')
            root.destroy()
            return "restart" if result else "exit"
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo('❌ No Path Found', 
                              'No path exists between start and end points!')
            root.destroy()
            return "exit"

    def run(self):
        # Setup UI
        self.setup_ui()
        
        if not hasattr(self.ui, 'start'):
            return

        # Set start and end nodes
        self.start_node = self.grid[self.ui.start[0]][self.ui.start[1]]
        self.end_node = self.grid[self.ui.end[0]][self.ui.end[1]]

        # Setup visualization
        self.draw_grid()
        self.draw_borders()
        self.apply_maze_layout()
        self.apply_weights()
        self.graph.build_graph()

        # Show start and end nodes
        self.start_node.show(self.green, 0)
        self.end_node.show(self.red, 0)

        pygame.display.update()

        # Main game loop
        running = True
        pathfinding_started = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not pathfinding_started:
                        pathfinding_started = True
                        
                        # Run pathfinding
                        path, cost = self.run_pathfinding()
                        
                        # Display result
                        self.display_path(path)
                        
                        # Show result dialog
                        action = self.show_result(path, cost)
                        
                        if action == "restart":
                            pygame.quit()
                            visualizer = PathfindingVisualizer()
                            visualizer.run()
                            return
                        else:
                            running = False
                    elif event.key == pygame.K_r:  # Reset
                        # Reset the grid to initial state
                        self.create_grid()
                        self.draw_grid()
                        self.draw_borders()
                        self.apply_maze_layout()
                        self.apply_weights()
                        self.graph.build_graph()
                        
                        # Reset start and end nodes
                        self.start_node = self.grid[self.ui.start[0]][self.ui.start[1]]
                        self.end_node = self.grid[self.ui.end[0]][self.ui.end[1]]
                        self.start_node.show(self.green, 0)
                        self.end_node.show(self.red, 0)
                        
                        # Reset pathfinding state
                        pathfinding_started = False
                        
                        pygame.display.update()
                
                # Handle mouse input for drawing/erasing walls
                if not pathfinding_started:
                    self.handle_mouse_input()
            
            # Cap the frame rate
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    visualizer = PathfindingVisualizer()
    visualizer.run()