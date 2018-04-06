from Grid import Grid

# Check that the random coordinates never fall outside of the foil.
def test_random_coordinates():
    grid = Grid(10)
    for i in range(100000):
        x,y = grid.random_coordinates()
        assert 0 < x <= grid.side_length
        assert 0 < y <= grid.side_length