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

        # Calculates the direction of the car: horizontal or vertical
        if posList[0][0] == posList[1][0]:
            self.direction = 'h'
        elif posList[0][1] == posList[1][1]:
            self.direction = 'v'
        else:
            raise ValueError("Invalid coordinates!")

    def getPos(self):
        return self.posList

    def getDirection(self):
        return self.direction

    def getLength(self):
        return len(self.posList)

    def moveCar(self, distance):
        coord = self.getPos()
        
        if self.richting == 'h':
            for i in xrange(len(coord)):
                # x-coordinaten worden aangepast
                coord[i] = (coord[i][0] + distance, coord[i][1])
        else:
            for i in xrange(len(coord)):
                # x-coordinaten worden aangepast
                coord[i] = (coord[i][0], coord[i][1] + distance)
                
        self.posList = coord

    def isAt(self, pos):
        # @pos: type: tuple
        return pos in self.posList

class RedCar(Car):
    # het lijkt me het handigst als simulatie checkt of RedCar bij de uitgang is.
    pass

class Parking(object):
    """
    Parking space with cars on it.

    input: width, height: integers. exitpos: tuple. carlist: list
    """
    def __init__(self, width, height, exitpos, carList):
        self.width = width
        self.height = height
        self.exitpos = exitpos

        # Parking representatie (lijst met lijsten).
        # (x,y) aanroepen door: parkList[x][y]
        self.parkList = [ [None for y in xrange(height)] for x in xrange(width)]

        # Auto's worden geplaatst.
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
    
    def 

def runSimulation():
    pass
