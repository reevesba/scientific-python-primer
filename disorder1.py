# A Primer on Scientific Programming w/ Python
# Exercise 8.36
# Bradley Reeves
# 12/4/2019

# code adapted from https://github.com/hplgit/scipro-primer/blob/master/src-4th/random/walk2Dv.py

from scitools.std import plot
import numpy, sys

class Particles_vec:
    def __init__(self, np, ns, plot_step):
        self.np = np
        self.ns = ns
        self.plot_step = plot_step
        self.xpositions = numpy.zeros(np)
        self.ypositions = numpy.zeros(np)

    def plot(self, step):
        xymin = 0; xymax = 1

        # plot every plot_step steps
        if (step+1) % self.plot_step == 0:
            plot(self.xpositions, self.ypositions, 'ko',
                 axis=[xymin, xymax, xymin, xymax],
                 title='%d particles after %d steps' % 
                       (self.np, step+1),
                 savefig='tmp_%03d.pdf' % (step+1))

    def move(self, this_move):
        # constants
        NORTH = 1;  SOUTH = 2;  WEST = 3;  EAST = 4

        # move to new position
        self.ypositions += numpy.where(this_move == NORTH, 0.01, 0)
        self.ypositions -= numpy.where(this_move == SOUTH, 0.01, 0)
        self.xpositions += numpy.where(this_move == EAST,  0.01, 0)
        self.xpositions -= numpy.where(this_move == WEST,  0.01, 0)

        # check if within bountries
        youtbounds = numpy.logical_or(self.ypositions < 0, self.ypositions > 1)
        xoutbounds = numpy.logical_or(self.xpositions < 0, self.xpositions > 1)

        # if outside area, move to relevant boundry
        for i in range(self.np):
            if youtbounds[i]:
                if self.ypositions[i] < 0.0:
                    self.ypositions[i] = 0.0
                elif self.ypositions[i] > 1.0:
                    self.ypositions[i] = 1.0

            if xoutbounds[i]:
                if self.xpositions[i] < 0.0:
                    self.xpositions[i] = 0.0
                elif self.xpositions[i] > 1.0:
                    self.xpositions[i] = 1.0

    def init_positions(self):
        self.xpositions += numpy.random.uniform(0, 0.5, self.np)
        self.ypositions += numpy.random.uniform(0, 1, self.np)

    def moves(self):
        # initialize particles to half of area
        self.init_positions()

        # generate/shape moves vector
        moves = numpy.random.random_integers(1, 4, size=self.ns*self.np)
        moves.shape = (self.ns, self.np)

        # step through simulation
        for step in range(self.ns):
            this_move = moves[step,:]
            self.move(this_move)
            self.plot(step)
        
        return self.xpositions, self.ypositions

def main():
    numpy.random.seed(11)

    np = int(sys.argv[1])           # number of particles
    ns = int(sys.argv[2])           # number of steps
    plot_step = int(sys.argv[3])    # number of time steps

    # create new particles object and simulate
    pv = Particles_vec(np, ns, plot_step)
    x, y = pv.moves()

if __name__ == '__main__':
    main()
