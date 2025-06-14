import pygame
import sys
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import deque
import heapq
from node import node
from data import fixed_maze, fixed_weights

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
        self.adjacent_list.clear()   # built_in fun()
        self.add_vertices()
        self.add_edges()
 
    def add_vertices(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if not self.grid[x][y].is_obsetecle:
                    self.add_vertex((x, y))

    def add_edges(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if not self.grid[x][y].is_obsetecle:
                    # Check and add edge to right neighbor
                    if x < self.cols - 1 and not self.grid[x + 1][y].is_obsetecle:
                        self.add_edge((x, y), (x + 1, y), self.grid[x + 1][y].weight)
                    # Check and add edge to left neighbor
                    if x > 0 and not self.grid[x - 1][y].is_obsetecle:
                        self.add_edge((x, y), (x - 1, y), self.grid[x - 1][y].weight)
                    # Check and add edge to bottom neighbor
                    if y < self.rows - 1 and not self.grid[x][y + 1].is_obsetecle:
                        self.add_edge((x, y), (x, y + 1), self.grid[x][y + 1].weight)
                    # Check and add edge to top neighbor
                    if y > 0 and not self.grid[x][y - 1].is_obsetecle:
                        self.add_edge((x, y), (x, y - 1), self.grid[x][y - 1].weight)

    def dijkstra(self, start, end, open_set, closed_set, show_steps, teal, purple):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        costs = {v: float('inf') for v in self.adjacent_list}
        costs[start] = 0
        visited = {}
        pq = [(0, start)]
        open_set.add(start)

        while pq:
            weight, node = heapq.heappop(pq)
            if node == end:
                path = []
                cur = end
                while cur in visited:
                    path.insert(0, cur)
                    cur = visited[cur]
                if path:
                    path.insert(0, start)
                return path, costs[end]

            open_set.discard(node)
            closed_set.add(node)
            if show_steps and node != start:
                self.grid[node[0]][node[1]].show(purple, 0)

            for nbr in self.adjacent_list[node]:
                if nbr not in closed_set:
                    edge_weight = self.adjacent_list[node][nbr]
                    new_cost = costs[node] + edge_weight
                    if new_cost < costs[nbr]:
                        costs[nbr] = new_cost
                        visited[nbr] = node
                        heapq.heappush(pq, (new_cost, nbr))
                        if nbr not in open_set:
                            open_set.add(nbr)
                            if show_steps:
                                self.grid[nbr[0]][nbr[1]].show(teal, 0)
        return None, None

    def bfs(self, start, end, open_set, closed_set, show_steps, teal, purple):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        queue = deque([[start]])
        visited = set()
        distances = {start: 0}
        open_set.add(start)

        while queue:
            path = queue.popleft()
            node = path[-1]
            if node not in visited:
                visited.add(node)
                closed_set.add(node)
                open_set.discard(node)
                if show_steps and node != start:
                    self.grid[node[0]][node[1]].show(purple, 0)

                if node == end:
                    return path, distances[node]

                for adj in self.adjacent_list[node]:
                    if adj not in visited:
                        new_path = list(path)
                        new_path.append(adj)
                        queue.append(new_path)
                        distances[adj] = distances[node] + 1
                        open_set.add(adj)
                        if show_steps:
                            self.grid[adj[0]][adj[1]].show(teal, 0)
        return None, None

    def dfs(self, start, end, open_set, closed_set, show_steps, teal, purple):
        if start not in self.adjacent_list or end not in self.adjacent_list:
            return None, None

        stack = [[start]]
        visited = set()
        open_set.add(start)

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == end:
                return path, len(path)

            if node not in visited:
                visited.add(node)
                open_set.discard(node)
                closed_set.add(node)
                if show_steps and node != start:
                    self.grid[node[0]][node[1]].show(purple, 0)

                for neighbor in self.adjacent_list.get(node, []):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        stack.append(new_path)
                        if neighbor not in open_set:
                            open_set.add(neighbor)
                            if show_steps:
                                self.grid[neighbor[0]][neighbor[1]].show(teal, 0)

        return None, None

class PathfindingGameUI:
    def __init__(self, window,list):
        self.window = window
        self.window.title("Pathfinding Visualizer")
        self.window.geometry("400x400")

        # Tkinter variables
        self.tkvar = tk.StringVar()
        self.tkvar2 = tk.StringVar()
        self.tkvar3 = tk.StringVar()
        self.var = tk.IntVar()

        # Choices
        self.algo_choose = ['Dijkstra', 'DFS', 'BFS']
        self.obsetcel_shape = ['Blank', 'Fixed Maze', 'Random']
        self.weight_choices = ['All Weights 1', 'Fixed Weights', 'Random Weights']

        # Set default values
        self.tkvar.set('Dijkstra')
        self.tkvar2.set('Blank')
        self.tkvar3.set('All Weights 1')

        # Track user choices
        self.option = self.tkvar.get()
        self.m_option = self.tkvar2.get()
        self.w_option = self.tkvar3.get()

        # Start and end coordinates
        self.start =list[0][0]
        self.end = list[0][0] # it changed in in  onsubmit()

        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(self.window, text='Start (x,y) : ')
        label.grid(row=0, pady=3)
        self.startBox = tk.Entry(self.window)
        self.startBox.grid(row=0, column=1, pady=3)

        label1 = tk.Label(self.window, text='End (x,y) : ')
        label1.grid(row=1, pady=3)
        self.endBox = tk.Entry(self.window)
        self.endBox.grid(row=1, column=1, pady=3)

        # Show steps checkbox
        self.showPath = ttk.Checkbutton(self.window, text='Show Steps :', 
                                      onvalue=1, offvalue=0, variable=self.var)
        self.showPath.grid(columnspan=2, row=2, pady=3)

        # Algorithm selection
        tk.Label(self.window, text="Algorithm:").grid(row=3, pady=3, padx=3)
        self.popupMenu = tk.OptionMenu(self.window, self.tkvar, *self.algo_choose, 
                                     command=self.choose_algo)
        self.popupMenu.grid(row=3, column=1, pady=3)

        # Weight type selection
        tk.Label(self.window, text="Weight:").grid(row=4, pady=3, padx=3)
        self.wMenu = tk.OptionMenu(self.window, self.tkvar3, *self.weight_choices, 
                                 command=self.change_weight)
        self.wMenu.grid(row=4, column=1, pady=3)

        # Maze type selection
        tk.Label(self.window, text="Starting Layout:").grid(row=5, pady=3, padx=3)
        self.mMenu = tk.OptionMenu(self.window, self.tkvar2, *self.obsetcel_shape, 
                                 command=self.choose_obtescel)
        self.mMenu.grid(row=5, column=1, pady=3)

        # Instructions
        tk.Label(self.window, text="1 ≤ x ≤ 48 and 1 ≤ y ≤ 48").grid(
            row=6, column=0, columnspan=2, pady=3)
        tk.Label(self.window, text="Use cursor to draw walls.").grid(
            row=7, column=0, columnspan=2, pady=3)
        tk.Label(self.window, text="Press 'SPACE' to start.").grid(
            row=8, column=0, columnspan=2, pady=3)

        # Submit button
        self.submit = tk.Button(self.window, text="let's go❕⚡", command=self.onsubmit)
        self.submit.grid(columnspan=2, row=9, pady=10)

    def choose_algo(self, event=None, *args):
        self.option = self.tkvar.get()
        print("Algorithm:", self.option)
        if self.option != 'Dijkstra':
            self.wMenu.configure(state='disabled')
        else:
            self.wMenu.configure(state='normal') # if any algo insteade of dijkstra the eight option is disabled 

    def choose_obtescel(self, event=None, *args):
        self.m_option = self.tkvar2.get()
        print("Maze Layout:", self.m_option)

    def change_weight(self, event=None, *args):
        self.w_option = self.tkvar3.get()
        print("Weight Mode:", self.w_option)

    def onsubmit(self):
        try:
            st = self.startBox.get().split(',')
            ed = self.endBox.get().split(',')
            
            # Check if inputs are empty
            if not st[0] or not st[1] or not ed[0] or not ed[1]:
                messagebox.showerror("Error", "Please enter valid coordinates for both start and end points!")
                return
                
            # Convert to integers and validate
            start_x = int(st[0])
            start_y = int(st[1])
            end_x = int(ed[0])
            end_y = int(ed[1])
            
            # Validate coordinates are within bounds
            if not (1 <= start_x <= 48 and 1 <= start_y <= 48 and 
                    1 <= end_x <= 48 and 1 <= end_y <= 48):
                messagebox.showerror("Error", "Coordinates must be between 1 and 48!")
                return
                
            self.start = (start_x, start_y)
            self.end = (end_x, end_y)
            self.window.quit()
            self.window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for coordinates!")
        except IndexError:
            messagebox.showerror("Error", "Please enter coordinates in the format: x,y")

class PathfindingVisualizer:
    def __init__(self):
        # Initialize pygame 
        pygame.init()
        
        # Screen settings
        self.screen_w = 800
        self.screen_h = 800
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        
        # Load image before display is created
        self.background_image = pygame.image.load("images.jpeg")
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_w, self.screen_h)
        )

        pygame.display.set_caption("welcome! : Pathfinding Visualizer")
        
        # Grid settings
        self.cols = 50
        self.rows = 50
        self.w = self.screen_w / self.cols
        self.h = self.screen_h / self.rows
        
        # Colors
        self.purple = (128, 0, 128)    # Color for visited nodes
        self.teal = (173, 216, 230)    # Color for nodes in open set
        self.blue = (0, 0, 255)        # Color for final path
        self.black = (0, 0, 0)         # Color for obstacles
        self.white = (255, 255, 255)   # Background color
        self.green = (50, 255, 50)     # Start node color
        self.red = (255, 50, 50)       # End node color
        
        self.weight_colors = [
    [(255 - i * 17, 255 - i * 17, 255 - i * 17), 0] for i in range(15)
]

