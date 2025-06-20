# Chess Engine in Python
A simple, terminal-based chess game built in Python. This engine supports legal move validation, check and checkmate detection, and interactive play entirely in the terminal using emoji-based board rendering.

## Features
- Legal move validation for all pieces
- Check and checkmate detection
- Visual chessboard rendered with emojis
- Interactive command-line interface

## Installation
1. Clone the repository
```bash
git clone https://github.com/reality8807/chess.git
cd chess
```
2. Run the game
```bash
python main.py
```
3. Use a terminal with a dark theme and ensure it’s wide enough to display the board properly.

## How to Play
- Use standard algebraic chess notation to enter your moves.

- When prompted:
  - Initial move: Enter the position of the piece you want to move (e.g., e2)
  - Final move: Enter the destination square (e.g., e4)

Type ```exit``` at any time to quit the game.

## Requirements
No external packages are required. This project uses only standard Python libraries.

## Future Improvements
- Castling support
- En passant
- Pawn promotion
- GUI interface using Tkinter
