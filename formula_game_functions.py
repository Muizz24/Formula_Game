""" Muizz Ahmed
# Copyright Nick Cheng, 2016, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file. If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment.

# Add your functions here.


def draw_tree_helper(root, depth):
    '''(FormulaTree, int) -> str
    Takes in the root of the tree along with a given depth and draws the tree
    out. By default the depth starts at 1 because we don't consider the
    depth of the root (which is a depth of 0) when we find the given children.
    The recursion process in this function is simple. It moves to the next
    child of the parent along with adding on to its depth by 1.
    '''
    # Base case for when there are no children
    if (root.get_symbol().islower()):
        draw_tree = root.get_symbol()
    # Base case for when there is only 1 child
    elif (root.get_symbol() == '-'):
        draw_tree = '- ' + draw_tree_helper(root.get_children()[0], depth + 1)
    # Base case when there is 2 children and connective is And
    elif (root.get_symbol() == '*'):
        draw_tree = ('* ' +
                     draw_tree_helper(root.get_children()[1], depth + 1) +
                     '\n' +
                     '  '*depth +
                     draw_tree_helper(root.get_children()[0], depth + 1))
    # Base case when there is 2 children and connective is Or
    elif (root.get_symbol() == '+'):
        draw_tree = ('+ ' +
                     draw_tree_helper(root.get_children()[1], depth + 1) +
                     '\n' +
                     '  '*depth +
                     draw_tree_helper(root.get_children()[0], depth + 1))
    # Return the drawn tree
    return draw_tree


def build_tree(formula):
    '''(str) -> FormulaTree
    Builds a tree out of the formula given to the function an returns an obj
    representation of it. A proper tree does not have any capitalized
    variables, any extraneous parenthesses, unmatches parenthesses, or missing
    parenthesses.
    >>> build_tree('X')
    None
    >>> build_tree('(x*y)')
    AndTree(Leaf('x'), Leaf('y'))
    >>> build_tree("(x+y*(z))")
    None
    >>> build_tree("((-x+y)*-(-y+x))")
    AndTree(OrTree(NotTree(Leaf('x')), Leaf('y')),
    NotTree(OrTree(NotTree(Leaf('y')), Leaf('x'))))
    '''
    # Set an arbitrary tree solely for error detection
    tree = NotTree(None)
    # Base case when the formula is empty
    if (len(formula) == 0):
        tree = None
    # Base case when the formula is just a variable/leaf
    elif (len(formula) == 1 and formula.islower()):
        tree = Leaf(formula)
    # Base case when the formula has a Not connective
    elif (len(formula) >= 2 and formula.startswith('-')):
        tree = NotTree(build_tree(formula[1:]))
    else:
        # Set the variables required for the while loop
        # i is the index, o_p_c stands for Open Parenthesses Count and
        # root found confirms when the outermost root is found, this variable
        # reduces the amount of iteration increasing overall efficency
        i, o_p_c, root_found = 0, 0, False
        # Loop through the entire string. The outermost root is found when the
        # o_p_c is 1; once its found, loop cancels. If the outermost root isn't
        # found by some unrecognizable form, the loop cancels and the tree
        # stays as the same arbitrary tree assigned earlier.
        while (root_found is False and i < len(formula)):
            # Increment o_p_c by 1 if an open parenthesses is found
            if (formula[i] == '('):
                o_p_c += 1
            # Decrement o_p_c by 1 if a closed parenthesses is found
            elif (formula[i] == ')'):
                o_p_c -= 1
            # Recur over the outermost Or connective when found; root is found
            elif (formula[i] == '+' and o_p_c == 1):
                tree, root_found = OrTree(build_tree(formula[1:i]),
                                          build_tree(formula[i+1:-1])), True
            # Recur over the outermost And connective when found; root is found
            elif (formula[i] == '*' and o_p_c == 1):
                tree, root_found = AndTree(build_tree(formula[1:i]),
                                           build_tree(formula[i+1:-1])), True
            # Increment index by 1
            i += 1
    # If statement to know when the tree is in an unrecognizable form
    if (tree is None):
        tree = None
    elif (None in tree.get_children()):
        tree = None
    # Return the built tree
    return tree


def draw_formula_tree(root):
    '''(FormulaTree) -> str
    Takes in the root of a Formula Tree and then returns the
    drawn out tree structure in a 90 degrees angle as a string. Right subtree
    is the upper part of the Formula Tree and the lower part is the left
    Subtree.
    >>> draw_formula_tree(AndTree(Leaf('x'), Leaf('y')))
    * y
      x
    '''
    # Call the helper function draw_tree_helper to find the str version of
    # the given Formula Tree. the 1 is the starting depth
    drawn_tree = draw_tree_helper(root, 1)
    # Return the drawn tree
    return drawn_tree


def evaluate(root, variables, values):
    '''(FormulaTree, str, str) -> int
    Finds whether or not the given FormulaTree is True or False for the
    variables and their values. The return statement is either 1 (True) or
    0 (False) depending if the variables satisfy their connective conditions.
    Connective conditions:
    Not connective (-): returns 1 if 1-formula = 0 when formula is 1 or
    1-formula = 1 when formula is 0
    And connective (*): returns 1 iff both values are 1; both variables sum
    up to 2, else returns False for the formula
    Or connective (+): returns 1 if both values sum up to 1 or 2
    else returns 0
    REQ: values can only consist of '1's and '0's
    >>> evaluate(AndTree(Leaf('x'), Leaf('y')), 'xy', '10')
    0
    >>> evaluate(OrTree(Leaf('x'), Leaf('y')), 'xy', '10')
    1
    >>> evaluate(NotTree(Leaf('x')), 'x', '1')
    0
    '''
    # Base case for when formula is just a variable
    if (root.get_symbol().islower()):
        result = int(values[variables.find(root.get_symbol())])
    # Base case for when formula is a Not connective
    elif (root.get_symbol() == '-'):
        result = 1 - evaluate(root.get_children()[0], variables, values)
    # When formula is an And connective
    elif (root.get_symbol() == '*'):
        result = (evaluate(root.get_children()[0], variables, values) +
                  evaluate(root.get_children()[1], variables, values))
        # Check to see if the sum adds up to 2 to decide the result is 0 or 1
        if (result == 2):
            result = 1
        else:
            result = 0
    # When formula is an Or connective
    elif (root.get_symbol() == '+'):
        result = (evaluate(root.get_children()[0], variables, values) +
                  evaluate(root.get_children()[1], variables, values))
        # Check to see if the sum adds up to 1 or more to decide if result is 1
        # or 0
        if (result >= 1):
            result = 1
        else:
            result = 0
    # Return the evaluated formula
    return result


def play2win_helper(root, turns, variables, values, goal, players_turn):
    '''(FormulaTree, str, str, str, int, str) -> int
    Finds whether or not the resulting choice of next move would provide
    a 'guaranteed win' through binary recursion. A guaranteed win, in short,
    is if this move is played, regardless of whatever other move is played,
    the desired outcome (1/0) would be the same for the player A/E.
    REQ: len(turns) > len(values)
    REQ: len(turns) == len(variables)
    REQ: turns can only consist of 'A's and 'E's
    REQ: values can only consist of '1's and '0's
    >>> play2win_helper(AndTree(Leaf('y'), NotTree(Leaf('x'))), 'AE', 'xy', '1'
                        , 1 , 'E')
    0
    '''
    # Firstly, Assign a variable to store each turn
    next_turns = turns[len(values):]
    # If there is no next turn; i.e the amount of turns = amount of values
    # equate the result. This will be our base case.
    if (next_turns == ''):
        result = evaluate(root, variables, values)
    else:
        case_1 = play2win_helper(root, turns, variables, (values + '1'),
                                 goal, players_turn)
        case_2 = play2win_helper(root, turns, variables, (values + '0'),
                                 goal, players_turn)
        # In the advent that player A/E has multiple turns, both
        # cases mustn't have to result into the desired outcome in order to win
        if (players_turn == next_turns[0] and
            (case_1 == goal or case_2 == goal) and
            (players_turn in next_turns[1:] or
             players_turn in turns[len(values)-1:])):
            result = goal
        # If both scenarios result in the same conclusion aka both
        # cases conclude to player A/E's desired outcome, its a winning move
        elif (case_1 == goal and case_2 == goal):
            result = goal
        # If all conditions above don't satisfy, player A/E has no winning move
        else:
            result = 1 - goal
    # return the result
    return result


def play2win(root, turns, variables, values):
    '''(FormulaTree, str, str, str) -> int
    Finds the next move for Player A (Someone trying to make the tree False)
    or Player E (Someone trying to make the tree True) such that this move
    would result in a guaranteed win for that player.
    REQ: len(turns) > len(values)
    REQ: len(turns) == len(variables)
    REQ: turns can only consist of 'A's and 'E's
    REQ: values can only consist of '1's and '0's
    >>> play2win(OrTree(AndTree(Leaf('x'), NotTree(Leaf('y'))), Leaf('z')),
                 'EAE', 'xyz', '1')
    0
    >>> play2win(AndTree(Leaf('y'), NotTree(Leaf('x'))), 'AE', 'xy', '1')
    1
    '''
    # Find who plays the next turn
    next_turn = turns[len(values)]
    # This if statement helps set our objective for each player
    if (next_turn == 'A'):
        end_goal = 0
    elif (next_turn == 'E'):
        end_goal = 1
    # Helper called for both cases to find the guarenteed winning move
    pick_1 = play2win_helper(root, turns, variables, (values + '1'),
                             end_goal, next_turn)
    pick_0 = play2win_helper(root, turns, variables, (values + '0'),
                             end_goal, next_turn)
    # Player A/E chooses default if there is no guarenteed winning move.
    # If there is but both choices result in a winning move, pick their default
    # else picks the move that would result in a win.
    if (pick_1 == end_goal and pick_0 == end_goal):
        winning_strategy = end_goal
    elif ((pick_1 == end_goal and next_turn == 'A') or
          (pick_0 == end_goal and next_turn == 'E')):
        winning_strategy = 1 - end_goal
    else:
        winning_strategy = end_goal
    # Return the winning strategy
    return winning_strategy
