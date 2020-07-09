from jyro.simulator import *
from IPython.display import display, clear_output
import math
import random
import time

# initialize simulation
sim = Physics()

# add objects to simulation object
def addObjects(sim):
    sim.addBox(0, 0, 5, 5, fill="backgroundgreen", wallcolor="lightgrey") # meters
    sim.addBox(1, 1, 2, 2, "purple")
    sim.addLight(4, 4, 1.00, color=Color(255, 255, 0, 64))
    sim.addLight(4, 2, 1.00, color=Color(255, 255, 0, 64))

# add objects
addObjects(sim)

# create this robot class
class MyPioneer(Pioneer):
    def __init__(self, name, x, y, angle):
        Pioneer.__init__(self, name, x, y, angle)
        self.name = name
        self.addDevice(PioneerFrontSonars(maxRange=5.0))
        self.addDevice(PioneerFrontLightSensors(5))

    # define behavior as method
    def brain(self, robot):
        self.move(random.random() * 2 - 1,
                  random.random() * 2 - 1)

        # information below defines the sensor frame relative to the bot
        # assume robot heading to be 90 degrees
        # first ray at 0, last ray at 180
        # 8 total beams at 180/7 deg intervals 
        start_angle = 0; end_angle = 180; interval = 180.0/7

        # angle generator func
        def angle_gen(i): return start_angle + interval * i

        # generate angles for each beam
        angles = []
        for i in range(0, 8):
            angles.append(angle_gen(i))

        # get sensor and start counting from first light ray
        sensor = self.devices[1]
        points = []
        count = 0

        # calculate relative projected detected point position
        for r in self.devices[1].getData():

            # project points by their range and angle of beam
            projected_x = math.cos(math.radians(angles[count])) * r
            projected_y = math.sin(math.radians(angles[count])) * r

            # add projected point to list of all points and increase count
            points.append((projected_x, projected_y))
            count += 1
        print(points)
            
# define robot params 
robot = MyPioneer("Pioneer", 2.50, 4.50, math.pi / 2) 

# add robot to world
sim.addRobot(robot)
canvas = Canvas((250, 250))
sim.draw(canvas)

# teleport to position
robot.move(5, 5)

# run simulator for a range of time
for i in range(70):

    # run with brain
    sim.step(run_brain=True)

    # for each robot in sim
    for r in sim.robots:

        # add canvas to sim
        sim.draw(canvas)
        clear_output(wait=True)
        # is currrently not displaying the canvas 
        # display(canvas)
        time.sleep(.085) # sleep for a bit