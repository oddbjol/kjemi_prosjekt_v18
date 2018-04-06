import scipy.constants as constants
import random

class Grid:
    '''
    Grid class representing a 1 atom thick foil of some material (probably gold), where the atoms are evenly and 
    uniformly distributed into a lattice.
    '''
    def __init__(self, atoms_per_side, p=19.3, m_a=197):
        '''
        
        Initialize a grid with a certain number of atoms. The atoms will be uniformly spaced in both dimensions.
        
        :param atoms_per_side: How many atoms should there be in the x/y-direction? The amount of atoms will be the 
        square of this number.
        :param p: The density of the material to use, in g/cm^3. Default is for gold. 
        :param m_a: The atomic mass of the material to use, in g/mol. Default is for gold.
        '''
        self.p = p
        self.m_a = m_a

        self.d = self.distance_between_atoms()

        self.atoms_per_side = atoms_per_side
        self.total_atoms = atoms_per_side ** 2

        self.side_length = atoms_per_side * self.d
        self.area = self.side_length ** 2

    # Tested, OK!
    def reflected(self, x, y, nucleus_radius):
        '''
        Checks if a certain point (x,y) on the grid is touching a nucleus or not. If it is, a particle that hits here 
        will be reflected, and the function will return True.
        
        :param x: The x coordinate, in meters
        :param y: The y coordinate. in meters
        :param nucleus_radius: The radius of the nuclei, in meters
        :return: True if the point is touching a nucleus, False otherwise.
        '''
        if x < 0 or y < 0 or x > self.atoms_per_side*self.d or y > self.atoms_per_side * self.d:
            raise Exception('Alpha particle went out of bounds of the lattice.')


        # Simplified square bounding box of nucleus:
        # if 0.5 * self.d - nucleus_radius <= (x % self.d) <= 0.5 * self.d + nucleus_radius and \
        #     0.5 * self.d - nucleus_radius <= (y % self.d) <= 0.5 * self.d + nucleus_radius:
        #     return True
        # else:
        #     return False

        # Simplify by "moving" the alpha particle some multiple of d towards the corner, and check if it hit the corner atom.
        # If we split the foil into squares of length d, each atom is in the middle of its respective square.
        # For this reason, the corner nucleus is at point (0.5d, 0.5d)
        x_dist = abs(0.5 * self.d - (x % self.d))
        y_dist = abs(0.5 * self.d - (y % self.d))

        # Distance in meters between the point (x,y) and the nucleus occupying the same grid square
        dist = (x_dist**2 + y_dist**2) ** 0.5

        # If the distance is lower than the nucleus radius, it means the point is within the bounds of the nucleus,
        # and a particle hitting this point on the foil will be reflected.
        return dist <= nucleus_radius

    # Tested, OK!
    def random_coordinates(self):
        '''
        :return: A random point (x,y) in meters that is somewhere within the foil. 
        '''
        x = random.uniform(0, self.side_length)
        y = random.uniform(0, self.side_length)

        return x, y

    # Tested, OK!
    def bombard(self, nucleus_radius):
        '''
        Bombards the foil with a single alpha particle.
        
        :param nucleus_radius: The radius of the nuclei.
        :return: True if the alpha particle collided with a nucleus, otherwise false.
        '''
        x, y = self.random_coordinates()
        return self.reflected(x, y, nucleus_radius)

    # Tested, OK!
    def bombard_multiple(self, num, nucleus_radius):
        '''
        Bombards the foil with multiple particles.
        
        :param num: Number of alpha particles to bombard the foil with 
        :return: A number between 0 and 1, the percentage of hits. If 50% of particles collided, this will be 0.5.
        '''

        hits = 0
        for i in range(num):
            if self.bombard(nucleus_radius):
                # print("HIT!!")
                hits += 1

        print(hits, " hits of ", num, " (" , hits/num, ")")
        return hits / num

    # Tested, OK!
    def distance_between_atoms(self):
        '''
        :return: Distance along either x or y axis between two neighbouring atoms in the grid, in meters.
        '''

        #  We assume we have a cube of the material, with a volume of 1 cm^3.
        v = 1  # cm^3

        # Number of atoms in 1 this cm^3 of the substance.
        num_in_cube = ((self.p*v) / self.m_a) * constants.Avogadro

        # Number of atoms across 1 cm of the substance.
        num_along_side = num_in_cube ** (1/3)

        # Length between two neighbouring atoms, in cm
        cm_between_atoms = 1 / num_along_side  # cm

        # Remember to convert to meters.
        return cm_between_atoms/100

