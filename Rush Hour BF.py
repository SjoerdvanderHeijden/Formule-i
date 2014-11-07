# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu


import math


class Car(object):
    """
    Car / lorry object.
    """
    # To identify different cars during debugging.
    # This number will be increased each time a new car is added.
    name = 0
    
    def __init__(self, length, horizontal):
        """
        @length: length of the car (2 or 3)
        @horizontal: True if car is horizontal, False if it is vertical
        """
        self.length = length
        self.horizontal = horizontal
        
        # Assigns new number to every new car
        self.name = Car.name
        Car.name +=1

    def getName(self):
        return self.name

    def getLength(self):
        return self.length
        
    def isHorizontal(self):
        # Returns TRUE if car is in an HORIZONTAL position, FALSE if car is in a VERTICAL position.
        return self.horizontal
        
    def getPos(self, upperLeftCoord):
        """
        Calculates the coordinates of the car, given the upper left coordinates of the car.
        
        @upperLeftCoord: most upper left coordinates, in the form (x,y).
        (tuple containing two integers)
        
        return: list of tuples corresponding to all the coordinates of the car
        """ 
        coordinates = [upperLeftCoord]
        
        # For every "piece" of the car, adds a tuple to the list coordinates, corresponding to the coordinates of that
        # piece.
        for n in range(1,self.length):
            if self.horizontal == True:
                coordinates.append((upperLeftCoord[0]+n, upperLeftCoord[1]))
            else:
                coordinates.append((upperLeftCoord[0],upperLeftCoord[1]+n))
        
        return coordinates
    
class RedCar(Car):
    """
    The car that needs to get out of the parking space.
    """
    pass

class Parking(object):
    """
    Parking space with cars on it.

    input: width, height: integers. exitpos: tuple. carlist: list
    """
    def __init__(self, width, height, exitPos):
        self.width = width
        self.height = height
        self.exitPos = exitPos
        self.carList = []

        # Parking representation is a list of lists. The lists correspond to x-coordinates, and their indexes to y-coordinates.
        # Thus: Element at position (x,y) is found at parkList[x][y]
        # If a car is positioned at (x,y), parkList[x][y] returns the car as an instance of Car, if no car is positioned at 
        # (x,y), parkList[x][y] returns None. 
        self.parkList = [ [None for y in xrange(height)] for x in xrange(width)]


    def addCar(self, car, upperLeftCoord):
        """
        Adds a Car object to Parking.

        @car: car object.
        @upperLeftCoord: position (tuple) of upper left coordinate.
        """
        for pos in car.getPos(upperLeftCoord):
            x, y = pos[0], pos[1]

            try:
                if self.parkList[x][y] == None:
                    self.parkList[x][y] = car
                else:
                    raise ValueError("Double car placing!")
                
            except IndexError:
                raise ValueError("Car out of parking range!")
        

    def getParking(self):
        # List representation of Parking (lists in list).
        # For printing in terminal just use: print 
        return self.parkList

    def getExit(self):
        return self.exitPos

    def occupiedBy(self, pos):
        return self.parkList[pos[0]][pos[1]]

    def moveCarInParking(self, car, upperLeftCoord, distance):
        """
        Moves a car, by making a copy of the parking instance and 
        changing the position of the car in parkList of the copy.
        
        @car: car to be moved (instance of the car class)
        @upperLeftCoord: upper left coordinate of the car to be moved.
        (tuple containing two integers)
        @distance: distance the car is moved. Positive if the car is moved 
        right/down and negative if it is moved left/up.
        !!! As it is written now, the car is only moved in the right
        way if the distance is +1 or -1!!!
        
        return: the parkList of the copy, with the car at another position
        (list of lists)
        """
        # Retrieves a list of tuples corresponding to the coordinates of the car
        startPos = car.getPos()
        # Makes a copy of the current parking. The new position of the car will 
        # be stored in this copy 
        newParking = deepcopy(self)
        
        if car.isHorizontal():
            # Moves the car to the RIGHT:
            # First, checks if it possible. For every tile in the way of moving..
            if distance > 0:
                for x in range(startPos[-1][0] + 1, \
    startPos[-1][0] + 1 + distance):
                    #..checks wether is is still in the parking.
                    if x >= width:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    #..checks wether the way is free of cars.
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")
            # Second, actually moves the car.
            # !!!This part only works if the car is moved by 1 tile!!!
            newParking.parkList[startPos[0][0]][startPos[0][1]] = None
            newParking.parkList[startPos[-1][0]+distance][startPos[0][1]] = car
            
            # Moving the car to the left
            if distance < 0:
                for x in range(startPos[0][0] - 1, \
    startPos[0][0] - 1 - distance, -1):
                    if x < 0:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")
            # Second, actually moves the car.
            # !!!This part only works if the car is moved by 1 tile!!!
            newParking.parkList[startPos[-1][0]][startPos[0][1]] = None
            newParking.parkList[startPos[0][0]+distance][startPos[0][1]] = car
            
        elif not car.isHorizontal():
            # Moving the car down
            if distance > 0:
                for y in range(startPos[-1][1] + 1, \
    startPos[-1][1] + 1 + distance):
                    if y >= length:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")
            # Second, actually moves the car.
            # !!!This part only works if the car is moved by 1 tile!!!
            newParking.parkList[startPos[0][0]][startPos[0][1]] = None
            newParking.parkList[startPos[0][0]][startPos[-1][1]+distance] = car

            # Moving the car up
            if distance < 0:
                for y in range(startPos[0][1] - 1, \
    startPos[0][1] - 1 - distance, -1):
                    if y < 0:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")                
            # Second, actually moves the car.
            # !!!This part only works if the car is moved by 1 tile!!!
            newParking.parkList[startPos[0][0]][startPos[-1][1]] = None
            newParking.parkList[startPos[0][0]][startPos[0][0]+distance] = car
            
        return newParking.parkList


    def __str__(self):
        output = self.parkList[:]

        for x in xrange(self.width):
            for y in xrange(self.height):
                if output[x][y] == None:
                    output[x][y] = '.'
                else:
                    output[x][y] = output[x][y].getName()

        print '*',
        for i in xrange(self.width):
            print '*',
        print '*'
            
        for y in xrange(self.height):
            print '*',
            for x in xrange(self.width):
                print str(output[x][y]),
            print '*'

        print '*',
        for i in xrange(self.width):
            print '*',
        print '*'

        return "Exit: "+ str(self.exitPos)
                

def testMoveCarInParking():             
    audi = RedCar(2,True)
    seat = Car(2,False)
    exitPos1 = (6,2)
    parking1 = Parking(6,6,exitPos1)
    parking1.addCar(audi, (0,0))
    parking1.addCar(seat, (3,2))

    print parking1

testMoveCarInParking()
            
def BreadthFirstSimulation(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x_coord = 0
    y_coord = 0
    
    for column in parking.parkList:
        # evCar voor "eventual car" ;) 
        for evCar in column:
            if evCar != None:
                try:
                    newParkinparking.moveCarInParking(evCar, (x_coord, y_coord), 1)
                except ValueError:
                    pass
            y_coord += 1
    x_coord += 1
                
    
