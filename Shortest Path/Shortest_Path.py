import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import random
import math
import heapq


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
        self.adjacent_list[v][u] = weight  # for undirected graph

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

        distances = {v: float('inf') for v in self.adjacent_list}
        distances[start] = 0
        prev = {}
        pq = [(0, start)]

        while pq:
            dist, node = heapq.heappop(pq)

            if node == end:
                break

            if dist > distances[node]:
                continue

            for nbr in self.adjacent_list[node]:
                # FIX: Use actual edge weight instead of hardcoded 1
                edge_weight = self.adjacent_list[node][nbr]
                new_distance = dist + edge_weight

                if new_distance < distances[nbr]:
                    distances[nbr] = new_distance
                    prev[nbr] = node
                    heapq.heappush(pq, (new_distance, nbr))

        # Reconstruct path
        path = []
        cur = end
        while cur in prev:
            path.insert(0, cur)
            cur = prev[cur]

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
        self.root.title("🎯 Pathfinding Visualizer")
        self.root.geometry("1250x800")
        self.root.configure(bg='#2c3e50')

        # Grid settings
        self.grid_size = 20
        self.canvas_width = 800
        self.canvas_height = 500
        self.rows = self.canvas_height // self.grid_size
        self.cols = self.canvas_width // self.grid_size

        # Game state
        self.start_pos = None
        self.end_pos = None
        self.obstacles = set()
        self.path = []
        self.dragging = None
        self.graph = Graph()
        self.mode = "place_points"
        self.setup_ui()
        self.create_grid()

    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        title_label = tk.Label(title_frame, text="🎯 Interactive Pathfinding Visualizer",
                               font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()

        # Instructions
        instructions = tk.Label(self.root,
                                text="🔴 Red = Start | ⚫ Black = End | 🟡 Yellow = Obstacles | 🟢 Green = Path",
                                font=('Arial', 12), fg='#bdc3c7', bg='#2c3e50')
        instructions.pack(pady=5)

        # Mode selection frame
        mode_frame = tk.Frame(self.root, bg='#2c3e50')
        mode_frame.pack(pady=5)

        self.mode_var = tk.StringVar(value="place_points")
        tk.Radiobutton(mode_frame, text="🎯 Place Start/End Points", variable=self.mode_var, value="place_points",
                       command=self.change_mode, bg='#2c3e50', fg='#ecf0f1', selectcolor='#34495e',
                       font=('Arial', 11)).pack(side='left', padx=10)
        tk.Radiobutton(mode_frame, text="🧱 Draw Obstacles", variable=self.mode_var, value="draw_obstacles",
                       command=self.change_mode, bg='#2c3e50', fg='#ecf0f1', selectcolor='#34495e',
                       font=('Arial', 11)).pack(side='left', padx=10)

        # Control buttons and algorithm select bar
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)

        button_style = {
            'font': ('Arial', 12, 'bold'),
            'relief': 'flat',
            'bd': 0,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }

        self.find_path_btn = tk.Button(control_frame, text="🔍 Find Shortest Path",
                                       command=self.find_path,
                                       bg='#3498db', fg='white', **button_style)
        self.find_path_btn.grid(row=0, column=0, padx=5)

        self.reset_btn = tk.Button(control_frame, text="🔄 Reset Everything",
                                   command=self.reset_all,
                                   bg='#e74c3c', fg='white', **button_style)
        self.reset_btn.grid(row=0, column=1, padx=5)

        self.clear_obstacles_btn = tk.Button(control_frame, text="🧹 Clear Obstacles",
                                             command=self.clear_obstacles,
                                             bg='#e67e22', fg='white', **button_style)
        self.clear_obstacles_btn.grid(row=0, column=2, padx=5)

        self.generate_obstacles_btn = tk.Button(control_frame, text="🎲 Generate Random",
                                                command=self.generate_random_obstacles,
                                                bg='#f39c12', fg='white', **button_style)
        self.generate_obstacles_btn.grid(row=0, column=3, padx=5)

        self.explain_btn = tk.Button(control_frame, text="📚 How It Works",
                                     command=self.show_algorithm_explanation,
                                     bg='#9b59b6', fg='white', **button_style)
        self.explain_btn.grid(row=0, column=4, padx=5)

        # Algorithm selection bar
        self.algorithm = tk.StringVar(value="BFS")
        algo_label = tk.Label(control_frame, text="Algorithm:", font=('Arial', 12), bg='#2c3e50', fg='white')
        algo_label.grid(row=0, column=5, padx=5)
        algo_menu = ttk.Combobox(control_frame, textvariable=self.algorithm, state="readonly",
                                 values=["BFS", "DFS", "Dijkstra"], width=10)
        algo_menu.grid(row=0, column=6, padx=5)

        # Canvas frame with border
        canvas_frame = tk.Frame(self.root, bg='#34495e', relief='ridge', bd=3)
        canvas_frame.pack(pady=20)

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height,
                                bg='#ecf0f1', highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)

        # Bind events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_hover)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready! Select mode and click to place start (red) and end (black) points.")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                              font=('Arial', 10), fg='#ecf0f1', bg='#34495e',
                              relief='sunken', bd=1, anchor='w', padx=10)
        status_bar.pack(fill='x', side='bottom')

    def create_grid(self):
        for i in range(0, self.canvas_width, self.grid_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill='#bdc3c7', width=1)
        for i in range(0, self.canvas_height, self.grid_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill='#bdc3c7', width=1)

    def change_mode(self):
        self.mode = self.mode_var.get()
        if self.mode == "place_points":
            self.status_var.set("Mode: Place Start/End Points. Click to place or drag existing points.")
        else:
            self.status_var.set("Mode: Draw Obstacles. Click and drag to create/remove obstacles.")

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
        x, y = self.get_canvas_pos(grid_x, grid_y)
        padding = 2
        shadow_offset = 2
        self.canvas.create_rectangle(x + padding + shadow_offset,
                                     y + padding + shadow_offset,
                                     x + self.grid_size - padding + shadow_offset,
                                     y + self.grid_size - padding + shadow_offset,
                                     fill='#7f8c8d', outline='', tags=tag)
        return self.canvas.create_rectangle(x + padding, y + padding,
                                            x + self.grid_size - padding,
                                            y + self.grid_size - padding,
                                            fill=color, outline='white', width=2, tags=tag)

    def on_click(self, event):
        grid_x, grid_y = self.get_grid_pos(event.x, event.y)

        if self.mode == "place_points":
            self.handle_point_placement(grid_x, grid_y)
        else:  # draw_obstacles mode
            self.handle_obstacle_drawing(grid_x, grid_y)

    def handle_point_placement(self, grid_x, grid_y):
        # Check if clicking on existing start or end point to drag them
        if self.start_pos and self.start_pos == (grid_x, grid_y):
            self.dragging = 'start'
            return
        elif self.end_pos and self.end_pos == (grid_x, grid_y):
            self.dragging = 'end'
            return

        # Check if clicking on obstacle - remove it
        if (grid_x, grid_y) in self.obstacles:
            self.obstacles.remove((grid_x, grid_y))
            self.update_display()
            self.status_var.set("Obstacle removed!")
            return

        # Place start or end point
        if not self.start_pos:
            self.start_pos = (grid_x, grid_y)
            self.status_var.set("Start point placed! Now place the end point (black).")
        elif not self.end_pos:
            self.end_pos = (grid_x, grid_y)
            self.status_var.set("End point placed! Switch to 'Draw Obstacles' mode or click 'Find Path'.")
        else:
            # Both points exist, allow user to replace them
            if messagebox.askyesno("Replace Point", "Both start and end points exist. Replace start point?"):
                self.start_pos = (grid_x, grid_y)
                self.status_var.set("Start point moved!")
            else:
                self.end_pos = (grid_x, grid_y)
                self.status_var.set("End point moved!")

        self.update_display()

    def handle_obstacle_drawing(self, grid_x, grid_y):
        if (grid_x, grid_y) == self.start_pos or (grid_x, grid_y) == self.end_pos:
            self.status_var.set("Cannot place obstacle on start or end point!")
            return

        if (grid_x, grid_y) in self.obstacles:
            self.obstacles.remove((grid_x, grid_y))
            self.status_var.set(f"Obstacle removed at ({grid_x}, {grid_y})")
        else:
            self.obstacles.add((grid_x, grid_y))
            self.status_var.set(f"Obstacle added at ({grid_x}, {grid_y})")

        self.update_display()

    def on_drag(self, event):
        grid_x, grid_y = self.get_grid_pos(event.x, event.y)
        grid_x = max(0, min(grid_x, self.cols - 1))
        grid_y = max(0, min(grid_y, self.rows - 1))

        if self.mode == "place_points" and self.dragging:
            if self.dragging == 'start':
                self.start_pos = (grid_x, grid_y)
            elif self.dragging == 'end':
                self.end_pos = (grid_x, grid_y)
            self.update_display()
        elif self.mode == "draw_obstacles":
            # Continuous obstacle drawing while dragging
            if (grid_x, grid_y) != self.start_pos and (grid_x, grid_y) != self.end_pos:
                self.obstacles.add((grid_x, grid_y))
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

    def clear_obstacles(self):
        """Clear all obstacles"""
        self.obstacles.clear()
        self.path = []
        self.update_display()
        self.status_var.set("All obstacles cleared!")

    def generate_random_obstacles(self):
        if not self.start_pos or not self.end_pos:
            messagebox.showwarning("Warning", "Please place start and end points first!")
            return
        self.obstacles.clear()
        patterns = ['maze_walls', 'spiral', 'clusters', 'corridors']
        chosen_pattern = random.choice(patterns)
        if chosen_pattern == 'maze_walls':
            self.generate_maze_walls()
        elif chosen_pattern == 'spiral':
            self.generate_spiral_obstacles()
        elif chosen_pattern == 'clusters':
            self.generate_cluster_obstacles()
        else:
            self.generate_corridor_obstacles()
        self.ensure_path_exists()
        self.update_display()
        self.status_var.set(f"Generated {len(self.obstacles)} connected obstacles! Pattern: {chosen_pattern.title()}")

    def generate_maze_walls(self):
        for wall_x in range(5, self.cols, 8):
            for y in range(1, self.rows - 1):
                if random.random() < 0.7:
                    pos = (wall_x, y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)
        for wall_y in range(5, self.rows, 6):
            for x in range(1, self.cols - 1):
                if random.random() < 0.6:
                    pos = (x, wall_y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)

    def generate_spiral_obstacles(self):
        center_x, center_y = self.cols // 2, self.rows // 2
        max_radius = min(center_x, center_y) - 2
        for radius in range(2, max_radius, 3):
            angles = range(0, 360, 15)
            for angle in angles:
                x = center_x + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    pos = (x, y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)

    def generate_cluster_obstacles(self):
        num_clusters = random.randint(4, 7)
        for _ in range(num_clusters):
            cluster_x = random.randint(3, self.cols - 4)
            cluster_y = random.randint(3, self.rows - 4)
            cluster_size = random.randint(8, 15)
            for _ in range(cluster_size):
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-3, 3)
                x = cluster_x + offset_x
                y = cluster_y + offset_y
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    pos = (x, y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)

    def generate_corridor_obstacles(self):
        for corridor_y in [self.rows // 4, 3 * self.rows // 4]:
            for x in range(self.cols):
                if random.random() < 0.8:
                    pos = (x, corridor_y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)
                    pos2 = (x, corridor_y + 1 if corridor_y < self.rows - 1 else corridor_y - 1)
                    if pos2 != self.start_pos and pos2 != self.end_pos:
                        self.obstacles.add(pos2)
        for corridor_x in [self.cols // 3, 2 * self.cols // 3]:
            for y in range(self.rows):
                if random.random() < 0.7:
                    pos = (corridor_x, y)
                    if pos != self.start_pos and pos != self.end_pos:
                        self.obstacles.add(pos)

    def ensure_path_exists(self):
        max_attempts = 5
        for attempt in range(max_attempts):
            self.build_graph()
            test_path = self.graph.bfs(self.start_pos, self.end_pos)
            if test_path:
                break
            obstacles_to_remove = random.sample(list(self.obstacles),
                                                min(len(self.obstacles) // 4, 10))
            for obs in obstacles_to_remove:
                self.obstacles.remove(obs)

    def build_graph(self):
        self.graph = Graph()
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in self.obstacles:
                    self.graph.add_vertex((x, y))

        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in self.obstacles:
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.cols and 0 <= ny < self.rows and
                                (nx, ny) not in self.obstacles):
                            weight = random.randint(1, 15)  # Random weight between 1 and 15
                            self.graph.add_edge((x, y), (nx, ny), weight)

    def find_path(self):
        if not self.start_pos or not self.end_pos:
            messagebox.showwarning("Warning", "Please place both start and end points!")
            return
        self.build_graph()
        algorithm = self.algorithm.get()
        if algorithm == "BFS":
            path = self.graph.bfs(self.start_pos, self.end_pos)
        elif algorithm == "DFS":
            path = self.graph.dfs(self.start_pos, self.end_pos)
        else:
            path = self.graph.dijkstra(self.start_pos, self.end_pos)
        if path:
            self.path = path
            self.animate_path_finding()
            self.status_var.set(f"{algorithm} Path found! Length: {len(path)} steps")
        else:
            messagebox.showinfo("No Path", f"No path found using {algorithm}!")
            self.status_var.set("No path found! Try removing some obstacles.")

    def animate_path_finding(self):
        self.canvas.delete("path")

        def draw_path_step(step):
            if step < len(self.path):
                x, y = self.path[step]
                if (x, y) != self.start_pos and (x, y) != self.end_pos:
                    self.draw_circle(x, y, '#2ecc71', 0.6, "path")
                self.root.after(100, lambda: draw_path_step(step + 1))
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
            self.canvas.create_line(center_x1, center_y1, center_x2, center_y2,
                                    fill='#27ae60', width=4, tags="path")

    def update_display(self):
        """Update the visual display"""
        self.canvas.delete("start")
        self.canvas.delete("end")
        self.canvas.delete("obstacle")
        self.canvas.delete("path")

        # Draw obstacles
        for x, y in self.obstacles:
            self.draw_square(x, y, '#f1c40f', "obstacle")

        # Draw start point
        if self.start_pos:
            self.draw_circle(self.start_pos[0], self.start_pos[1], '#e74c3c', tag="start")

        # Draw end point
        if self.end_pos:
            self.draw_circle(self.end_pos[0], self.end_pos[1], '#2c3e50', tag="end")

        # Redraw path if it exists
        if self.path:
            for x, y in self.path:
                if (x, y) != self.start_pos and (x, y) != self.end_pos:
                    self.draw_circle(x, y, '#2ecc71', 0.6, "path")
            self.draw_path_lines()

    def reset_all(self):
        """Reset everything"""
        self.start_pos = None
        self.end_pos = None
        self.obstacles = set()
        self.path = []
        self.canvas.delete("start")
        self.canvas.delete("end")
        self.canvas.delete("obstacle")
        self.canvas.delete("path")
        self.status_var.set("Reset complete! Select mode and click to place start point (red).")

    def show_algorithm_explanation(self):
        explanation = f"""
🔍 HOW THE PATHFINDING ALGORITHM WORKS

📊 ALGORITHM: {self.algorithm.get()}

⚙️ HOW IT WORKS:
1️⃣ Start at the red point (start position)
2️⃣ {"Explore neighbors level by level" if self.algorithm.get() == "BFS" else
        "Explore one path deeply" if self.algorithm.get() == "DFS" else
        "Find path with lowest total weight"}
3️⃣ {"Ignore weights, find shortest path" if self.algorithm.get() == "BFS" else
        "Ignore weights, find any path" if self.algorithm.get() == "DFS" else
        "Consider weights, find lowest cost path"}
4️⃣ Find the black point (end position)
5️⃣ Show final path (green)

🧠 ALGORITHM DIFFERENCES:
• BFS: Shortest path by steps (ignores weights)
• DFS: Any valid path (ignores weights)  
• Dijkstra: Shortest path by total weight

⏱️ COMPLEXITY:
• Time: O(V + E)
• Space: O(V)

✅ {"Shortest path by steps (BFS)" if self.algorithm.get() == "BFS" else
        "Any valid path (DFS)" if self.algorithm.get() == "DFS" else
        "Shortest path by total weight (Dijkstra)"}! 🎉

🎯 HOW TO USE:
1. Select "Place Start/End Points" mode to set red and black points
2. Select "Draw Obstacles" mode to click/drag and create yellow obstacles
3. Click "Find Shortest Path" to see the result!
        """
        explanation_window = tk.Toplevel(self.root)
        explanation_window.title("🧠 Algorithm Explanation")
        explanation_window.geometry("600x700")
        explanation_window.configure(bg='#2c3e50')
        explanation_window.transient(self.root)
        explanation_window.grab_set()
        text_frame = tk.Frame(explanation_window, bg='#2c3e50')
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget = tk.Text(text_frame, wrap='word', font=('Arial', 11),
                              bg='#ecf0f1', fg='#2c3e50', padx=15, pady=15)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        text_widget.insert('1.0', explanation)
        text_widget.config(state='disabled')
        close_btn = tk.Button(explanation_window, text="✅ Got It!",
                              command=explanation_window.destroy,
                              bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                              padx=20, pady=10)
        close_btn.pack(pady=10)

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