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
        return len(self.posList)
        
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
            elif self.horizontal == False:
                coordinates.append((upperLeftCoord[0],upperLeftCoord[1]+n))
        
        return coordinates


    def moveCar(self, distance):
        """
        Changes the coordinates of the car by changing self.posList
            
        @distance: Number of tiles the car is moved. Positive if the car is moved right/down, negative if moved left/up.
        """
        coord = self.getPos()
        
        if self.isHorizontal():
            for i in xrange(len(coord)):
                # x-coordinates are adjusted
                coord[i] = (coord[i][0] + distance, coord[i][1])
        else:
            for i in xrange(len(coord)):
                # y-coordinates are adjusted
                coord[i] = (coord[i][0], coord[i][1] + distance)
                
        self.posList = coord

    def isAt(self, pos):
        # @pos: type: tuple
        return pos in self.posList
        
        
    
    

class RedCar(Car):
    # It is probably better if simulation or parking checks wether the red car is at the exit.
    pass

class Parking(object):
    """
    Parking space with cars on it.

    input: width, height: integers. exitpos: tuple. carlist: list
    """
    def __init__(self, width, height, exitPos, carList):
        self.width = width
        self.height = height
        self.exitPos = exitPos

        # Parking representation is a list of lists. The lists correspond to x-coordinates, and their indexes to y-coordinates.
        # Thus: Element at position (x,y) is found at parkList[x][y]
        # If a car is positioned at (x,y), parkList[x][y] returns the car as an instance of Car, if no car is positioned at 
        # (x,y), parkList[x][y] returns None. 
        self.parkList = [ [None for y in xrange(height)] for x in xrange(width)]

        # Cars are added at their position
        for car in carList:
            posList = car.getPos()
            
            for pos in posList:
                x, y = pos[0], pos[1]

                try:
                    if self.parkList[x][y] == None:
                        self.parkList[x][y] = car
                    else:
                        raise ValueError("Double car placing!")
                    
                except IndexError:
                    raise ValueError("Car out of parking range!")
                

    def getParking(self):
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
        startPos = car.getPosition()
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
            
                # Patrick: Alix, als je je regels niet meer dan ~ 80 breed doet
                # zou dat chill zijn.
                
def printParking(parking):
    """
    prints the list of lists of a parking in a nice way
    """
    for row in parking.parkList:
        print row

def testMoveCarInParking():             
    audi = RedCar([(6,0),(6,1)])
    seat = Car([(1,2),(1,3)])
    exitPos1 = (6,6)
    parking1 = Parking(6,6,exitPos1,[audi,seat])   

    printParking(parking1)

testMoveCarInParking()
            
def BreadthFirstSimulation(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x-coord = 0
    y-coord = 0
    
    for column in parking.parkList:
        # evCar voor "eventual car" ;) 
        for evCar in column:
            if evCar != None:
                try:
                    newParkinparking.moveCarInParking(evCar, (x-coord, y-coord), 1)
                except ValueError:
                    pass
            y-coord += 1
    x-coord += 1
                
    
    
    


def runSimulation():
    audi = RedCar([(6,0),(6,1)])
    seat = Car([(1,2),(1,3)])
    exitPos1 = (6,6)
    parking1 = Parking(3,4,exitPos1,[audi,seat])

    solutions = []
    solve(parking1)


### !!! IK BEDENK ME NET DAT WE GEEN COORDINATEN IN 'CAR' MOETEN OPSLAAN.
# ER KOMEN NAMELIJK ALLEMAAL PARKEERPLAATSEN DIE NAAR DEZELFDE AUTO('S) WIJZEN..

    def solve(parking):
        # Patrick: er moet nog iets komen tegen loops + er moet bepaald worden
        # hoe er wordt gecheckt wanneer een puzzel is opgelost.
        if not solved:
            for car in cars:
                # Dit gaat alleen werken als moveCarInParking een nieuw
                #  Parking object returned.
                solve(parking.moveCarInParking(car, 1))
                solve(parking.moveCarInParking(car, -1))
                
        else:
            save solution

    
