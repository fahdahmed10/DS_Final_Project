# 🎯 Sudoku Master - Python GUI Game

**Sudoku Master** is a visually enhanced Sudoku game implemented in Python using the Tkinter library. It offers a fully interactive 9x9 grid, difficulty levels, undo/redo functionality, hints, and animated solution reveal.


## 🚀 Features

- ✅ Generate Sudoku puzzles with 3 difficulty levels: Easy, Medium, Hard.
- 💡 Get hints for empty cells.
- ↶ Undo and ↷ Redo your moves.
- ✨ Animate the solution reveal.
- 🔄 Reset the board to original.
- ✅ Check your solution with validation.
- 🎉 Win message when the puzzle is solved correctly.
- 🎨 Modern color scheme and intuitive UI.

## 🛠️ Technologies Used

- Python 3
- Tkinter for GUI
- Random & Copy for puzzle generation and manipulation
- Threading and Time for animation effects

## 📦 How to Run

1. Make sure you have Python 3 installed.
2. Save the file as `sudoku_game.py`.
3. Run it:

```bash
python sudoku_game.py
```

## 📁 File Structure

- `sudoku_game.py`: The main game script.
- *(Optional)* `sudoku_icon.png`: A PNG icon file used for the app window.

## 🧠 Game Logic

- The grid is generated with a backtracking algorithm ensuring a full valid solution.
- A random number of cells are removed based on the selected difficulty.
- Validity checks include rows, columns, and 3x3 areas.
- The solution can be shown instantly or with animation.

## 🧪 Features in Detail

| Feature         | Description                                         |
|----------------|-----------------------------------------------------|
| Difficulty      | Choose Easy (35 empty), Medium (45), Hard (55)     |
| Hint            | Randomly fills a correct number in an empty cell   |
| Undo/Redo       | Supports 50 move history steps                     |
| Reset           | Resets puzzle to original generated state          |
| Show Solution   | Reveals solution with cell-by-cell animation       |
| Check Solution  | Verifies user entries for correctness              |

## 🧩 Sudoku Rules

- Each row, column, and 3x3 subgrid must contain numbers from 1 to 9 without repetition.

## 🤖 Future Enhancements (Ideas)

- Timer and score tracking
- User custom puzzles
- Save/load game state
- Keyboard shortcuts and accessibility improvements

## 👨‍💻 Author

Created by **[ahmed farahat]**  
You can modify the design or logic freely for learning or improvement purposes.