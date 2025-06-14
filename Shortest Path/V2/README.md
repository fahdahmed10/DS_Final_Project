# 🎯 Pathfinding Visualizer

A beautiful, interactive visualization tool for exploring classic pathfinding algorithms. Watch as algorithms like Dijkstra's, BFS, and DFS find their way through mazes and weighted grids in real-time!

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🧠 **Three Powerful Algorithms**
- **Dijkstra's Algorithm** - Finds the shortest weighted path
- **Breadth-First Search (BFS)** - Guarantees shortest unweighted path
- **Depth-First Search (DFS)** - Explores paths deeply

### 🎨 **Interactive Visualization**
- **Real-time Animation** - Watch algorithms explore the grid step by step
- **Customizable Speed** - Adjust animation speed from 1-100
- **Color-coded Exploration** - Purple for visited nodes, teal for frontier
- **Dynamic Path Display** - Beautiful blue path highlighting

### 🏗️ **Flexible Grid Configuration**
- **Multiple Maze Types**:
  - Blank canvas for custom designs
  - Pre-built fixed maze layouts
  - Randomly generated mazes
- **Weight Systems**:
  - Uniform weights (all cells equal)
  - Fixed weight patterns
  - Random weight distributions (1-15 range)
- **Interactive Wall Drawing** - Left-click to add, right-click to remove walls

### 🎮 **User-Friendly Interface**
- Intuitive configuration dialog
- Custom start/end point selection
- Real-time mouse interaction
- Keyboard shortcuts for quick actions

## 🚀 Quick Start

### Prerequisites
```bash
pip install pygame tkinter
```

### Installation
1. Clone or download the repository
2. Navigate to the project directory
3. Run the visualizer:
```bash
python path_finder_v2.py
```

### Basic Usage
1. **Configure Settings** - Choose algorithm, maze type, and parameters
2. **Set Coordinates** - Define start (green) and end (red) points
3. **Customize Grid** - Use mouse to draw/erase walls
4. **Start Visualization** - Press `SPACE` to begin pathfinding
5. **Reset & Retry** - Press `R` to reset the grid

## 🎮 Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start pathfinding algorithm |
| `R` | Reset grid to initial state |
| `Left Click` | Add wall/obstacle |
| `Right Click` | Remove wall/obstacle |
| `ESC` | Exit application |

## 🎨 Visual Legend

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Start point |
| 🔴 **Red** | End point |
| ⚫ **Black** | Walls/obstacles |
| 🟣 **Purple** | Visited nodes |
| 🔵 **Light Blue** | Frontier nodes |
| 🔷 **Dark Blue** | Final path |
| 🎨 **Gray Shades** | Weighted cells (lighter = lower weight) |

## 📊 Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Guarantees Shortest Path | Considers Weights |
|-----------|----------------|------------------|-------------------------|-------------------|
| **Dijkstra** | O((V + E) log V) | O(V) | ✅ Yes | ✅ Yes |
| **BFS** | O(V + E) | O(V) | ✅ Yes (unweighted) | ❌ No |
| **DFS** | O(V + E) | O(V) | ❌ No | ❌ No |

*V = vertices (cells), E = edges (connections)*

## 🛠️ Configuration Options

### Maze Layouts
- **Blank** - Clean grid for custom maze creation
- **Fixed Maze** - Predefined maze with strategic walls
- **Random** - Procedurally generated obstacles

### Weight Configurations
- **All Weights 1** - Uniform traversal cost
- **Fixed Weights** - Predetermined weight patterns
- **Random Weights** - Varied traversal costs (1-15)

### Animation Settings
- **Show Steps Toggle** - Enable/disable step-by-step visualization
- **Speed Control** - Adjust animation speed (1-100)
- **Custom Coordinates** - Set start/end points (1-48 range)

## 🏗️ Architecture

The project follows a clean, modular architecture:

```
├── Node Class          # Individual grid cell representation
├── Graph Class         # Graph structure and pathfinding algorithms
├── PathfindingGameUI   # Configuration interface
└── PathfindingVisualizer # Main visualization engine
```

### Key Components

**Node Class**
- Represents individual grid cells
- Handles visual rendering and properties
- Manages obstacle and weight states

**Graph Class**
- Implements graph data structure
- Contains all pathfinding algorithms
- Handles graph construction and traversal

**UI Components**
- Modern tkinter interface
- Real-time parameter adjustment
- Input validation and error handling

## 🔧 Customization

### Adding New Algorithms
```python
def your_algorithm(self, start, end, visualizer):
    # Your pathfinding logic here
    # Use visualizer.animate_node() for visualization
    return path, cost
```

### Custom Maze Patterns
```python
# Add to fixed_maze array
custom_maze = [
    [1, 1, 1, 1, 1],  # 1 = wall, 0 = empty
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]
```

### Color Schemes
```python
# Modify colors in PathfindingVisualizer class
self.purple = (155, 89, 182)    # Visited nodes
self.teal = (52, 152, 219)      # Frontier nodes
self.blue = (41, 128, 185)      # Final path
```

## 🎯 Use Cases

### Educational
- **Computer Science Courses** - Visualize algorithm behavior
- **Data Structures Learning** - Understand graph traversal
- **Algorithm Analysis** - Compare performance characteristics

### Research & Development
- **Pathfinding Research** - Test new algorithms
- **Game Development** - Prototype AI movement
- **Robotics** - Simulate navigation planning

### Entertainment
- **Interactive Learning** - Engaging algorithm exploration
- **Puzzle Solving** - Create and solve custom mazes
- **Algorithm Racing** - Compare speeds visually

## 🚀 Advanced Features

### Performance Optimization
- Efficient graph representation using adjacency lists
- Optimized rendering with pygame
- Smart animation frame limiting

### Extensibility
- Modular algorithm implementation
- Easy color scheme customization
- Configurable grid dimensions

### User Experience
- Intuitive mouse controls
- Comprehensive error handling
- Responsive UI design

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Contribution Ideas
- 🔥 New pathfinding algorithms (A*, Greedy Best-First)
- 🎨 Enhanced visual themes
- 🚀 Performance optimizations
- 📱 Mobile-friendly version
- 🧪 Unit tests and documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

Having issues? We're here to help!

- 📧 **Email**: Open an issue on GitHub
- 🐛 **Bug Reports**: Use the issue tracker
- 💡 **Feature Requests**: Share your ideas via issues
- 📚 **Documentation**: Check the code comments

## 🏆 Acknowledgments

- Built with Python and Pygame
- Inspired by pathfinding algorithm visualizations
- Thanks to the open-source community

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ by passionate developers

</div>