# 🎮 Pacman Game

<div align="center">

![Pacman](https://img.shields.io/badge/Game-Pacman-yellow?style=for-the-badge&logo=gamepad)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?style=for-the-badge&logo=pygame)

*A classic Pacman game built with Python and Pygame featuring procedural maze generation and intelligent ghost AI*

</div>

## 🌟 Features

- **🎯 Classic Gameplay** - Navigate through mazes, collect dots, and avoid ghosts
- **🧠 Smart AI** - Ghost uses BFS pathfinding to hunt down Pacman
- **🗺️ Procedural Generation** - Each level features a randomly generated maze
- **🎵 Immersive Audio** - Sound effects and background music enhance the experience
- **📈 Progressive Difficulty** - Multiple levels with increasing challenge
- **✨ Smooth Animations** - Floating title text and pulsing game over messages

## 🎬 Demo

```
🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
🟦                    PACMAN GAME                     🟦
🟦  Score: 0                              Level: 1    🟦
🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
🟦⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦
🟦⬛🟨·····⬛·····⬛·····⬛·····⬛
🟦⬛··⬛··⬛··⬛··⬛··⬛··⬛··⬛
🟦⬛··⬛··⬛··⬛··⬛··⬛··⬛··⬛
🟦⬛·····⬛·····⬛·····⬛·····👻⬛
🟦⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟦
```

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pacman-game.git
   cd pacman-game
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Add game assets**
   
   Make sure you have these files in your project directory:
   ```
   📁 pacman-game/
   ├── 🐍 pacman_game.py
   ├── 🖼️ pacman.png
   ├── 📷 ghost.png
   ├── 🔊 pacman_eatfruit.wav
   ├── 📢 pacman_intermission.wav
   ├── 🎵 pacman_death.wav
   └── 🎶 pacman_beginning.wav
   ```

4. **Run the game**
   ```bash
   python pacman_game.py
   ```

## 🎮 How to Play

### Controls
- **⬆️ Arrow Up** - Move Pacman up
- **⬇️ Arrow Down** - Move Pacman down  
- **➡️ Arrow Right** - Move Pacman right
- **⬅️ Arrow Left** - Move Pacman left
- **R** - Restart game (when game over)
- **Enter** - Next level (when won)

### Objective
- **Collect dots** (·) to increase your score
- **Avoid the ghost** 👻 - contact means game over!
- **Clear all dots** to advance to the next level
- **Survive as long as possible** and achieve the highest score

## 🛠️ Technical Details

### Game Architecture

- **Game Class** - Main game logic and state management
- **Procedural Maze Generation** - Random maze creation with guaranteed solvability
- **BFS Pathfinding** - Breadth-First Search algorithm for ghost AI
- **Event-Driven Architecture** - Responsive input handling and game state management

### Key Components

| Component | Description |
|-----------|-------------|
| **Map Generation** | Creates random mazes with walls (⬛) and dots (·) |
| **Collision Detection** | Prevents movement through walls |
| **AI Pathfinding** | Ghost uses BFS to find shortest path to Pacman |
| **Audio System** | Background music and sound effects |
| **Animation System** | Smooth visual effects and transitions |

### Configuration

```python
# Game Settings
num_of_tiles = 32      # Tile size
tile_width = 25        # Map width
tile_height = 15       # Map height
pacman_speed = 5       # Pacman movement speed
ghost_speed = 10       # Ghost movement speed
```

## 🎨 Customization

### Modify Game Parameters

You can easily customize the game by changing these variables:

```python
# Maze size
tile_width = 25        # Width of the maze
tile_height = 15       # Height of the maze

# Speed settings
pacman_speed = 5       # Lower = faster Pacman
ghost_speed = 10       # Lower = faster ghost

# Visual settings
num_of_tiles = 32      # Size of each tile in pixels
```

### Adding New Features

- **Multiple Ghosts** - Duplicate ghost logic in `move_ghost()` method
- **Power Pellets** - Add special dots that make ghosts vulnerable
- **Bonus Items** - Implement fruit and bonus point systems
- **Different Maze Patterns** - Modify `generate_map()` for custom layouts

## 🧠 Algorithm Insights

### Maze Generation
The game uses a probability-based approach where each cell has a 15% chance of being a wall, ensuring playable mazes while maintaining randomness.

### Ghost AI
The ghost employs **Breadth-First Search (BFS)** to find the optimal path to Pacman:

```python
def BFS(self, start, end):
    # Returns shortest path from ghost to Pacman
    # Guarantees optimal pathfinding
```

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **ModuleNotFoundError: pygame** | Run `pip install pygame` |
| **No audio playing** | Check if audio files exist and are accessible |
| **Game runs too fast/slow** | Adjust `pacman_speed` and `ghost_speed` values |
| **Images not displaying** | Ensure `pacman.png` and `ghost.png` are in the project directory |

### Performance Tips

- The game runs at 60 FPS by default
- Maze generation might take a moment for larger maps
- Audio files should be in WAV format for best compatibility

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🔧 Create a feature branch
3. 💡 Add your improvements
4. 📤 Submit a pull request

## 📞 Support

If you encounter any issues or have questions:

- 🐛 **Bug Reports** - Open an issue on GitHub
- 💡 **Feature Requests** - Share your ideas in the discussions
- 📧 **Contact** - Reach out for any other questions

---

<div align="center">

**⭐ Star this repository if you enjoyed the game! ⭐**

Made with ❤️ and Python

</div>