"""
Create crossword puzzles in .puz format.

You should not need to worry about this module. We used this to create the some of the test puzzles.
"""

from typing import List, Optional, Union
import logging
from pathlib import Path
import puz

from crossword.types import Clue, Direction, Grid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CrosswordCreator:
    """Creates and manages crossword puzzles in .puz format."""
    
    def __init__(self, width: int, height: int, title: str = "Custom Crossword", author: str = "Anonymous"):
        """
        Initialize a new CrosswordCreator instance.
        """
        self.title = title
        self.author = author
        self.grid = Grid(width=width, height=height, cells=[])
        self.grid.initialize_empty()
        self.clues: List[Clue] = []
        self.puzzle = puz.Puzzle()
        
    def add_entry(self, 
                 number: int,
                 direction: Direction,
                 clue_text: str,
                 answer: str,
                 row: int,
                 col: int) -> None:
        """
        Add a new entry to the crossword.
        """
        clue = Clue(
            number=number,
            text=clue_text,
            direction=direction,
            length=len(answer),
            row=row,
            col=col,
            answer=answer.upper()
        )
            
        if not self._validate_entry(clue):
            raise ValueError(f"Invalid entry at position ({row}, {col})")
            
        self._place_entry(clue)
        self.clues.append(clue)
        
    def _validate_entry(self, clue: Clue) -> bool:
        """
        Validate if a clue can be placed at the specified position.
        """
        cells = clue.cells()
        if not cells:
            return False
            
        for row, col in cells:
            if (row < 0 or row >= self.grid.height or 
                col < 0 or col >= self.grid.width):
                return False
            
            # Check overlap with existing letters
            current_cell = self.grid.cells[row][col]
            if current_cell.value is not None:
                answer_idx = (col - clue.col) if clue.direction == Direction.ACROSS else (row - clue.row)
                if current_cell.value != clue.answer[answer_idx]:
                    return False
                
        return True
        
    def _place_entry(self, clue: Clue) -> None:
        """Place a clue in the grid."""
        for i, (row, col) in enumerate(clue.cells()):
            cell = self.grid.cells[row][col]
            cell.value = clue.answer[i]
                               
    def create_puzzle(self) -> None:
        """
        Create the .puz puzzle from the current entries.
        """
        if not self.clues:
            raise ValueError("No clues added to the crossword")
            
        # Sort clues by number and direction (across before down)
        self.clues.sort(key=lambda c: (c.number, c.direction != Direction.ACROSS))
        
        # Set puzzle metadata
        self.puzzle.width = self.grid.width
        self.puzzle.height = self.grid.height
        self.puzzle.title = self.title
        self.puzzle.author = self.author
        
        # Create solution string
        solution_string = ''
        for row in self.grid.cells:
            for cell in row:
                solution_string += cell.value if cell.value else '.'
                
        # Create fill string (- for letters, . for blanks)
        fill_string = ''.join('-' if c.isalpha() else '.' for c in solution_string)
        
        self.puzzle.solution = solution_string
        self.puzzle.fill = fill_string
        self.puzzle.clues = [clue.text for clue in self.clues]
        
    def save_puzzle(self, output_dir: Optional[Union[str, Path]] = None) -> None:
        """
        Save the puzzle to a .puz file.
        """
        filename = f"{self.title.replace(' ', '_')}.puz"
        if output_dir:
            output_path = Path(output_dir) / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path(filename)
            
        self.puzzle.save(str(output_path))
        logger.info(f"Successfully saved puzzle to {output_path}")

    def print_grid(self) -> None:
        """
        Print the crossword grid.
        """
        print("\nCrossword Grid:")
        print("-" * (self.grid.width * 2 + 1))
        for i in range(self.grid.height):
            print("|", end=" ")
            for j in range(self.grid.width):
                cell = self.grid.cells[i][j]
                print(cell.value if cell.value else "-", end=" ")
            print("|")
        print("-" * (self.grid.width * 2 + 1))

def create_cat_cow_puzzle():
    """
    Creates a puzzle with this layout:
    C A T - -
    O - E - -
    W - A - -
    - - R - -
    - - - - -
    """
    # Initialize creator
    creator = CrosswordCreator(
        width=5,
        height=5,
        title="Cat and Cow Puzzle",
        author="Crossword Creator"
    )
    
    # Across entries
    # Add the entries
    # 1. CAT going across
    creator.add_entry(
        number=1,
        direction=Direction.ACROSS,
        clue_text="Feline friend",
        answer="CAT",
        row=0,
        col=0
    )
    
    # Down entries
    # 2. COW going down
    creator.add_entry(
        number=1,
        direction=Direction.DOWN,
        clue_text="Dairy farm animal",
        answer="COW",
        row=0,
        col=0
    )
    
    # 3. TEAR going down
    creator.add_entry(
        number=2,
        direction=Direction.DOWN,
        clue_text="A drop of sadness",
        answer="TEAR",
        row=0,
        col=2
    )
    
    # Create and save the puzzle
    creator.create_puzzle()
    creator.save_puzzle()
    
    # Print the grid for visualization
    print("\nCrossword Grid:")
    creator.print_grid()
    
    # Print the clues
    print("\nClues:")
    for clue in creator.clues:
        print(f"{clue.number}{clue.direction.value[0].upper()}. {clue.text}")

def create_book_puzzle():
    """
    Creates a puzzle with literary theme
    """
    creator = CrosswordCreator(
        width=7,
        height=7,
        title="Literary Crossword",
        author="Crossword Creator"
    )
    
    # Add across entries
    creator.add_entry(
        number=1,
        direction=Direction.ACROSS,
        clue_text="A long narrative poem",
        answer="EPIC",
        row=0,
        col=0
    )
    
    creator.add_entry(
        number=2,
        direction=Direction.ACROSS,
        clue_text="A person who writes books",
        answer="AUTHOR",
        row=3,
        col=1
    )

    # Add down entries

    creator.add_entry(
        number=1,
        direction=Direction.DOWN,
        clue_text="A short story with a moral lesson",
        answer="PARABLE",
        row=0,
        col=1
    )
    
    creator.add_entry(
        number=2,
        direction=Direction.DOWN,
        clue_text="A book's outer casing",
        answer="COVER",
        row=2,
        col=5
    )
    
    creator.add_entry(
        number=3,
        direction=Direction.DOWN,
        clue_text="A narrative tale",
        answer="STORY",
        row=2,
        col=3
    )

    # Create and save puzzle
    creator.create_puzzle()
    creator.save_puzzle()
    
    # Print visualization
    print("\nCrossword Grid:")
    creator.print_grid()

    print("\nClues:")
    for clue in creator.clues:
        print(f"{clue.number}{clue.direction.value[0].upper()}. {clue.text}")


if __name__ == "__main__":
    create_cat_cow_puzzle()
    create_book_puzzle()