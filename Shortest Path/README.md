# 🎯 Interactive Pathfinding Visualizer

A Python-based graphical application that visualizes popular pathfinding algorithms including BFS, DFS, and Dijkstra's algorithm. Built with Tkinter for an intuitive drag-and-drop interface.

![Pathfinding Demo](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **Interactive Grid Interface**: Click and drag to place start/end points and obstacles
- **Multiple Algorithms**: Compare BFS, DFS, and Dijkstra's algorithm performance
- **Real-time Visualization**: Watch the pathfinding process with animated path discovery
- **Smart Obstacle Generation**: Generate various obstacle patterns (maze walls, spirals, clusters, corridors)
- **Weighted Edges**: Dijkstra's algorithm uses random edge weights for realistic pathfinding
- **Intuitive Controls**: Easy-to-use mode switching and drag-and-drop functionality

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Tkinter (usually comes with Python)

### Installation

1. Clone or download the repository:
```bash
git clone <repository-url>
# or download the pathfinding_visualizer.py file
```

2. Run the application:
```bash
python pathfinding_visualizer.py
```

### Usage

1. **Place Start and End Points**:
   - Select "🎯 Place Start/End Points" mode
   - Click to place red start point and black end point
   - Drag existing points to reposition them

2. **Create Obstacles**:
   - Switch to "🧱 Draw Obstacles" mode
   - Click and drag to create yellow obstacles
   - Click on existing obstacles to remove them

3. **Find Path**:
   - Choose your algorithm (BFS, DFS, or Dijkstra)
   - Click "🔍 Find Shortest Path"
   - Watch the green path animate from start to end

## 🧠 Algorithms Explained

### Breadth-First Search (BFS)
- **Purpose**: Finds the shortest path by number of steps
- **Method**: Explores all neighbors level by level
- **Best for**: Unweighted graphs, guaranteed shortest path
- **Time Complexity**: O(V + E)

### Depth-First Search (DFS)
- **Purpose**: Finds any valid path (not necessarily shortest)
- **Method**: Explores one path deeply before backtracking
- **Best for**: Finding any solution quickly, maze solving
- **Time Complexity**: O(V + E)

### Dijkstra's Algorithm
- **Purpose**: Finds the shortest path by total weight/cost
- **Method**: Always explores the lowest-cost path first
- **Best for**: Weighted graphs, finding minimum cost path
- **Time Complexity**: O((V + E) log V)

## 🎮 Controls and Interface

### Color Legend
- 🔴 **Red Circle**: Start point
- ⚫ **Black Circle**: End point  
- 🟡 **Yellow Squares**: Obstacles
- 🟢 **Green Path**: Solution path with connecting lines

### Buttons
- **🔍 Find Shortest Path**: Execute the selected algorithm
- **🔄 Reset Everything**: Clear all points, obstacles, and paths
- **🧹 Clear Obstacles**: Remove all obstacles but keep start/end points
- **🎲 Generate Random**: Create random obstacle patterns
- **📚 How It Works**: Show detailed algorithm explanation

### Modes
- **🎯 Place Start/End Points**: Click to place/move start and end positions
- **🧱 Draw Obstacles**: Click and drag to create/remove obstacles

## 🛠️ Technical Details

### Code Structure

```
pathfinding_visualizer.py
├── Graph class                 # Core graph data structure and algorithms
│   ├── add_vertex()           # Add vertices to the graph
│   ├── add_edge()             # Add weighted edges
│   ├── bfs()                  # Breadth-first search implementation
│   ├── dfs()                  # Depth-first search implementation
│   └── dijkstra()             # Dijkstra's algorithm implementation
│
└── PathfindingGUI class       # Main application interface
    ├── Grid Management        # Canvas grid creation and coordinate conversion
    ├── Event Handling         # Mouse clicks, drags, and hover effects
    ├── Visualization          # Drawing points, obstacles, and paths
    ├── Algorithm Integration  # Connecting GUI with pathfinding algorithms
    └── Obstacle Generation    # Random pattern creation
```

### Key Components

- **Graph Data Structure**: Adjacency list representation with weighted edges
- **Grid System**: 20x20 pixel cells for precise placement
- **Event System**: Comprehensive mouse event handling for interaction
- **Animation System**: Step-by-step path visualization
- **Pattern Generation**: Multiple obstacle patterns for testing

## 🎨 Customization Options

### Grid Settings
```python
self.grid_size = 20           # Size of each grid cell
self.canvas_width = 800       # Canvas width in pixels  
self.canvas_height = 500      # Canvas height in pixels
```

### Visual Styling
- Modern dark theme with accent colors
- Smooth animations and hover effects
- Shadow effects for depth perception
- Responsive cursor changes

### Algorithm Parameters
- Edge weights: Random values between 1-15 for Dijkstra
- Pattern generation: Configurable density and complexity
- Animation speed: 100ms delays for smooth visualization

## 🔧 Advanced Features

### Random Obstacle Patterns

1. **Maze Walls**: Vertical and horizontal wall segments
2. **Spiral**: Circular spiral patterns from center
3. **Clusters**: Random clustered obstacle groups  
4. **Corridors**: Horizontal and vertical corridor obstacles

### Path Validation
- Automatic path existence checking
- Intelligent obstacle removal to ensure solvability
- Multiple attempt validation system

### Interactive Elements
- Drag-and-drop point repositioning
- Continuous obstacle drawing while dragging
- Real-time status updates and feedback
- Comprehensive error handling

## 🐛 Troubleshooting

### Common Issues

**Application won't start**:
- Ensure Python 3.7+ is installed
- Verify Tkinter is available: `python -c "import tkinter"`

**No path found**:
- Check if start and end points are accessible
- Remove obstacles blocking all possible paths
- Use "Generate Random" for solvable configurations

**Performance issues**:
- Reduce grid size for larger areas
- Limit obstacle density for complex patterns

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional pathfinding algorithms (A*, Greedy Best-First)
- More obstacle patterns and generation options
- Performance optimizations for larger grids
- Export/import functionality for grid configurations
- Pathfinding statistics and comparison tools

## 📚 Educational Use

Perfect for:
- Computer Science algorithm visualization
- Interactive learning about graph theory
- Understanding pathfinding concepts
- Comparing algorithm performance and behavior
- Teaching computational thinking and problem-solving

---

*Built with Python and Tkinter for cross-platform compatibility and ease of use.*
