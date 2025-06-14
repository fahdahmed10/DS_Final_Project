import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy
import threading
import time

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯  Sudoku master")
        self.root.geometry("900x800")
        self.root.configure(bg='#1a1a2e')
        self.root.minsize(800, 700)
        
        
        self.set_window_icon()
        
        # Game state
        self.current_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.history = []
        self.redo_stack = []
        self.selected_cell = None
        self.cells = {}
        self.animating = False
        
        # Enhanced color scheme
        self.colors = {
            'bg_main': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_card': '#0f3460',
            'cell_bg_light': '#ffffff',
            'cell_bg_dark': '#f8f9fa',
            'cell_original': '#2c3e50',
            'cell_user': '#3498db',
            'cell_hint': '#f39c12',
            'cell_selected': '#e74c3c',
            'cell_error': '#e74c3c',
            'text_primary': '#ffffff',
            'text_secondary': '#bdc3c7',
            'accent': '#e94560',
            'success': '#27ae60',
            'warning': '#f39c12'
        }
        
        self.create_enhanced_gui()
        
    def set_window_icon(self):
        
        try:
            icon = tk.PhotoImage(file='sudoku_icon.png')
            self.root.iconphoto(False, icon)
            
           
           
            
        except Exception as e:
            print(f"Could not set icon: {e}")
            
            pass
    
    def create_text_icon(self):
        """Create a simple text-based icon"""
        try:
           
            icon_data = '''
                R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH+GkNyZWF0ZWQgd2l0aCBhamF4bG9h
                ZC5pbmZvACH5BAkAAAAALAAAAAAQABAAAAMuGLrc/jDKSVe4OOvNu/9gKI5kaZ5oqq5s675wLM90bd94
                ru987//AoHBILBqPAgA7
            '''
           
            pass
        except:
            pass
    
    def use_embedded_icon(self):
        """Use a base64 encoded icon embedded in the code"""
        try:
            
            icon_data = '''
            iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz
            AAAAB3cAAAd3AzKzJykAAAAgSURBVDiNY/z//z8DJZiJgUJANWAUjHowasIoGAUjHgwAAMYAH3EH
            TgwAAAAASUVORK5CYII=
            '''
            
            
            pass
        except:
            pass
        
    def create_enhanced_gui(self):
        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
       
        self.create_header()
        
       
        main_frame = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
       
        self.create_control_panel(main_frame)
        
       
        self.create_sudoku_grid(main_frame)
        
        
        self.create_action_panel(main_frame)
        
        
        self.create_status_bar()
        
    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.colors['accent'], height=80)
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎯 SUDOKU MASTER", 
                              font=('Arial', 32, 'bold'), 
                              fg=self.colors['text_primary'], 
                              bg=self.colors['accent'])
        title_label.pack(expand=True)
        
    def create_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['bg_card'], width=200)
        control_frame.grid(row=0, column=0, sticky='ns', padx=(0, 15), pady=10)
        control_frame.grid_propagate(False)
        
       
        tk.Label(control_frame, text="🎮 GAME CONTROLS", 
                font=('Arial', 14, 'bold'), 
                fg=self.colors['text_primary'], 
                bg=self.colors['bg_card']).pack(pady=(20, 30))
        
       
        diff_frame = tk.Frame(control_frame, bg=self.colors['bg_card'])
        diff_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(diff_frame, text="🎯 Difficulty Level:", 
                font=('Arial', 11, 'bold'), 
                fg=self.colors['text_primary'], 
                bg=self.colors['bg_card']).pack(anchor='w')
        
        self.difficulty_var = tk.StringVar(value="Medium")
        
       
        diff_buttons_frame = tk.Frame(diff_frame, bg=self.colors['bg_card'])
        diff_buttons_frame.pack(fill='x', pady=5)
        
        difficulties = [("Easy", "#27ae60"), ("Medium", "#f39c12"), ("Hard", "#e74c3c")]
        for diff, color in difficulties:
            btn = tk.Button(diff_buttons_frame, text=diff,
                           font=('Arial', 10, 'bold'),
                           bg=color, fg='white', relief=tk.FLAT,
                           command=lambda d=diff: self.set_difficulty(d))
            btn.pack(fill='x', pady=2)
            
       
        generate_btn = tk.Button(control_frame, text="🎲 GENERATE\nNEW PUZZLE",
                                font=('Arial', 12, 'bold'),
                                bg=self.colors['success'], fg='white',
                                relief=tk.FLAT, height=3,
                                command=self.generate_sudoku)
        generate_btn.pack(pady=20, padx=20, fill='x')
        
        
        self.info_label = tk.Label(control_frame, text="Ready to play!\nGenerate a puzzle to start.",
                                  font=('Arial', 10), 
                                  fg=self.colors['text_secondary'], 
                                  bg=self.colors['bg_card'],
                                  justify='center')
        self.info_label.pack(pady=20, padx=20)
        
    def create_sudoku_grid(self, parent):
       
        grid_container = tk.Frame(parent, bg=self.colors['bg_main'])
        grid_container.grid(row=0, column=1, pady=20)
        
        
        self.grid_frame = tk.Frame(grid_container, bg='#2c3e50', bd=4, relief=tk.RAISED)
        self.grid_frame.pack()
        
        # Create 9 subgrids (3x3 boxes)
        self.subgrids = {}
        for box_row in range(3):
            for box_col in range(3):
                # Each 3x3 box
                subgrid_frame = tk.Frame(self.grid_frame, bg='#34495e', bd=2, relief=tk.RAISED)
                subgrid_frame.grid(row=box_row, column=box_col, padx=2, pady=2)
                self.subgrids[(box_row, box_col)] = subgrid_frame
                
                # Create 9 cells in each box
                for cell_row in range(3):
                    for cell_col in range(3):
                        # Calculate global position
                        global_row = box_row * 3 + cell_row
                        global_col = box_col * 3 + cell_col
                        
                        # Create cell
                        cell = tk.Entry(subgrid_frame, width=3, justify='center',
                                       font=('Arial', 20, 'bold'),
                                       bg=self.colors['cell_bg_light'],
                                       fg=self.colors['cell_original'],
                                       relief=tk.SOLID, bd=1,
                                       disabledbackground=self.colors['cell_bg_dark'],
                                       disabledforeground=self.colors['cell_original'])
                        cell.grid(row=cell_row, column=cell_col, padx=1, pady=1, ipady=8)
                        
                        # Bind events
                        cell.bind('<Button-1>', lambda e, r=global_row, c=global_col: self.select_cell(r, c))
                        cell.bind('<KeyPress>', lambda e, r=global_row, c=global_col: self.on_key_press(e, r, c))
                        cell.bind('<FocusIn>', lambda e, r=global_row, c=global_col: self.select_cell(r, c))
                        
                        self.cells[(global_row, global_col)] = cell
        
    def create_action_panel(self, parent):
        action_frame = tk.Frame(parent, bg=self.colors['bg_card'], width=200)
        action_frame.grid(row=0, column=2, sticky='ns', padx=(15, 0), pady=10)
        action_frame.grid_propagate(False)
        
        
        tk.Label(action_frame, text="⚡ ACTIONS", 
                font=('Arial', 14, 'bold'), 
                fg=self.colors['text_primary'], 
                bg=self.colors['bg_card']).pack(pady=(20, 30))
        
        
        buttons_data = [
            ("💡 HINT", self.colors['warning'], self.show_hint),
            ("↶ UNDO", "#95a5a6", self.undo_move),
            ("↷ REDO", "#95a5a6", self.redo_move),
            ("🔄 RESET", "#e67e22", self.reset_game),
            ("✨ SHOW\nSOLUTION", self.colors['accent'], self.show_solution_animated),
            ("✅ CHECK\nSOLUTION", "#3498db", self.check_solution),
        ]
        
        for text, color, command in buttons_data:
            btn = tk.Button(action_frame, text=text,
                           font=('Arial', 11, 'bold'),
                           bg=color, fg='white',
                           relief=tk.FLAT, height=2,
                           command=command)
            btn.pack(pady=8, padx=20, fill='x')
            
        
        stats_frame = tk.Frame(action_frame, bg=self.colors['bg_secondary'])
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(stats_frame, text="📊 STATS", 
                font=('Arial', 12, 'bold'), 
                fg=self.colors['text_primary'], 
                bg=self.colors['bg_secondary']).pack(pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Moves: 0\nHints: 0",
                                   font=('Arial', 10), 
                                   fg=self.colors['text_secondary'], 
                                   bg=self.colors['bg_secondary'])
        self.stats_label.pack(pady=5)
        
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=40)
        status_frame.grid(row=2, column=0, sticky='ew')
        status_frame.grid_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="🎮 Ready to play! Generate a puzzle to start.",
                                    font=('Arial', 12), 
                                    fg=self.colors['text_primary'], 
                                    bg=self.colors['bg_secondary'])
        self.status_label.pack(expand=True)
        
    def set_difficulty(self, difficulty):
        self.difficulty_var.set(difficulty)
        self.update_status(f"Difficulty set to {difficulty}")
        
    def select_cell(self, row, col):
        if self.animating:
            return
            
       
        if self.selected_cell:
            old_r, old_c = self.selected_cell
            self.update_cell_appearance(old_r, old_c)
        
        
        self.selected_cell = (row, col)
        cell = self.cells[(row, col)]
        cell.configure(bg=self.colors['cell_selected'])
        cell.focus_set()
        
    def on_key_press(self, event, row, col):
        if self.animating:
            return 'break'
            
        if event.char.isdigit() and '1' <= event.char <= '9':
            if self.original_grid[row][col] == 0: 
                self.add_to_history()
                new_value = int(event.char)
                
                self.current_grid[row][col] = new_value
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, event.char)
                self.update_cell_appearance(row, col)
                
                self.update_stats()
                
                if self.check_win():
                    self.show_win_message()
                    
        elif event.keysym in ['Delete', 'BackSpace']:
            if self.original_grid[row][col] == 0:
                self.add_to_history()
                self.current_grid[row][col] = 0
                self.cells[(row, col)].delete(0, tk.END)
                self.update_cell_appearance(row, col)
                self.update_stats()
        
        return 'break'
    
    def update_cell_appearance(self, row, col):
        cell = self.cells[(row, col)]
        
        if self.selected_cell == (row, col):
            cell.configure(bg=self.colors['cell_selected'])
        elif self.original_grid[row][col] != 0:
            cell.configure(bg=self.colors['cell_bg_dark'], 
                          fg=self.colors['cell_original'],
                          font=('Arial', 20, 'bold'))
        elif self.current_grid[row][col] != 0:
            cell.configure(bg=self.colors['cell_bg_light'], 
                          fg=self.colors['cell_user'],
                          font=('Arial', 20, 'bold'))
        else:
            cell.configure(bg=self.colors['cell_bg_light'], 
                          fg=self.colors['cell_original'])
    
    def generate_sudoku(self):
        if self.animating:
            return
            
        self.update_status("🎲 Generating new puzzle...")
        self.root.update()
        
       
        solution = self.generate_complete_sudoku()
        
        
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            cells_to_remove = 35
        elif difficulty == "Medium":
            cells_to_remove = 45
        else:  
            cells_to_remove = 55
        
        puzzle = copy.deepcopy(solution)
        cells_removed = 0
        attempts = 0
        
        while cells_removed < cells_to_remove and attempts < 100:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if puzzle[row][col] != 0:
                backup = puzzle[row][col]
                puzzle[row][col] = 0
                
                
                if self.has_unique_solution(puzzle):
                    cells_removed += 1
                else:
                    puzzle[row][col] = backup
            attempts += 1
        
        self.original_grid = copy.deepcopy(puzzle)
        self.current_grid = copy.deepcopy(puzzle)
        self.solution_grid = copy.deepcopy(solution)
        self.history = []
        self.redo_stack = []
        
        self.update_display()
        self.update_status(f"✨ New {difficulty} puzzle generated! Good luck!")
        self.info_label.configure(text=f"Difficulty: {difficulty}\nEmpty cells: {cells_to_remove}")
        self.update_stats()
        
    def show_hint(self):
        if self.animating:
            return
            
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                       if self.current_grid[i][j] == 0]
        
        if not empty_cells:
            messagebox.showinfo("💡 Hint", "All cells are filled!")
            return
        
        row, col = random.choice(empty_cells)
        self.add_to_history()
        
        correct_value = self.solution_grid[row][col]
        self.current_grid[row][col] = correct_value
        
        cell = self.cells[(row, col)]
        cell.delete(0, tk.END)
        cell.insert(0, str(correct_value))
        
        
        original_bg = cell.cget('bg')
        cell.configure(bg=self.colors['cell_hint'])
        self.root.after(500, lambda: self.update_cell_appearance(row, col))
        
        self.update_stats()
        self.update_status("💡 Hint revealed!")
        
        if self.check_win():
            self.show_win_message()
    
    def check_solution(self):
        if self.valid_sudoku(self.current_grid):
            if self.check_win():
                messagebox.showinfo("🎉 Congratulations!", "Perfect! Puzzle solved correctly!")
            else:
                messagebox.showinfo("✅ Good Progress", "All filled cells are correct! Keep going!")
        else:
            messagebox.showwarning("❌ Check Again", "There are some errors in your solution.")
        
    def add_to_history(self):
        self.history.append(copy.deepcopy(self.current_grid))
        self.redo_stack.clear() 
        if len(self.history) > 50:
            self.history.pop(0)
    
    def undo_move(self):
        if self.animating or not self.history:
            self.update_status("❌ Nothing to undo!")
            return
            
        self.redo_stack.append(copy.deepcopy(self.current_grid))
        self.current_grid = self.history.pop()
        self.update_display()
        self.update_status("↶ Move undone")
        self.update_stats()
    
    def redo_move(self):
        if self.animating or not self.redo_stack:
            self.update_status("❌ Nothing to redo!")
            return
            
        self.history.append(copy.deepcopy(self.current_grid))
        self.current_grid = self.redo_stack.pop()
        self.update_display()
        self.update_status("↷ Move redone")
        self.update_stats()
    
    def reset_game(self):
        if self.animating:
            return
            
        self.current_grid = copy.deepcopy(self.original_grid)
        self.history = []
        self.redo_stack = []
        self.update_display()
        self.update_status("🔄 Game reset to original state")
        self.update_stats()
    
    def show_solution_animated(self):
        if self.animating:
            return
            
        self.animating = True
        self.update_status("✨ Revealing solution...")
        
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                       if self.current_grid[i][j] == 0]
        
        if not empty_cells:
            messagebox.showinfo("Solution", "Puzzle already complete!")
            self.animating = False
            return
        
        self.animate_solution(empty_cells, 0)
    
    def animate_solution(self, empty_cells, index):
        if index >= len(empty_cells):
            self.animating = False
            self.update_status("✨ Solution revealed completely! 🎉")
            return
        
        row, col = empty_cells[index]
        correct_value = self.solution_grid[row][col]
        
        cell = self.cells[(row, col)]
        cell.configure(bg=self.colors['success'])
        cell.delete(0, tk.END)
        cell.insert(0, str(correct_value))
        
        self.current_grid[row][col] = correct_value
        
        self.root.after(150, lambda: self.animate_solution(empty_cells, index + 1))
        self.root.after(300, lambda: self.update_cell_appearance(row, col))
    
    def update_display(self):
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                cell.delete(0, tk.END)
                if self.current_grid[i][j] != 0:
                    cell.insert(0, str(self.current_grid[i][j]))
                self.update_cell_appearance(i, j)
    
    def update_stats(self):
        moves = len(self.history)
        filled_cells = sum(1 for i in range(9) for j in range(9) 
                          if self.current_grid[i][j] != 0 and self.original_grid[i][j] == 0)
        self.stats_label.configure(text=f"Moves: {moves}\nFilled: {filled_cells}")
    
    def update_status(self, message):
        self.status_label.configure(text=message)
        self.root.update()
    
    def check_win(self):
        for i in range(9):
            for j in range(9):
                if self.current_grid[i][j] == 0:
                    return False
        return self.valid_sudoku(self.current_grid)
    
    def show_win_message(self):
        messagebox.showinfo("🎉 VICTORY!", 
                           "🏆 Congratulations!\nYou solved the puzzle!\n\n🌟 Excellent work! 🌟")
        self.update_status("🎉 Puzzle solved! Generate a new one to continue.")
    
    
    def generate_complete_sudoku(self):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(grid)
        return grid
    
    def has_unique_solution(self, puzzle):
        grid1 = copy.deepcopy(puzzle)
        grid2 = copy.deepcopy(puzzle)
        
        if not self.solve(grid1):
            return False
        return self.count_solutions(grid2) == 1
    
    def count_solutions(self, grid, count=0):
        if count > 1:
            return count
            
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.valid_number(grid, i, j, num):
                            grid[i][j] = num
                            count = self.count_solutions(grid, count)
                            grid[i][j] = 0
                            if count > 1:
                                return count
                    return count
        return count + 1

    def valid_row(self, grid):
        for i in range(9):
            exist = set()
            for j in range(9):
                if grid[i][j] == 0:
                    continue
                elif grid[i][j] not in exist:
                    exist.add(grid[i][j])
                else:
                    return False  
        return True

    def valid_column(self, grid):
        for i in range(9):
            exist = set()
            for j in range(9):
                if grid[j][i] == 0:
                    continue
                elif grid[j][i] not in exist:
                    exist.add(grid[j][i])
                else:
                    return False  
        return True

    def valid_area(self, grid):
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                exist = set()
                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        if grid[i][j] == 0:
                            continue
                        elif grid[i][j] not in exist:
                            exist.add(grid[i][j])
                        else:
                            return False  
        return True

    def valid_sudoku(self, grid):
        return self.valid_row(grid) and self.valid_column(grid) and self.valid_area(grid)

    def valid_number(self, grid, r, c, n):
        not_in_row = n not in grid[r]
        not_in_column = n not in [grid[i][c] for i in range(9)]
        not_in_area = n not in [grid[i][j]
                                for i in range(r // 3 * 3, r // 3 * 3 + 3)
                                for j in range(c // 3 * 3, c // 3 * 3 + 3)]
        return not_in_row and not_in_column and not_in_area

    def solve(self, grid, r=0, c=0):
        if r == 9:
            return True
        if c == 9:
            return self.solve(grid, r + 1, 0)
        if grid[r][c] != 0:
            return self.solve(grid, r, c + 1)

        for i in range(1, 10):
            if self.valid_number(grid, r, c, i):
                grid[r][c] = i
                if self.solve(grid, r, c + 1):
                    return True
                grid[r][c] = 0  

        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGUI(root)
    root.mainloop()