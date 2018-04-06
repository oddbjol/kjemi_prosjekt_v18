from Grid import Grid

def main():
    ACTUAL_RADIUS = 8.75 * 10**-16  # This isn't used anywhere, but can come in handy.

    # The percentage of particles that were reflected in the original Geiger-Marsden experiment.
    P = 1/8000  # 0.000125

    # Number of particles to bombard foil with on each experiment. If the experiment is taking too long, lower this.
    NUM_PARTICLES = 100000

    #  this is the number of atoms along one side of our grid. The size of the grid will be calculated automatically
    #  using density of gold.
    GRID_LENGTH = 100

    # Initialize a gold foil with a certain number of atoms along each side of the grid.
    grid = Grid(GRID_LENGTH)

    # We assume the nucleus radius to lie between the grid size (d), and 10^-20. If we can
    # not assume that the nucleus is bigger than 10^-20, we can always lower this to something extreme like 2^-127.
    a = grid.d
    b = 10**-20

    # We will use bisection method to find a suitable value for the nucleus radius that gives a P of 1/8000
    # We will adjust the nucleus radius up or down and see if the P from our experiment matches the P from the
    # Geiger-Marsden experiment. If our P is too low, we need to make the nucleus bigger. If our P is too big, we need
    # to make the nucleus smaller.
    nucleus_radius = 0
    old_nucleus_radius = 0

    while True:
        nucleus_radius = (a + b) / 2

        # If the current estimate is very close to the previous one, it means we've come very near the exact solution,
        # so we can stop the experiments and print out the nucleus radius.
        if abs(nucleus_radius - old_nucleus_radius) < 10**-20:
            break

        print("trying experiment with nucleus radius of: ", nucleus_radius, " m")
        if grid.bombard_multiple(NUM_PARTICLES, nucleus_radius) < P:
            b = nucleus_radius
        else:
            a = nucleus_radius

        old_nucleus_radius = nucleus_radius

    # The value of the nucleus radius has stabilized on some value. We are done.
    print("final radius of nucleus: ", nucleus_radius)


if __name__ == '__main__':
    main()
