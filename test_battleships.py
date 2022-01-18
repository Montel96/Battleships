import pytest
from battleships import *


@pytest.mark.parametrize("s",
                         [(2, 3, False, 3, {(2, 3), (3, 3), (4, 3)}),
                          (6, 6, True, 4, {(6, 6), (6, 7), (6, 8), (6, 9)}),
                          (9, 9, True, 1, {(9, 9)})])
def test_is_sunk1(s): # assert that ships are sunk because no more hits can be mode
    assert is_sunk(s) is True


@pytest.mark.parametrize("s",
                         [(2, 3, False, 3, {(2, 3), (4, 3)}),
                          (0, 0, False, 2, {(0, 0)})])
def test_is_sunk2(s):  # ships are not sunk because there are still hits to be made
    assert is_sunk(s) is False


@pytest.mark.parametrize("ship, appears_in_list",
                         [((4, 5, True, 4, {(4, 5), (4, 6)}), "battleship"),
                          ((1, 4, True, 3, set()), "cruiser"),
                          ((6, 8, False, 2, {(6, 8)}), "destroyer"),
                          ((9, 9, True, 1, {(9, 9)}), "submarine")]
                         )
def test_ship_type1(ship, appears_in_list): # assert that ship type returns correct name
    assert ship_type(ship) == appears_in_list


@pytest.mark.parametrize("ship, appears_in_list",
                         [((4, 5, True, 4, {(4, 5), (4, 6)}), "cruiser"),
                          ((4, 5, True, 4, {(4, 5), (4, 6)}), "destroyer"),
                          ((4, 5, True, 4, {(4, 5), (4, 6)}), "submarine"),
                          ]
                         )
def test_ship_type2(ship, appears_in_list):  # assert that ship type does not return incorrect name
    assert ship_type(ship) != appears_in_list


@pytest.mark.parametrize("row, column, fleet",
                         [(2, 3, [(0, 0, True, 4, {()}), ])])
def test_is_open_sea1(row, column, fleet):
    assert is_open_sea(row, column, fleet) is True


@pytest.mark.parametrize("row", [-9, -5, -3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 16])
@pytest.mark.parametrize("column", [-9, -5, -3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 16])
@pytest.mark.parametrize("fleet", [
    [(1, 0, True, 4, set()), (1, 6, True, 4, set()), (4, 0, True, 4, set()), (4, 6, True, 4, set()),
     (7, 0, True, 4, set()), (7, 6, True, 4, set()), (9, 0, True, 1, set()), (9, 9, True, 1, set()),
     (9, 2, True, 2, set()), (9, 6, True, 2, set())]])
# fleet is theoretical as it contains more than one ship of of length 4
def test_is_open_sea2(row, column, fleet): # test illegal fleets including negative indicies
    assert is_open_sea(row, column, fleet) is False


@pytest.mark.parametrize("ship", [(4, 4, True, 4, set()), (5, 5, True, 3, set()), (6, 6, True, 3, set())])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, set()), (2, 2, False, 3, set()), (9, 7, False, 3, set()), (8, 0, True, 2, set()),
     (3, 0, False, 2, set()), (9, 0, True, 1, set()), (9, 5, True, 1, set())]])
def test_ok_to_place_ship_at1(ship, fleet):
    assert ok_to_place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet) is True


@pytest.mark.parametrize("ship", [(1, 1, True, 4, set()), (3, 3, True, 3, set()), (9, 8, True, 3, set())])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, set()), (2, 2, False, 3, set()), (9, 7, True, 3, set()), (8, 0, True, 2, set()),
     (3, 0, False, 2, set()), (9, 0, True, 1, set()), (9, 5, True, 1, set())]])
def test_ok_to_place_ship_at2(ship, fleet):
    assert ok_to_place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet) is False


@pytest.mark.parametrize("ship, fleet",
                         [((0, 0, True, 4, set()), []),
                          ((5, 5, False, 3, set()), [(0, 0, True, 4, set())]),
                          ((2, 3, True, 2, set()), [(0, 0, True, 4, set()), (5, 5, False, 3, set())]),
                          ((9, 9, True, 1, set()),
                           [(0, 0, True, 4, set()), (5, 5, False, 3, set()), (2, 3, True, 2, set())])])
def test_place_ship_at1(ship, fleet):  # assert that ship has been placed in the last index of the fleet
    assert ship == place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet)[-1]


@pytest.mark.parametrize("ship, fleet",
                         [((9, 0, True, 4, set()), []),
                          ((0, 9, False, 3, set()), [(0, 0, True, 4, set()), (5, 5, False, 3, set())]),
                          ((5, 3, True, 2, set()),
                           [(0, 0, True, 4, set()), (5, 5, False, 3, set()), (0, 9, False, 3, set()),
                            (2, 3, True, 2, set())]),
                          ((9, 7, True, 1, set()),
                           [(0, 0, True, 4, set()), (5, 5, False, 3, set()), (0, 9, False, 3, set()),
                            (2, 3, True, 2, set()), (5, 3, True, 2, set()), (9, 9, True, 1, set())])])
def test_place_ship_at2(ship, fleet):  # assert that ship has been placed in the fleet
    assert ship in place_ship_at(ship[0], ship[1], ship[2], ship[3], fleet)


@pytest.mark.parametrize("row, column", [(0, 0), (7, 5), (2, 9)])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, set()), (5, 5, False, 3, set()), (0, 9, False, 3, set()), (2, 3, True, 2, set()),
     (5, 3, True, 2, set()), (9, 9, True, 1, set()), (9, 7, True, 1, set())]])
def test_check_if_hits1(row, column, fleet):
    assert check_if_hits(row, column, fleet) is True


