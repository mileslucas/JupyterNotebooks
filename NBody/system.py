import numpy as np

#-------------------------------------------------------------------------------
"""
This class models a point particle with finite mass
"""
class Particle(object):

    def __init__(self, r, v, m=1):
        self.r = np.array(r, dtype='float64')
        self.v = np.array(v, dtype='float64')
        self.m = m
        self.rp = self.vp = 0

    def __str__(self):
        return 'Pos: '+str(self.r)+', Vel: '+str(self.v)

    # Returns the acceleration due to gravity of another body
    def acceleration(self, other):
        acc = -other.m * (self.r - other.r) / np.linalg.norm(self.r - other.r)**3
        return acc

    # Determines the new velocity and position due to given acceleration
    def update(self, a, dt):
        self.vp = a*dt
        self.rp = 0.5*a*dt**2 + self.v*dt

    # Applies the aforementioned new velocities and positions
    def apply(self):
        self.v += self.vp
        self.r += self.rp

#-------------------------------------------------------------------------------

"""
This class models a system of particle objects
"""
class System(object):

    def __init__(self, bodies=[]):
        self.bodies = bodies
        self.time = 0

    def add(self, body):
        self.bodies.append(body)

    # Solves the N-body acceleration of each body and applies it
    def update(self, dt):
        for i, b in enumerate(self.bodies):
            a = np.zeros(3)
            # The sum of the accelerations due to all OTHER bodies
            a = sum([b.acceleration(b2) for b2 in np.delete(self.bodies, i)])
            b.update(a, dt)
        for b in self.bodies:
            b.apply()
        self.time += dt

    # unpacks the position vector for every body in the system
    def unpack(self):
        r = []
        for b in self.bodies:
            r.append(b.r)
        return np.asarray(r)
