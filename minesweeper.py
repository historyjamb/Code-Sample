"""
This project was completed as part of the coursework for the Introduction to AI with Python course taken through Harvard Extension School.
The full project description as well as the original minesweeper.py and runner.py files can be accessed at the following link: 
https://cs50.harvard.edu/summer/ai/2022/projects/1/minesweeper/
 
Functions programmed for this project include the following: 
- Sentence class: known_mines, known_safes, mark_mine, and mark_safe
- MinesweeperAI class: add_knowledge, make_safe_move, make_random_move, find_neighbors, remove_empty_sets, remove_duplicates
"""

import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If #mines == length of sentence, all cells are mines
        if self.count == len(self.cells):
            return self.cells
        # Otherwise, no mine locations known for certain: return empty set
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If no mines in sentence, all cells are safe
        if self.count == 0:
            return self.cells
        # Otherwise, no safe locations known for certain: return empty set
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Mark cell as mine by removing from sentence and update mine count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Mark cell as safe by removing from sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) and 2)
        self.moves_made.add(cell)
        self.safes.add(cell)

        # 3) Construct new sentence with count = #neighboring mines
        new_set = set()
        new_count = count

        for n in self.find_neighbors(cell):
            # If already a known mine, do not add to new_set (update count accordingly)
            if n in self.mines:
                new_count -= 1

            # If not already a known safe (or move made), add to sentence
            elif n not in self.safes:
                new_set.add(n)

        new_sentence = Sentence(new_set, new_count)

        # 3) If new sentence is not empty and not already in KB, add to KB
        if len(new_set) != 0 and new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # 4-5) Make inferences from KB and update KB accordingly
        made_inference = True
        while made_inference:
            made_inference = False

            # Loop through all sentences in KB
            for sentence in list(self.knowledge):

                # 4) Remove known mines and known safes
                for cell in copy.copy(sentence.known_mines()):
                    self.mark_mine(cell)
                    made_inference = True

                for cell in copy.copy(sentence.known_safes()):
                    self.mark_safe(cell)
                    made_inference = True

                # If marked new mines or safes, remove any empty sets or duplicates in KB
                if made_inference:
                    self.remove_empty_sets(self.knowledge)
                    self.remove_duplicates(self.knowledge)

                """
                5) Make additional inferences: Loop through all pairs of sentences (A, B).
                If A and B are not identical and A is a subset of B, return sentence B-A.
                """
                for sentence2 in self.knowledge:
                    A, B = sentence, sentence2

                    # Skip over pair comprised of sentence and itself
                    if A.cells == B.cells:
                        continue

                    # If sentences are of different lengths, let A be the shorter one
                    if len(A.cells) > len(B.cells):
                        A, B = B, A

                    # If A is subset of B
                    if A.cells.issubset(B.cells):
                        newS = Sentence(B.cells.difference(A.cells), B.count - A.count)

                        # Return sentence B - A if not already in KB
                        if newS not in self.knowledge:
                            made_inference = True
                            self.knowledge.append(newS)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # return first discovered safe move not already in self.moves_made
        for s in self.safes:
            if s not in self.moves_made:
                return s

        # else return None
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # if empty board, pick random cell
        if self.knowledge is None:
            return (random.randrange(self.height), random.randrange(self.width))

        # else create list of all available moves
        else:
            open_moves = []
            for row in range(0, self.height):
                for col in range(0, self.width):
                    if (row, col) not in set.union(self.safes, self.mines):
                        open_moves.append((row, col))

            # and return randomly selected move
            if len(open_moves) != 0:
                return random.choice(open_moves)
            else:
                return None

    def find_neighbors(self, cellX):
        """
        Returns a list of all neighboring cells
        """
        # Loop through neighboring cells
        neighbors = []
        for i in range(cellX[0] - 1, cellX[0] + 2):
            for j in range(cellX[1] - 1, cellX[1] + 2):

                # Ignore the cell itself
                if (i, j) == cellX:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.append((i, j))
        return neighbors

    def remove_empty_sets(self, KB):
        """
        Removes empty sentences from knowledge base
        """
        for sentence in KB:
            if len(sentence.cells) == 0:
                KB.remove(sentence)

    def remove_duplicates(self, KB):
        """
        Removes duplicate sentences from knowledge base
        """
        for sentence in KB:
            for sentence2 in KB:
                if sentence is not sentence2 and sentence == sentence2:
                    KB.remove(sentence2)
