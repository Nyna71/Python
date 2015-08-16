# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanedTiles = []
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        i = int(pos.getX())
        j = int(pos.getY())
        if not self.isTileCleaned(i, j):
            self.cleanedTiles.append((i, j))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.cleanedTiles.count((m, n)) == 1
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanedTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.random() * self.width
        y = random.random() * self.height
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX() > 0 and pos.getX() < self.width and \
            pos.getY() > 0 and pos.getY() < self.height 


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = random.randint(0, 359)
        self.position = self.room.getRandomPosition()
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError
            

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        while True:
            newPosition = self.position.getNewPosition(self.direction, self.speed)
            if self.room.isPositionInRoom(newPosition):
                self.setRobotPosition(newPosition)
                break
            else:
                self.setRobotDirection(random.randint(0, 359))
        
        self.room.cleanTileAtPosition(self.getRobotPosition())

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """    
    timeSteps = []
    
    for i in range(num_trials):
        #Prepare room and robot visuaalizations
        #anim = ps6_visualize.RobotVisualization(num_robots, width, height)        
        
        #Same room is shared by multiple robots
        room = RectangularRoom(width, height)
        robots = []
        for r in range(num_robots):
            robots.append(robot_type(room, speed))

        nbrSteps = 0
        roomIsNotCleaned = True
        
        while roomIsNotCleaned:
            for robot in robots:
                robot.updatePositionAndClean()
                if float(room.getNumCleanedTiles()) / room.getNumTiles() >= min_coverage:
                    roomIsNotCleaned = False
                    break
            nbrSteps += 1
            #anim.update(room, robots)
        timeSteps.append(nbrSteps)
    
    #anim.done()      
    return pylab.mean(timeSteps)    


# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    cleanSteps = []
    
    for robots in range(1, 11):
        cleanSteps.append(runSimulation(robots, 1.0, 20, 20, 0.8, 10, StandardRobot))
    
    pylab.figure()
    pylab.plot(range(1,11), cleanSteps)
    pylab.xlabel("Nbr robots")
    pylab.ylabel("Mean Steps")
    pylab.title("Mean time to clean 80% or a 20x20 room using 1-10 standard robots")
    pylab.show()
    
    cleanSteps = []
    xLabel = []
    rooms = [(20,20), (25,16), (40,10), (50,8), (80,5), (100,4)]
    
    for room in rooms:
        cleanSteps.append(runSimulation(2, 1.0, room[0], room[1], 0.8, 10, StandardRobot))
        xLabel.append(room[0] / room[1])
        
    pylab.figure()
    pylab.plot(xLabel, cleanSteps)
    pylab.xlabel("Width / Height ratio")
    pylab.ylabel("Mean Steps")
    pylab.title("Mean time to clean 80% of various 20x20 rooms using 2 standard robots")
    pylab.show()
    
    cleanSteps = []
    xLabel = []
    rooms = [(5,5), (10,10), (10,20), (20,20), (30,30), (40,40)]
    
    for room in rooms:
        cleanSteps.append(runSimulation(3, 1.0, room[0], room[1], 0.7, 10, StandardRobot))
        xLabel.append(room[0] * room[1])
        
    pylab.figure()
    pylab.plot(xLabel, cleanSteps)
    pylab.xlabel("Rooms area")
    pylab.ylabel("Mean Steps")
    pylab.title("Mean time to clean 70% of various room areas using 3 standard robots")
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    cleanSteps = []
    
    for robots in range(1, 11):
        cleanSteps.append(runSimulation(robots, 1.0, 20, 20, 0.8, 10, RandomWalkRobot))
    
    pylab.figure()
    pylab.plot(range(1,11), cleanSteps)
    pylab.xlabel("Nbr robots")
    pylab.ylabel("Mean Steps")
    pylab.title("Mean time to clean 80% or a 20x20 room using 1-10 random walk robots")
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        while True:
            newPosition = self.position.getNewPosition(self.direction, self.speed)
            self.setRobotDirection(random.randint(0, 359))
            if self.room.isPositionInRoom(newPosition):
                self.setRobotPosition(newPosition)
                break
        
        self.room.cleanTileAtPosition(self.getRobotPosition())
