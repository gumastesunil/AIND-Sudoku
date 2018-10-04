
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units : DONE
diagonal_unit1 = [[r+c for r,c in zip(rows,cols)]]
diagonal_unit2 = [[r+c for r,c in zip(rows,cols[::-1])]]
unitlist = unitlist + diagonal_unit1 + diagonal_unit2


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function! DONE
    for unit in unitlist:  # Loop through all the units
        # Find all instances of naked twins in a unit
        # Get the boxes whose value is not fixed yet
        b_lst = [box for box in unit if (len(values[box]) > 1)]
        # Get the values of boxes whose value isn't fixed yet
        v_lst = [values[box] for box in unit if (len(values[box]) > 1)]
        # Get the unique 'values' for such boxes
        v_set = set(v_lst)
        # Get the values of all twins. Also applies to triplets/quadrulets etc..
        t_lst = [v for v in v_set if(v_lst.count(v) == len(v))]

        # Eliminate the naked twins as possibilities for their peers
        for val in t_lst:  # Loop through values of all the twins in a unit
            for digit in val:  # For a given value of a twin, loop through all the digits
                for b, v in zip(b_lst, v_lst):  # Loop through the subset of boxes( whose value > 1) in the unit
                    if v == val:  # If the value of a box is same as the value of a twin, it is a twin
                        continue  # Continue to loop
                    if digit in v:  # If the value of a box contains one of the digits of a twin, then eliminate
                        # that digit from the value
                        # values[b] = values[b].replace(digit,'')
                        values = assign_value(values, b, values[b].replace(digit, ''))
                # end for b,v in zip(b_lst,v_lst):
            # end for digit in val:
        # end for val in t_lst:
    # end for unit in unitlist:

    return values
    # raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function. DONE
    for box, value in values.items():  # Loop through all the boxes of sudoku
        if len(value) == 1:  # Select the box which has a value already fixed
            peers_of_box = peers[box]  # Get 'peers' of the box
            for b in peers_of_box:  # Loop through all the peers and eliminate 'value' from their 'values'
                # values[b] = values[b].replace(value, '')
                values = assign_value(values, b, values[b].replace(value, ''))
            # end for b in peers_of_box:
        # if(len(value) == 1):
    # end for box,value in values.items():
    return values
    # raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function. DONE
    for unit in unitlist:  # loop through all the units
        for box in unit:  # loop through all the boxes of a unit
            if len(values[box]) > 1:  # if 'values' of a box is multi-char...
                unit_of_box = list(unit)  # create a copy of the unit
                unit_of_box.remove(box)  # consider all boxes, except the current box
                unit_val_lst = [values[b] for b in unit_of_box]  # get the values of rest of boxes in the unit
                unit_val_str=''.join(unit_val_lst)  # concatenate all the 'values'(strings)
                unit_val_set = set(unit_val_str)  # convert to a set so that repetitions are eliminated
                box_val_set = set(values[box])  # convert the value string of current box to a set
                val_dif = box_val_set.difference(unit_val_set)  # Use set difference operation
                if len(val_dif) == 1:  # If there is only one element in the set difference,
                    # values[box] = list(val_dif)[0]             # assign the element as value for the box
                    values = assign_value(values, box, list(val_dif)[0])
                # end if(len(val_dif) == 1):
            # end if(len(values[box]) > 1):
        # end for box in unit:
    # end for unit in unitlist:
    return values
    # raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    # TODO: Copy your code from the classroom and modify it to complete this function. DONE
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the naked twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        # end if
    # end while

    return values
    # raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function. DONE
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    reduce_ret = reduce_puzzle(values)
    if reduce_ret is False:  # Unable to solve puzzle
        return False
    else:
        # We may have reached a solution or we may be stuck while reducing the puzzle
        # Check if we have solved the puzzle in 'reduce_puzzle'
        bv_lst = [(b, len(v)) for b, v in values.items() if len(v) > 1]
        if len(bv_lst) == 0:  # Solution found as all the boxes have single digit as their value
            return values
        else:
            # Choose one of the unfilled squares with the fewest possibilities
            # bv_lst is a list of all boxes whose values are not fixed yet. It is a list of tuples(box,len(value))
            # pick the box that has the lowest number of possible digits as its value
            box, v_len = min(bv_lst, key=lambda x: x[1])  # the 'key' argument ensures we consider minimum of the
            # second element of the tuple(b,v)
            # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False),
            # return that answer!
            for digit in values[box]:
                copy_of_values = values.copy()  # Make a copy of the puzzle. We dont want to write to the parent's copy.
                copy_of_values[box] = digit  # In the new copy, fix one of the digits as the value of the box
                search_ret = search(copy_of_values)  # Call 'search' with the new copy.Thus we have started a recursion.
                if search_ret:
                    return search_ret  # We found a solution along this path or branch.
                    # Return from here, with that solution.
                else:
                    continue  # We failed along this branch. Assign another digit and search on a new path/branch
            # end for digit in values[box]:
            return False  # We did not find a solution using the box that we had picked and fixed values!!
            # TODO: What if we try using the box with the next minimum possible-values? Use a loop.
        # end if(len(bv_lst) == 0):
    # end if(reduce_ret is False):

    assert (False)  # should return from one of the if/else blocks. Dont expect to be here.
    # raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
