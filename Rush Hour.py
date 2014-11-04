# Rush Hour.py

class Car(object):
    """
    Car / lorry object.
    """
    def __init__(self, posList):
        """
        input: posList = list with tuples with all coordinates of the car.
        """
        self.posList = posList

        # Calculates wether the car is an horizontal position.
        if posList[0][0] == posList[1][0]:
            self.horizontal = True
        elif posList[0][1] == posList[1][1]:
            self.horizontal = False
        else:
            raise ValueError("Invalid coordinates!")

    def getPos(self):
        return self.posList

    def isHorizontal(self):
        # Returns TRUE if car is in an HORIZONTAL position, FALSE if cas is in a VERTICAL position.
        return self.horizontal

    def getLength(self):
        return len(self.posList)

    def moveCar(self, distance):
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
        print self.parkList

    def occupiedBy(self, pos):
        return self.parkList[pos[0]][pos[1]]
    
    def moveCarInParking(self, car, distance):
        """
        Moves a car, by changing it position in the parking class and changing it's coordinates in the car class.
        
        @car: car to be moved (instance of the car class)
        @distance: distance the car is moved. Positive if the car is moved right/down and negative if it is moved left/up.
        """
        horizontal = car.isHorizontal()
        
        
        
        

def runSimulation():
    pass
