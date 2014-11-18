# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu


import math, copy, Queue


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


### ======================================================================= ###
### ======================================================================= ###


class Parking(object):
    """
    Parking space with cars on it.

    input: width, height: integers. exitpos: tuple.
    """
    def __init__(self, width, height, exitPos):
        self.width = width
        self.height = height
        self.exitPos = exitPos
        self.parent = None

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

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def moveCarInParking(self, upperLeftCoord, distance):
        """
        Moves a car, by making a copy of the parking instance and 
        changing the position of the car in parkList of the copy.
        
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
        car = self.occupiedBy(upperLeftCoord)
        startPos = car.getPos(upperLeftCoord)
        # Makes a copy of the current parking. The new position of the car will 
        # be stored in this copy 
        newParking = copy.deepcopy(self)
        newParking.setParent(self)        
        
        if car.isHorizontal():
            # Moves the car to the RIGHT:
            # First, checks if it possible. For every tile in the way of moving..
            if distance > 0:
                for x in range(startPos[-1][0] + 1, \
    startPos[-1][0] + 1 + distance):
                    #..checks wether is is still in the parking.
                    if x >= self.width:
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
    startPos[0][0] - 1 + distance, -1):
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
        
        # If car is not horizontal:
        else:
            # Moving the car down
            if distance > 0:
                for y in range(startPos[-1][1] + 1, \
    startPos[-1][1] + 1 + distance):
                    if y >= self.height:
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
    startPos[0][1] - 1 + distance, -1):
                    if y < 0:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")                
            # Second, actually moves the car.
            # !!!This part only works if the car is moved by 1 tile!!!
            newParking.parkList[startPos[0][0]][startPos[-1][1]] = None
            newParking.parkList[startPos[0][0]][startPos[0][1]+distance] = car
            
        return newParking


    def __str__(self):
        output = self.parkList[:]

        print '*',
        for i in xrange(self.width):
            print '*',
        print '*'
            
        for y in xrange(self.height):
            print '*',
            for x in xrange(self.width):
                if type(output[x][y]) == Car:
                    print str(output[x][y].getName()),
                elif (x,y) == self.exitPos:
                    print '@',
                elif output[x][y] == None:
                    print '.',
                else:
                    print 'R',

            print '*'

        endRow = ''
        for i in xrange(self.width + 2):
            endRow += '* '

        return endRow
                
##==========================================================================##

def testMoveCarInParking():             
    audi = RedCar(2,True)
    seat = Car(2,False)
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    parking1.addCar(audi, (0,2))
    parking1.addCar(seat, (3,2))
    print parking1
    
    parking2 = parking1.moveCarInParking((0,2), 1)
    print parking2

    # a.k.a. botsing:
    parking3 = parking2.moveCarInParking((1,2), 1)
    print parking3

            
def BreadthFirstSimulation(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x = 0
    y = 0

    q = Queue.Queue()
    q.put(parking)

    visited = set()

    while not q.empty():
        currentParking = q.get()

        if type(currentParking.occupiedBy(currentParking.getExit())) == RedCar:
            oplossing =  currentParking
            break

        if currentParking not in visited:
            visited.add(currentParking)
            movedCars = set()

            for column in currentParking.getParking():
                # evCar voor "eventual car" ;) 
                for evCar in column:
                    if evCar != None and evCar not in movedCars:
                        try:
                            q.put(currentParking.moveCarInParking((x, y), 1) )
                            movedCars.add(evCar)
                        except ValueError:
                            pass
                        try:
                            q.put(currentParking.moveCarInParking((x, y), -1) )
                            movedCars.add(evCar)
                        except ValueError:
                            pass
                    y += 1
                x += 1
                y = 0
            x = 0
            y = 0

    route = [oplossing]
    parent = oplossing.getParent()

    while parent != None:
        route.append(parent)
        parent = parent.getParent()

    route.reverse()
    return route
                
    
if __name__ == '__main__':
    audi = RedCar(2,True)
    seat = Car(2,False)
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    parking1.addCar(audi, (0,2))
    parking1.addCar(seat, (3,2))
#    parking = BreadthFirstSimulation(parking1)
    for board in BreadthFirstSimulation(parking1):
        print board
