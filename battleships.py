
from random import randint
from copy import deepcopy


def is_sunk(ship):
    """returns Boolean value, which is `True` if `ship` is sunk and `False` otherwise"""
    if len(ship[4]) == ship[3]:  # if the number of hits is the same as the length of the ship, it has sunk
        return True
    elif len(ship[4]) < ship[3]:  # if the number of hits is less than the length of the ship, it has sunk
        return False


def ship_type(ship):
    """returns one of the strings `"battleship"`, `"cruiser"`, `"destroyer"`, or `"submarine"`
    identifying the type of `ship`"""
    ship_list = ["submarine", "destroyer", "cruiser", "battleship"]
    return ship_list[ship[3] - 1]  # length n of ship corresponds to the nth name in the list


def is_open_sea(row, column, fleet):
    """checks if the square given by `row` and `column` neither contains nor is adjacent
    (horizontally, vertically, or diagonally) to some ship in `fleet`. Returns Boolean
    `True` if so and `False` otherwise"""
    if row not in range(0, 10) or column not in range(0, 10):  # if row or column is outside the grid, sea is not open
        return False
    taken_row_x_col = set()  # will first be filled with tuples representing tiles taken by the ships in the fleet
    for ship in fleet:  # iterate through ships in fleet
        if ship[2]:  # if ship is horizontal, populate taken squares horizontally for the length of the ship
            taken_row_x_col.update((ship[0], y) for y in range(ship[1], (ship[1] + ship[3])))
        else:  # if ship is not horizontal, populate taken squares vertically for the length of the ship
            taken_row_x_col.update((x, ship[1]) for x in range(ship[0], (ship[0] + ship[3])))
    for row_x_col in taken_row_x_col:  # check if input is adjacent to taken squares
        if abs(row - row_x_col[0]) <= 1 and abs(column - row_x_col[1]) <= 1:
            return False
    return True


def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    """checks if addition of a ship, specified by `row, column, horizontal`, and `length` as in `ship` representation
    above, to the `fleet` results in a legal arrangement (see the figure above). If so, the function returns Boolean
    `True` and it returns `False` otherwise. This function makes use of the function `is_open_sea`"""

    if horizontal:  # generates list of squares taken by ship if horizontal
        squares_taken = [(row, y) for y in range(column, column + length)]

    else:  # generates list of squares taken by ship if it is not horizontal
        squares_taken = [(x, column) for x in range(row, row + length)]

    for square in squares_taken:  # check that sea is open for all squares taken by proposed ship
        if is_open_sea(square[0], square[1], fleet) is False:
            return False
    return True  # if open sea never returns false, a true value will be returned


def place_ship_at(row, column, horizontal, length, fleet):
    """returns a new fleet that is the result of adding a ship, specified by `row, column, horizontal`, and `length`
    as in `ship` representation above, to `fleet`. It may be assumed that the resulting arrangement of the new fleet is
    legal"""
    fleet.append((row, column, horizontal, length, set()))  # add ship to fleet
    return fleet


def randomly_place_all_ships():
    """returns a fleet that is a result of a random legal arrangement of the 10 ships in the ocean. This function makes
    use of the functions `ok_to_place_ship_at` and `place_ship_at` """
    fleet = []  # initialise fleet
    ship_list = {'battleship': [1, 4],
                 'cruiser': [2, 3],
                 'destroyer': [3, 2],
                 'submarine': [4, 1]}  # Initialise dictionary containing ship types, number to be placed and length.

    for key, value in ship_list.items():
        """Iterate through key value pairs, placing ships into the fleet (dictionaries ordered as Python 3.9 used)"""
        while value[0] > 0:  # generate ship of key given by key type if there are still ships of that type to be placed
            row = randint(0, 9)
            column = randint(0, 9)
            horizontal = bool(randint(0, 1))
            length = value[1]
            if ok_to_place_ship_at(row, column, horizontal, length, fleet):
                fleet = place_ship_at(row, column, horizontal, length, fleet)  # place ship into fleet if it is legal
                value[0] -= 1  # ship of type key has been placed, so one less required
    return fleet


def check_if_hits(row, column, fleet):
    """returns Boolean value, which is `True` if the shot of the human player at the square
    represented by `row` and `column` hits any of the ships of `fleet`, and `False` otherwise"""
    taken_row_x_col = set()  # will first be filled with tuples representing tiles taken by the ships in the fleet
    already_hit = set()  # will be filled with the squares that have been already hit

    for ship in fleet:  # iterate through each ship in the fleet
        already_hit = already_hit.union(ship[4])  # add already hit squares to set
        if ship[2]:  # update set of squares occupied by ships with current ship if it is horizontal
            taken_row_x_col.update((ship[0], y) for y in range(ship[1], (ship[1] + ship[3])))
        else:  # update set of squares occupied by ships with current ship if it is vertical
            taken_row_x_col.update((x, ship[1]) for x in range(ship[0], (ship[0] + ship[3])))

    if (row, column) in taken_row_x_col.difference(already_hit):
        # check that row, column are in a square that is taken by a ship, but not already hit
        return True
    else:
        return False


def hit(row, column, fleet):
    """returns a tuple `(fleet1, ship)` where `ship` is the ship from the fleet `fleet` that receives a hit by the shot
    at the square represented by `row` and `column`, and `fleet1` is the fleet resulting from this hit. It may be
    assumed that shooting at the square `row, column` results in of some ship in `fleet`"""
    fleet1 = deepcopy(fleet)  # copy fleet with fleet 1

    for ship_pos in range(0, 10):  # counter, counting the ship in the fleet
        if fleet1[ship_pos][2]:  # if horizontal ship, find coordinates of ship
            taken_by_ship = [(fleet1[ship_pos][0], y) for y in
                             range(fleet1[ship_pos][1], (fleet1[ship_pos][1] + fleet1[ship_pos][3]))]
        else:  # if vertical ship, find coordinates of ship
            taken_by_ship = [(x, fleet1[ship_pos][1]) for x in
                             range(fleet1[ship_pos][0], (fleet1[ship_pos][0] + fleet1[ship_pos][3]))]
        if (row, column) in taken_by_ship:  # if row and column inside the ship
            fleet1[ship_pos][4].add((row, column))  # update ship with hit
            ship = fleet1[ship_pos]  # update fleet with new ship
            return fleet1, ship


def are_unsunk_ships_left(fleet):
    """returns Boolean value, which is `True` if there are ships in the fleet that are still not sunk,
    and `False` otherwise. Uses the is_sunk """
    for ship in fleet:  # iterate through each ship to check if they are sunk
        if not is_sunk(ship):
            return True  # returns true if any ship is found to not be sunk
    return False  # returns false if all ships are sunk


# COMMIT 7: ALL FUNCTIONS AND TESTS NOW CONSTRUCTED
def main():
    """returns nothing. It prompts the user to call out rows and columns of shots and outputs the responses of the
    computer (see *General Idea of Assignment*) iteratively until the game stops. Our expectations from this function:
    (a) there must be an option for the human player to quit the game at any time, (b) the program must never crash
    (i.e., no termination with Python error messages), whatever the human player does."""
    import extension


if __name__ == '__main__':
    main()
