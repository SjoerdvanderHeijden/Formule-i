# Rush Hour.py

class Car(object):
    """
    Car / lorry object.
    """
    # To identify different cars during debugging.
    # This number will be increased each time a new car is added.
    name = 0
    
    def __init__(self, posList):
        """
        input: posList = list with tuples with all coordinates of the car.
        """
        self.posList = posList
        self.name = Car.name
        Car.name +=1

        # Calculates wether the car is an horizontal position.
        if posList[0][0] == posList[1][0]:
            self.horizontal = True
        elif posList[0][1] == posList[1][1]:
            self.horizontal = False
        else:
            raise ValueError("Invalid coordinates!")

    def getName(self):
        return self.name

    def getPos(self):
        return self.posList

    def isHorizontal(self):
        # Returns TRUE if car is in an HORIZONTAL position, FALSE if cas is in a VERTICAL position.
        return self.horizontal

    def getLength(self):
        return len(self.posList)

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
        print self.parkList

    def occupiedBy(self, pos):
        return self.parkList[pos[0]][pos[1]]
<<<<<<< HEAD
=======
    
    def moveCarInParking(self, car, distance):
        """
        Moves a car, by changing it position in the parking class and changing it's coordinates in the car class.
        
        @car: car to be moved (instance of the car class)
        @distance: distance the car is moved. Positive if the car is moved right/down and negative if it is moved left/up.
        """
        horizontal = car.isHorizontal()
        initPos = car.getPosition()
        length = car.getLength()

        
        if car.isHorizontal():
            for x-coord in (car.getPosition()[-1][0], car.getPosition()[-1][0]+distance):
                if self.parkList[x-coord][initPos[1]]!= None:
                    raise ValueError("Other car in the way")
            
            try:
                for pos in car.getPostition():
                   x, y = pos[0], pos[1]
                  self.parkList[x][y] = None
                  self.parkList[x+distance][y] = car
            except IndexError:
                raise ValueError("New position out of range.")
                
        else:
            try:
               for pos in car.getPostition():
                 x, y = pos[0], pos[1]
                 self.parkList[x][y] = None
                 self.parkList[x][y+distance] = car
            except IndexError:
                raise ValueError("New position out of range.")
            
        
            
        # Changes the coordinates of the car in its own class. 
        car.moveCar(distance)
            
            
        
        
        
>>>>>>> 770df6131a5565b7d0ac03b7a01f7cbbbe91270e

def runSimulation():
    audi = RedCar([(6,0),(6,1)])
    seat = Car([(1,2),(1,3)])
    parking = Parking(3,4,(6,6),[audi,seat])

    def verplaats(parking):
        pass # if verplaatsbaar: verplaats




    
