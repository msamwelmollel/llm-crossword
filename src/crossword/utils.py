"""
Utility functions for loading and manipulating crossword puzzles.

You should not need to worry about this module. We use it to load CrosswordPuzzle instances from .puz files.
"""

from src.crossword.crossword import CrosswordPuzzle
from src.crossword.exceptions import InvalidClueError
from src.crossword.types import Clue, Grid, Cell, Direction
import puz

def load_puzzle(puz_file_path: str) -> CrosswordPuzzle:
    """Load a puzzle from a .puz file."""
    puzzle_file = puz.read(puz_file_path)
    
    # Initialize puzzle with dimensions
    puzzle = CrosswordPuzzle(
        width=puzzle_file.width,
        height=puzzle_file.height
    )
    
    # Update initial grid with puzzle file content
    new_cells = [[Cell(row=r, col=c, value=None) 
                    for c in range(puzzle.width)]
                for r in range(puzzle.height)]
                
    for i, c in enumerate(puzzle_file.fill):
        row = i // puzzle.width
        col = i % puzzle.width
        new_cells[row][col].value = None if c == '-' else '░' if c == '.' else c

    puzzle.grid_history[0] = Grid(
        width=puzzle.width,
        height=puzzle.height,
        cells=new_cells
    )

    numbering = puzzle_file.clue_numbering()

    # Add across clues with answers
    for across in numbering.across:
        row = across["cell"] // puzzle.width
        col = across["cell"] % puzzle.width
        answer = ''.join(puzzle_file.solution[across["cell"] + i] 
                        for i in range(across["len"]))
        try:
            puzzle.add_clue(Clue(
                number=len(puzzle.clues) + 1,
                text=across["clue"],
                direction=Direction.ACROSS,
                length=across["len"],
                row=row,
                col=col,
                answer=answer
            ))
        except InvalidClueError as e:
            raise InvalidClueError(f"Invalid across clue: {e}")

    # Add down clues with answers
    for down in numbering.down:
        row = down["cell"] // puzzle.width
        col = down["cell"] % puzzle.width
        answer = ''.join(puzzle_file.solution[down["cell"] + i * puzzle.width] 
                        for i in range(down["len"]))
        try:
            puzzle.add_clue(Clue(
                number=len(puzzle.clues) + 1,
                text=down["clue"],
                direction=Direction.DOWN,
                length=down["len"],
                row=row,
                col=col,
                answer=answer
            ))
        except InvalidClueError as e:
            raise InvalidClueError(f"Invalid down clue: {e}")

    return puzzle
