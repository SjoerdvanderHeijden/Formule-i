# Rush Hour.py

class Car(object):
    """
    Car / lorry object.
    
    input: posList = list with tuples with coordinates.
    """
    def __init__(self, posList):
        self.posList = posList

        # uirekenen van richting
        if posList[0][0] == posList[1][0]:
            self.richting = 'h'
        elif posList[0][1] == posList[1][1]:
            self.richting = 'v'
        else:
            raise ValueError("Invalid coordinates!")

    def getPos(self):
        return self.posList

    def getDirection(self):
        return self.richting

    def getLength(self):
        return len(self.posList)

    def moveCar(self, distance):
        crd = self.posList
        
        if self.richting == 'h':
            for i in xrange(len(crd)):
                # x-coordinaten worden aangepast
                crd[i] = (crd[i][0] + distance, crd[i][1])
        else:
            for i in xrange(len(crd)):
                # x-coordinaten worden aangepast
                crd[i] = (crd[i][0], crd[i][1] + distance)
                
        self.posList = crd

    def isAt(self, pos):
        # @pos: type: tuple
        return pos in self.posList

class RedCar(Car):
    #het lijkt me het handigst als simulatie checkt of RedCar bij de uitgang is.
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

def runSimulation():
    pass
