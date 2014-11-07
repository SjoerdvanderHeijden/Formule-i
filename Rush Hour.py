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
        
        # Assigns another number to every new car
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
        # This print can be changed into a return if necessary.
        print self.parkList

    def getExit(self):
        return self.exitPos

    def occupiedBy(self, pos):
        return self.parkList[pos[0]][pos[1]]

    def moveCarInParking(self, car, distance):
        """
        Moves a car, by changing it position in the parking class and changing it's coordinates in the car class.
        
        @car: car to be moved (instance of the car class)
        @distance: distance the car is moved. Positive if the car is moved right/down and negative if it is moved left/up.
        """
        horizontal = car.isHorizontal()
        startPos = car.getPosition()
        length = car.getLength()
        
        # nextTileIndex is 1 if the car is moved right/down, and -1 if the car is moved left/up. It is also 1 if the car is not
        # moved (distance = 0). 
        # It is used to check wether the tiles the car wants to move over are free, or if another car blocks the way.
        nextTileIndex = int(math.copysign(1,distance))        
        
        if car.isHorizontal():
            for x-coord in (startPos[-nextTileIndex][0] + nextTileIndex, startPos[-nextTileIndex][0] + nextTileIndex + distance):
                # Alix : Here, hier was ik laatst bezig. -nextTileIndex klopt niet, het moet 0 zijn als de auto naar links gaat.
                # Patrick: Alix, als je je regels niet meer dan ~ 80 breed doet
                # zou dat chill zijn.
               
                if self.parkList[x-coord][startPos[0][1]] != None:
                    raise ValueError("Cannot move car, there is another car in the way.")

            
            try:
                for pos in startPos:
                    x, y = pos[0], pos[1]
                    self.parkList[x][y] = None
                    self.parkList[x+distance][y] = car
            except IndexError:
                raise ValueError("Cannot move car, there is another car in the way.")
                
        else:
            for y-coord in (startPos[0][-1], startPos[-1][0]+distance):
                if self.parkList[x-coord][startPos[1]]!= None:
                    raise ValueError("Cannot move car, there is another car in the way.")          
            try:
                for pos in startPos:
                    x, y = pos[0], pos[1]
                    self.parkList[x][y] = None
                    self.parkList[x][y+distance] = car
            except IndexError:
                raise ValueError("New position out of range.")
            
        
            
        # Changes the coordinates of the car in its own class. 
        car.moveCar(distance)
            
def BreadthFirstSimulation():
    pass
    
    
    


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

    
