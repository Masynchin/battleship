from collections import defaultdict

from warships.warships import Warships


def test_hit_cell():
    warships = Warships(width=4, height=3)
    warships._place_ship(x0=0, y0=0, x1=3, y1=0)
    warships._place_ship(x0=0, y0=2, x1=0, y1=2)
    # 1 1 1 1
    # 0 0 0 0
    # 1 0 0 0

    for x in range(4):
        move_result = warships.hit_cell(x, cell_y=1)
        assert move_result.is_miss

    for x in range(3):
        move_result = warships.hit_cell(x, cell_y=0)
        assert move_result.is_damaged

    move_result = warships.hit_cell(cell_x=3, cell_y=0)
    assert move_result.is_destroyed

    move_result = warships.hit_cell(cell_x=0, cell_y=2)
    assert move_result.is_win



def test_get_ship_points():
    warships = Warships(width=5, height=4)
    warships._place_ship(x0=1, y0=1, x1=2, y1=1)
    warships._place_ship(x0=4, y0=0, x1=4, y1=3)
    # 0 0 0 0 1
    # 0 1 1 0 1
    # 0 0 0 0 1
    # 0 0 0 0 1

    for y in range(4):
        ship_points = set(warships.get_ship_points(cell_x=4, cell_y=y))
        assert ship_points == {(4, 0), (4, 1), (4, 2), (4, 3)}

    for x in range(1, 3):
        ship_points = set(warships.get_ship_points(cell_x=x, cell_y=1))
        assert ship_points == {(1, 1), (2, 1)}


def test_place_ships():
    warships = Warships(width=10, height=10)
    warships.place_ships()

    ships_count = defaultdict(int)
    ships_points = []
    for j, row in enumerate(warships.field):
        for i, cell in enumerate(row):
            if cell.is_ship:
                ship_points = set(warships.get_ship_points(i, j))
                if ship_points not in ships_points:
                    ships_points.append(ship_points)
                    ship_length = len(ship_points)
                    ships_count[ship_length] += 1

    assert ships_count == {4: 1, 3: 2, 2: 3, 1: 4}