# easy way to better than a big list okkkkk
      
        # Initialize grid
        self.grid = []
        self.create_grid() # call the fun of creating 2d list of the nodes {
            
    def create_grid(self):
        self.grid = []  # cread 2d list to be uesd in graph node and edges so that deaw in screen with pygame .show with cloers and w,h in choosen rows,cols/
        for x in range(self.cols):
            row = []
            for y in range(self.rows):
                n= node(pygame, self.screen, self.w, self.h, self.rows, self.cols, x, y)
                row.append(n)
            self.grid.append(row)
            
        '''
        x=>>>> for the index .
        x.pixel where pygame will show in screen with coloor we have choose 
        defualt is_obstecel===False
        
        
        
            '''
            
            
        # 
        # Initialize graph
        self.graph = Graph(self.grid, self.cols, self.rows)
        
        self.ui = None
        self.start_node = self.grid[1][1]
        self.end_node = self.grid[5][7]   # ====>>>>>>>>>>>> ay haga mesh hatefre2 hata law be none 
            
    def show_welcome_screen(self):
            """Display a welcome message on top of the background image"""
            self.screen.blit(self.background_image, (0, 0))

            # Initialize font
            font = pygame.font.SysFont(None, 60)  # (font name, size)
            message = font.render("Welcome to the Pathfinding Visualizer!", True, (45, 154, 100))  # Black text
            message_rect = message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

            # Optional: Add subtitle
            small_font = pygame.font.SysFont(None, 30)
            subtext = small_font.render("Press SPACE to begin", True, (50, 50, 50))
            subtext_rect = subtext.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))

            # Draw
            self.screen.blit(message, message_rect)
            self.screen.blit(subtext, subtext_rect)

            pygame.display.update()        

    def draw_grid(self):
        self.screen.fill(self.white)
        for x in range(self.cols):
            for y in range(self.rows):
                self.grid[x][y].show(self.black, 1)
                                                                                            

    def draw_borders(self):
        
        for pos in range(self.rows):
            # Left border
            self.grid[0][pos].show(self.black, 0)
            self.grid[0][pos].is_obsetecle = True
            # Right border
            self.grid[self.cols-1][pos].show(self.black, 0)
            self.grid[self.cols-1][pos].is_obsetecle = True
            # Bottom border
            self.grid[pos][self.rows-1].show(self.black, 0)  # for the borders 
            self.grid[pos][self.rows-1].is_obsetecle = True
            # Top border
            self.grid[pos][0].show(self.black, 0)
            self.grid[pos][0].is_obsetecle = True 

    def setup_ui(self):
        """Setup the UI for getting user input"""
        window = tk.Tk()
        self.ui = PathfindingGameUI(window,self.grid) # obj of the thinker to take what user wants then appleid to pygame 
        window.mainloop()

    def apply_maze_layout(self):
        """Apply the selected maze layout"""
        if self.ui.m_option == 'Random':
            for i in range(1, self.cols-1):
                for j in range(1, self.rows-1):
                    if (random.choice([1, 2, 3, 4]) == 2 and 
                        self.grid[i][j] != self.start_node and 
                        self.grid[i][j] != self.end_node):
                        self.grid[i][j].is_obsetecle = True
                        self.grid[i][j].show(self.black, 0)
        elif self.ui.m_option == 'Fixed Maze':
            for i in range(self.cols):
                for j in range(self.rows):
                    if (fixed_maze[j][i] == 1 and  #already done in data.py
                        self.grid[i][j] != self.start_node and 
                        self.grid[i][j] != self.end_node):
                        self.grid[i][j].is_obsetecle = True
                        self.grid[i][j].show(self.black, 0)

    def apply_weights(self):
        """Apply the selected weight configuration"""
        if self.ui.w_option == 'Random Weights':
            for i in range(1, self.cols-1):
                for j in range(1, self.rows-1):
                    if (self.grid[i][j] != self.start_node and 
                        self.grid[i][j] != self.end_node and 
                        not self.grid[i][j].is_obsetecle):
                        weight = random.randint(1, 15)
                        self.grid[i][j].weight = weight
                        # Use weight-1 as index since weights start at 1
                        color_info = self.weight_colors[weight-1]
                        self.grid[i][j].show(color_info[0], color_info[1])
        elif self.ui.w_option == 'Fixed Weights':
            for i in range(self.cols):
                for j in range(self.rows):
                    if (self.grid[i][j] != self.start_node and 
                        self.grid[i][j] != self.end_node and 
                        not self.grid[i][j].is_obsetecle):
                        weight = fixed_weights[j][i]  # Access as [row][col]
                        self.grid[i][j].weight = weight
                        color_info = self.weight_colors[weight - 1]
                        self.grid[i][j].show(color_info[0], color_info[1])                 

    def run_pathfinding(self):
        """Execute the selected pathfinding algorithm"""
        open_set = set()
        closed_set = set()
        path, cost = None, None    # initailiing the varibels 
        

        start_pos = (self.start_node.x, self.start_node.y)
        end_pos = (self.end_node.x, self.end_node.y)

        if self.ui.option == 'Dijkstra':
            path, cost = self.graph.dijkstra(start_pos, end_pos, open_set, closed_set, 
                                           self.ui.var.get(), self.teal, self.purple)
        elif self.ui.option == 'BFS':
            path, cost = self.graph.bfs(start_pos, end_pos, open_set, closed_set, 
                                      self.ui.var.get(), self.teal, self.purple)
        elif self.ui.option == 'DFS':
            path, cost = self.graph.dfs(start_pos, end_pos, open_set, closed_set, 
                                      self.ui.var.get(), self.teal, self.purple)

        return path, cost

    def display_path(self, path):
        """Display the final path"""
        if path:
            self.start_node.show(self.green, 0)
            for (x, y) in path[1:-1]:
                self.grid[x][y].show(self.blue, 0)
            self.end_node.show(self.red, 0)

    def show_result(self, path, cost):
        if path:
            message = (f'The shortest distance/least weighted path is {cost}' 
                    if self.ui.option == 'Dijkstra' 
                    else f'The shortest distance to the path is {cost} blocks away')
            
            root = tk.Tk()
            root.wm_withdraw()
            result = messagebox.askokcancel('Program Finished', 
                                        f'The program finished, {message}, \nwould you like to re run the program?')
            if result:  # User clicked OK
                return "restart"
            else:       # User clicked Cancel
                return "exit"
        else:
            messagebox.showinfo('No Path', 'No path found!')
            return "exit"

    def run(self):
        self.show_welcome_screen()

        self.setup_ui()
        
        """Setup the UI for getting user input"""
        '''
        def setup_ui():        
            window = tk.Tk()
            self.ui = PathfindingGameUI(window,self.grid) # obj of the thinker to take what user wants then appleid to pygame 
            window.mainloop()
        '''
        if self.ui.start is None or self.ui.end is None: #>>>>>>>>>> donnot continue 
            return
        self.start_node = self.grid[self.ui.start[0]][self.ui.start[1]] #============>>>>>>>> from window.tk
        self.end_node = self.grid[self.ui.end[0]][self.ui.end[1]]  
        
        # for example if (5,10) is the end 
        #so that end[0] =>> 5,end[1]=>> 10
        # # we need to accses the node in the grid grid[5][10]
        # Create a 2D list (5x5 grid)
        """
grid = [
                ['A0', 'A1', 'A2', 'A3', 'A4'],
                ['B0', 'B1', 'B2', 'B3', 'B4'],
                ['C0', 'C1', 'C2', 'C3', 'C4'],
                ['D0', 'D1', 'D2', 'D3', 'D4'],
                ['E0', 'E1', 'E2', 'E3', 'E4']
            ]

            # User gives start position as (row=2, col=3)
            start = (2, 3)

            # Access the element
            start_value = grid[start[0]][start[1]] =>>>>>>>>>>>>>>>> grid[2][3]>>>>>>'C3'
    
                                                                """
        self.draw_grid()
        self.draw_borders()
        
        self.apply_maze_layout()
        
        self.apply_weights()
        
        self.graph.build_graph()
        
        # Show start and end nodes
        self.start_node.show(self.green, 0)
        self.end_node.show(self.red, 0)
        
        # Main interaction loop
        running = True
        pathfinding_started = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not pathfinding_started:
                        pathfinding_started = True
                        path, cost = self.run_pathfinding()
                        self.display_path(path)
                        
                        action = self.show_result(path, cost)
                        if action == "restart":
                            pygame.quit()  # Clean up Pygame
                            # Restart by creating a new instance
                            visualizer = PathfindingVisualizer()
                            visualizer.run()
                            return   # Exit current instance
                        elif action == "exit":
                            running = False
                
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualizer = PathfindingVisualizer()
    visualizer.run()