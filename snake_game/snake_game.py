from tkinter import *
import random
from collections import deque
import pygame  # Import pygame for sound effects

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\OneDrive\Desktop\dataStructureTask\DS_Final_Project\snake_game\eating_sound.mp3")
game_over_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\OneDrive\Desktop\dataStructureTask\DS_Final_Project\snake_game\game_over_sound.mp3")
win_sound = pygame.mixer.Sound(r"C:\Users\Lenovo\OneDrive\Desktop\dataStructureTask\DS_Final_Project\snake_game\win_sound.mp3")

# Define winning scores for each difficulty level
WINNING_SCORES = {
    'Easy': 20,
    'Medium': 30,
    'Hard': 40
}

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 35
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
FONT_NAME = 'Consolas'

# Difficulty settings for initial speed (lower is faster) and initial body parts
DIFFICULTY_SETTINGS = {
    'Easy':   {'speed': 150, 'body_parts': 3, 'level_up_score': 5},
    'Medium': {'speed': 100, 'body_parts': 4, 'level_up_score': 4},
    'Hard':   {'speed': 75,  'body_parts': 5, 'level_up_score': 3},
}

MIN_SPEED = 30  # Minimum delay to cap speed

class Snake:
    def __init__(self, body_parts):
        self.body_size = body_parts
        self.coordinates = deque()
        self.squares = []
        for _ in range(body_parts):
            self.coordinates.append((0, 0))

    def create_on_canvas(self, canvas):
        for square in self.squares:
            canvas.delete(square)
        self.squares.clear()

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake
        self.coordinates = self._generate_coordinates()
        self.food = self.canvas.create_oval(
            self.coordinates[0], self.coordinates[1],
            self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

    def _generate_coordinates(self):
        max_x = (GAME_WIDTH // SPACE_SIZE) - 1  #doing python floor division in here
        max_y = (GAME_HEIGHT // SPACE_SIZE) - 1
        while True:
            x = random.randint(0, max_x) * SPACE_SIZE
            y = random.randint(0, max_y) * SPACE_SIZE
            if (x, y) not in self.snake.coordinates: #make sure the generated point is not on the snake coordinates
                return [x, y]

    def respawn(self):    #this is a helper method that gets called when you eat a pieace
        self.canvas.delete("food")  #deleting the tagged food as its easier way
        self.coordinates = self._generate_coordinates()
        self.food = self.canvas.create_oval(
            self.coordinates[0], self.coordinates[1],
            self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

class Game:
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        self.score = 0
        self.level = 1
        self.direction = ''
        self.speed = 100
        self.body_parts = 3
        self.level_up_score = 5
        self.winning_score = 0
        self.current_difficulty = None

        self.label = None
        self.canvas = None
        self.snake = None
        self.food = None
        self.game_running = False
        self.restart_button = None
        self.close_button = None
        self.menu_frame = None

        self.init_start_menu()

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = max(int((screen_width - width) / 2), 0)
        y = max(int((screen_height - height) / 2) - 40, 0)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def init_start_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.menu_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.menu_frame.pack(expand=True, fill=BOTH)

        title = Label(
            self.menu_frame, text="Snake Game",
            font=(FONT_NAME, 36, 'bold'),
            fg="white", bg=BACKGROUND_COLOR
        )
        title.pack(pady=(10, 30))

        instr = Label(
            self.menu_frame, text="Select Difficulty",
            font=(FONT_NAME, 20),
            fg="white", bg=BACKGROUND_COLOR
        )
        instr.pack(pady=(0, 5))

        score_text = "Reach the following scores to win:\n"
        for diff in ['Easy', 'Medium', 'Hard']:
            score_text += f"{diff}: {WINNING_SCORES[diff]}\n"
        score_label = Label(
            self.menu_frame, text=score_text,
            font=(FONT_NAME, 12), fg="white", bg=BACKGROUND_COLOR,
            justify=CENTER
        )
        score_label.pack(pady=(0, 20))

        for diff in ['Easy', 'Medium', 'Hard']:
            btn = Button(
                self.menu_frame, text=diff,
                font=(FONT_NAME, 16),
                width=14, bg="#444", fg="white",
                activebackground="#666", activeforeground="white",
                command=lambda d=diff: self.start_game(d)
            )
            btn.pack(pady=6)

        explain_btn = Button(
            self.menu_frame, text="How to Play & Time Complexity",
            font=(FONT_NAME, 14), width=30, bg="#555", fg="white",
            activebackground="#777", activeforeground="white",
            command=self.show_explanation_scroll
        )
        explain_btn.pack(pady=15)

        self.close_button = Button(
            self.menu_frame, text="Close Game",
            font=(FONT_NAME, 14), width=14,
            bg="#aa2222", fg="white",
            activebackground="#cc3333", activeforeground="white",
            command=self.window.quit
        )
        self.close_button.pack(pady=12)

        self.window.update_idletasks()
        req_width = self.menu_frame.winfo_reqwidth() + 40
        req_height = self.menu_frame.winfo_reqheight() + 40
        self.center_window(req_width, req_height)

        self.window.unbind('<Left>')
        self.window.unbind('<Right>')
        self.window.unbind('<Up>')
        self.window.unbind('<Down>')

    def show_explanation_scroll(self):
        explanation_window = Toplevel(self.window)
        explanation_window.title("How to Play & Time Complexity")
        explanation_window.configure(bg=BACKGROUND_COLOR)
        explanation_window.resizable(False, False)

        # Frame to hold text widget and scrollbar
        frame = Frame(explanation_window, bg=BACKGROUND_COLOR)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scroll_y = Scrollbar(frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        text_widget = Text(frame, wrap=WORD, font=(FONT_NAME, 13), fg="white",
                           bg=BACKGROUND_COLOR, yscrollcommand=scroll_y.set, width=60, height=15)
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        scroll_y.config(command=text_widget.yview)

        explanation_text = (
            """
1. Game Loop
    The main game loop is controlled by the next_turn method, 
    which is called repeatedly using self.window.after(self.speed, self.next_turn).
    The complexity of this loop is primarily determined by the operations performed within it.

2. Movement and Collision Detection
    In each iteration of the game loop, the following operations occur:

    - Direction Update: The direction of the snake is updated based on user input. This operation is O(1) since it involves simple variable assignments.
    - Coordinate Calculation: The new head position of the snake is calculated based on the current direction. This is also O(1).
    - Insert New Head: The new head position is added to the front of the snake's coordinates using appendleft, which is O(1) due to the use of a deque.
    - Collision Check: The method checks for collisions with the walls and the snake's own body:
    - Wall Collision: This check is O(1) since it involves comparing the head's coordinates against the game boundaries.
    - Self Collision: This check iterates through the snake's body (excluding the head) to see if the new head position matches any of the body segments. If the snake has n segments, this check is O(n).

3. Food Consumption
    When the snake eats food, the following operations occur:

    - Score Update: Incrementing the score is O(1).
    - Level Up Check: Checking if the score meets the level-up condition is O(1).
    - Food Respawn: The food is respawned at a new location.
      The _generate_coordinates method is called, 
      which may involve checking against the snake's body to ensure the food does not spawn on it.
      In the worst case, this could take O(n) time if the food is repeatedly generated in occupied spaces,
      leading to multiple iterations until a valid position is found.

4. Rendering
    The rendering of the snake and food involves creating graphical elements on the canvas:

    - Drawing the Snake: Each segment of the snake is drawn using create_rectangle,
      which is O(n) where n is the number of segments in the snake.
    - Drawing Food: The food is drawn using create_oval, 
      which is O(1) since it only involves one graphical element.

5. Overall Complexity
    Considering the above components, the overall time complexity of the game loop can be summarized as follows:

    - Best Case: O(1) when the snake is small, and there are no collisions or food respawn checks needed.
    - Average Case: O(n) due to the self-collision check and the rendering of the snake.
    - Worst Case: O(n) for the self-collision check and O(n) for food respawn checks if the food is repeatedly generated in occupied spaces.
      Thus, the worst-case scenario for a single iteration of the game loop can be approximated as O(n).

6. Space Complexity
    The space complexity of the game is primarily determined by the storage of the snake's coordinates and the food's coordinates:

    - Snake Storage: The snake's body is stored in a deque,
      which takes O(n) space where n is the number of segments in the snake.
    - Food Storage: The food's coordinates take O(1) space since it only stores a single position.

    Conclusion
    - In summary, the time complexity of the Snake game is primarily O(n) due to the need to check for collisions and render the snake.
    - The space complexity is also O(n) due to the storage of the snake's body.
    - The game is efficient for typical gameplay scenarios, 
    - as the operations are designed to handle the dynamic nature of the game while maintaining responsiveness to user input.
            """
        )

        text_widget.insert(END, explanation_text)
        text_widget.config(state=DISABLED)  # Make text read-only

        close_btn = Button(
            explanation_window, text="Close",
            font=(FONT_NAME, 14), width=10,
            bg="#aa2222", fg="white",
            activebackground="#cc3333", activeforeground="white",
            command=explanation_window.destroy
        )
        close_btn.pack(pady=10)

        explanation_window.update_idletasks()
        width = frame.winfo_reqwidth() + 40
        height = frame.winfo_reqheight() + close_btn.winfo_reqheight() + 50

        screen_width = explanation_window.winfo_screenwidth()
        screen_height = explanation_window.winfo_screenheight()
        x = max((screen_width - width) // 2, 0)
        y = max((screen_height - height) // 2 - 40, 0)
        explanation_window.geometry(f"{width}x{height}+{x}+{y}")

    def start_game(self, difficulty):
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.speed = settings['speed']
        self.body_parts = settings['body_parts']
        self.level_up_score = settings['level_up_score']
        self.winning_score = WINNING_SCORES[difficulty]
        self.current_difficulty = difficulty
        self.score = 0
        self.level = 1
        self.direction = "down"
        self.game_running = True

        for widget in self.window.winfo_children():
            widget.destroy()
        self.close_button = None

        self.label = Label(
            self.window, text=self.get_label_text(),
            font=(FONT_NAME, 18),
            fg="white", bg=BACKGROUND_COLOR
        )
        self.label.pack(pady=8)

        self.canvas = Canvas(
            self.window, bg=BACKGROUND_COLOR,
            height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()

        self.close_button = Button(
            self.window, text="Close Game",
            font=(FONT_NAME, 14), width=12,
            bg="#aa2222", fg="white",
            activebackground="#cc3333", activeforeground="white",
            command=self.window.quit
        )
        self.close_button.pack(pady=8)

        self.window.update_idletasks()
        width = max(self.canvas.winfo_reqwidth(), self.label.winfo_reqwidth(), self.close_button.winfo_reqwidth()) + 40
        height = (self.label.winfo_reqheight() +
                  self.canvas.winfo_reqheight() +
                  self.close_button.winfo_reqheight() + 50)
        self.center_window(width, height)

        self.snake = Snake(self.body_parts)
        self.snake.create_on_canvas(self.canvas)
        self.food = Food(self.canvas, self.snake)

        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

        self.window.after(self.speed, self.next_turn)

    def get_label_text(self):
        return f"Score: {self.score}  |  Level: {self.level}  |  Difficulty: {self.current_difficulty}"

    def next_turn(self):
        if not self.game_running:
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE
        else:
            self.window.after(self.speed, self.next_turn)
            return

        self.snake.coordinates.appendleft((x, y))
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=SNAKE_COLOR
        )
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            pygame.mixer.Sound.play(eat_sound)  # Play eat sound
            if self.score >= self.winning_score:
                self.win_game()
                return
            if self.score % self.level_up_score == 0:
                self.level += 1
                self.speed = max(MIN_SPEED, int(self.speed * 0.85))
            self.label.config(text=self.get_label_text())
            self.food.respawn()
        else:
            tail_coord = self.snake.coordinates.pop()
            tail_square = self.snake.squares.pop()
            self.canvas.delete(tail_square)

        if self.check_collision():
            self.animate_collision(0)
        else:
            self.window.after(self.speed, self.next_turn)

    def animate_collision(self, step):
        if step < 12:
            fill_color = "red" if step % 2 == 0 else SNAKE_COLOR
            for square in self.snake.squares:
                self.canvas.itemconfig(square, fill=fill_color)
            step += 1
            self.window.after(50, lambda: self.animate_collision(step))
        else:
            self.game_over()

    def win_game(self):
        self.game_running = False
        pygame.mixer.Sound.play(win_sound)  # Play win sound
        self.window.unbind('<Left>')
        self.window.unbind('<Right>')
        self.window.unbind('<Up>')
        self.window.unbind('<Down>')
        self.canvas.delete(ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 - 40,
            font=(FONT_NAME, 70),
            text="YOU WIN!",
            fill="green",
            tag="win"
        )
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 + 40,
            font=(FONT_NAME, 25),
            text=f"Final Score: {self.score}  |  Level: {self.level}",
            fill="white",
            tag="score"
        )

    def change_direction(self, new_direction):
        opposite_directions = {'left': 'right', 'right': 'left',
                               'up': 'down', 'down': 'up'}
        if self.direction == '' or new_direction != opposite_directions.get(self.direction, ''):
            self.direction = new_direction

    def check_collision(self):
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            pygame.mixer.Sound.play(game_over_sound)  # Play game over sound
            return True
        for body_part in list(self.snake.coordinates)[1:]:
            if x == body_part[0] and y == body_part[1]:
                pygame.mixer.Sound.play(game_over_sound)  # Play game over sound
                return True
        return False

    def game_over(self):
        self.game_running = False
        self.window.unbind('<Left>')
        self.window.unbind('<Right>')
        self.window.unbind('<Up>')
        self.window.unbind('<Down>')

        self.canvas.delete(ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 - 40,
            font=(FONT_NAME, 70),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 + 40,
            font=(FONT_NAME, 25),
            text=f"Final Score: {self.score}  |  Level: {self.level}",
            fill="white",
            tag="score"
        )


if __name__ == "__main__":
    import pygame
    pygame.mixer.init()


    window = Tk()
    window.configure(bg=BACKGROUND_COLOR)
    game = Game(window)
    window.mainloop()