@pytest.mark.parametrize("row, column", [(0, 5), (4, 1), (4, 3), (6, 0), (6, 6), (0, 0), (0, 1), (0, 9), (9, 9)])
@pytest.mark.parametrize("fleet", [
    [(0, 4, True, 4, {(0, 4), (0, 5), (0, 6), (0, 7)}), (2, 1, False, 3, {(2, 1), (3, 1), (4, 1)}),
     (4, 3, False, 3, {(4, 3), (6, 3)}), (6, 0, False, 2, {(6, 0)}), (6, 5, True, 2, {(6, 5), (6, 6)}),
     (8, 2, True, 2, set()), (6, 8, False, 1, set()), (0, 1, False, 1, {(0, 1)}), (0, 9, True, 1, {(0, 9)}),
     (8, 9, False, 1, set())]])
def test_check_if_hits2(row, column, fleet):
    assert check_if_hits(row, column, fleet) is False


@pytest.mark.parametrize("row,column", [(0, 0), (0, 3), (8, 6), (5, 5)])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, {(0, 1), (0, 2)}), (4, 5, False, 3, {(4, 5), (6, 5)}), (8, 6, False, 2, {(9, 6)})]])
def test_hit1(row, column, fleet):  # assert that the tuple was placed in the set of ship hits
    assert (row, column) in hit(row, column, fleet)[1][4]


@pytest.mark.parametrize("row,column", [(0, 0), (0, 3), (8, 6), (5, 5)])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, {(0, 1), (0, 2)}), (4, 5, False, 3, {(4, 5), (6, 5)}), (8, 6, False, 2, {(9, 6)})]])
def test_hit2(row, column, fleet):  # assert that the hit was correctly recorded in the ship
    ship_index = hit(row, column, fleet)[0].index(hit(row, column, fleet)[1])
    assert len(fleet[ship_index][4]) + 1 == len(hit(row, column, fleet)[1][4])


@pytest.mark.parametrize("row,column", [(0, 0), (0, 3), (8, 6), (5, 5)])
@pytest.mark.parametrize("fleet", [
    [(0, 0, True, 4, {(0, 1), (0, 2)}), (4, 5, False, 3, {(4, 5), (6, 5)}), (8, 6, False, 2, {(9, 6)})]])
def test_hit3(row, column, fleet):  # assert that the hit ship has been updated in the fleet
    assert hit(row, column, fleet)[0].count(hit(row, column, fleet)[1]) == 1


@pytest.mark.parametrize("fleet", [
    [(0, 4, True, 4, {(0, 4), (0, 5), (0, 6), (0, 7)}), (2, 1, False, 3, {(2, 1), (3, 1), (4, 1)}),
     (4, 3, False, 3, {(4, 3), (6, 3)}), (6, 0, False, 2, {(6, 0)}), (6, 5, True, 2, {(6, 5), (6, 6)}),
     (8, 2, True, 2, set()), (6, 8, False, 1, set()), (0, 1, False, 1, {(0, 1)}), (0, 9, True, 1, {(0, 9)}),
     (8, 9, False, 1, set())],
    [(0, 4, True, 4, {(0, 4)}), (2, 1, False, 3, {(2, 1)}), (4, 3, False, 3, {(5, 3)}), (6, 0, False, 2, set()),
     (6, 5, True, 2, {(7, 5)}),
     (8, 2, True, 2, {(9, 2)}), (6, 8, False, 1, set()), (0, 1, False, 1, {(0, 1)}), (0, 9, True, 1, {(0, 9)}),
     (8, 9, False, 1, set())],
    [(0, 4, True, 4, set()), (2, 1, False, 3, set()), (4, 3, False, 3, set()), (6, 0, False, 2, set()),
     (6, 5, True, 2, set()), (8, 2, True, 2, set()), (6, 8, False, 1, set()), (0, 1, False, 1, set()),
     (0, 9, True, 1, set()), (8, 9, False, 1, set())]
])
def test_are_unsunk_ships_left1(fleet):  # Fleets still have hits remaining so return true
    assert are_unsunk_ships_left(fleet) is True


@pytest.mark.parametrize("fleet", [
    [(0, 4, True, 4, {(0, 4), (0, 5), (0, 6), (0, 7)}), (2, 1, False, 3, {(2, 1), (3, 1), (4, 1)}),
     (4, 3, False, 3, {(4, 3), (6, 3), (5, 3)}),
     (6, 0, False, 2, {(6, 0), (7, 0)}), (6, 5, True, 2, {(6, 5), (6, 6)}), (8, 2, True, 2, {(8, 2), (8, 3)}),
     (6, 8, False, 1, {(6, 8)}), (0, 1, False, 1, {(0, 1)}), (0, 9, True, 1, {(0, 9)}), (8, 9, False, 1, {(8, 9)})],
    [(7, 2, True, 4, {(7, 2), (7, 3), (7, 4), (7, 5)}), (0, 5, True, 3, {(0, 5), (0, 6), (0, 7)}),
     (9, 2, True, 3, {(9, 2), (9, 3), (9, 4)}),
     (5, 4, True, 2, {(5, 4), (5, 5)}), (3, 0, True, 2, {(3, 0), (3, 1)}), (1, 1, True, 2, {(1, 1), (1, 2)}),
     (8, 9, False, 1, {(8, 9)}), (9, 6, False, 1, {(9, 6)}), (5, 2, True, 1, {(5, 2)}), (0, 9, True, 1, {(0, 9)})]])
def test_are_unsunk_ships_left2(fleet): # Fleets have no hits remaining, so return false
    assert are_unsunk_ships_left(fleet) is False
