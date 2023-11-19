import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variables in self.domains:
            for values in self.domains[variables]:
                if variables.length != len(values):
                    self.domains[variables].remove(values)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps(x,y):
            x_overlap = self.crossword.overlaps(x,y)[0]
            y_overlap = self.crossword.overlaps(x,y)[1]
            for x_words in self.domains[x]:
                for y_words in self.domains[y]:
                    if self.domains[x][x_words][x_overlap] != self.domains[y][y_words][y_overlap]:
                        self.domains[x].remove[x_words]
                        revised = True
        return revised

                

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list()
            for node in self.domains.keys():
                for other_node in self.domains.keys():
                    if node != other_node: 
                        arcs.append((node,other_node))
        while arcs:
            (x,y) = arcs.pop(0)
            if self.revise(x,y):
                if not self.domains[x]:
                    return False
                for z in self.domains.neighbors(x) - {y}:
                    arcs.append((z,x))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                if not assignment[variable]:
                    return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = list()
        for key,value in assignment.items():
            if value in values:
                return False
            else:
                values.append(value)
            if key.length != len(value):
                return False
            for neighbor in self.crossword.neighbors(key):
                overlap = self.crossword.overlaps[key,neighbor]
                if neighbor in assignment:
                    if assignment[neighbor][overlap[1]] != value[overlap[0]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = dict()
        neighbors = self.crossword.neighbors(var)
        for value in self.domain[var]:
            if value not in assignment:
                count = 0
                for neighbor in neighbors:
                    if value in self.domains[neighbor]:
                        count += 1
                values[value] = count
        return sorted(values, key = lambda key:values[key])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        degree = 0
        value = 1000000
        for current_variable in self.domains.keys():
            if current_variable in assignment:
                continue
            else:
                if value > len(self.domains[current_variable]):
                    value = len(self.domains[current_variable])
                    running_variable = current_variable
                    if self.crossword.neighbors(current_variable) is None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(current_variable))
                elif value == len(self.domains[current_variable]):
                    if self.crossword.neighbors(current_variable) is not None:
                        if degree < len(self.crossword.neighbors(current_variable)):
                            value = len(self.domains[current_variable])
                            running_variable = current_variable
                            degree = len(self.crossword.neighbors(current_variable))
                        else:
                            running_variable = current_variable
                            value = len(self.domains[current_variable])
                            degree = 0
        return running_variable



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consisten(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
