# 🐍 Advanced Snake Game with Tkinter & Pygame

A modern twist on the classic **Snake Game** built with Python's `Tkinter` for GUI and `Pygame` for immersive sound effects. This version includes difficulty levels, animated effects, a detailed start menu, and performance-aware logic. Perfect for learning object-oriented design, GUI development, and basic algorithm analysis.

---

## 🚀 Features

- 🟢 **3 Difficulty Levels**: Easy, Medium, Hard — each with increasing speed and complexity
- 🎵 **Sound Effects**: Eating, Game Over, and Victory sounds using `pygame.mixer`
- 🧠 **Time Complexity Breakdown**: Learn how the algorithm behaves with game progression
- 🖼️ **Intuitive GUI**: Built entirely with `Tkinter`
- 📊 **Game Stats**: Displays live score, level, and difficulty
- 🔁 **Restart and Close Controls**: Easily restart or quit from any state
- 🧪 **Efficient Logic**: Optimized with deques and complexity-conscious rendering

---

## 📸 Screenshot

![Snake Game Screenshot](https://user-images.githubusercontent.com/your-placeholder-link/snake-game-ui.png)  
*Customize this with your actual screenshot.*

---

## 🛠️ Requirements

- Python 3.x
- `tkinter` (usually included with Python)
- `pygame` (`pip install pygame`)

---

## 🧩 How to Run

1. Clone this repository or download the `snake_game.py` file.
2. Make sure you have the required sound files:
   - `eating_sound.mp3`
   - `game_over_sound.mp3`
   - `win_sound.mp3`
3. Modify the paths in the Python file if needed:
   ```python
   pygame.mixer.Sound(r"full/path/to/eating_sound.mp3")
   ```
4. Run the game:
   ```bash
   python snake_game.py
   ```

---

## 🎮 Controls

| Key      | Action        |
|----------|---------------|
| `↑`      | Move Up       |
| `↓`      | Move Down     |
| `←`      | Move Left     |
| `→`      | Move Right    |

---

## 📈 Time & Space Complexity

The game includes an in-app explanation of algorithmic complexity. Highlights:

- **Time Complexity:** `O(n)` where `n` = length of the snake (due to rendering and collision checks)
- **Space Complexity:** `O(n)` for storing the snake's body

View this through the `How to Play & Time Complexity` button in the main menu.

---

## 🧠 Educational Value

This game is a great example for:

- Object-Oriented Programming (OOP) with classes for `Snake`, `Food`, and `Game`
- GUI layout and interactivity using `Tkinter`
- Using `deque` for fast head/tail manipulation
- Real-world implementation of game loops and event binding

---

## 📁 Folder Structure Suggestion

```
/snake-game
│
├── snake_game.py
├── README.md
├── assets/
│   ├── eating_sound.mp3
│   ├── game_over_sound.mp3
│   └── win_sound.mp3
```

---

## 👨‍💻 Author

**Ali Ahmed Gad**  
Biomedical Engineering @ Cairo University  
Winner of 3rd place in Shell Autonomous Car Challenge  
Connect on [LinkedIn](https://www.linkedin.com/in/ali-gad)

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
