# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu


import math, copy, Queue


class Car(object):
    """
    Car / lorry object.
    """
    # To identify different cars during debugging.
    # This number will be increased each time a new car is added.
    name = 1
    
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

        # debugging
        #print "hi", distance, upperLeftCoord, car.getName()
        if distance == 0:
            raise ValueError("0")
                
        if car.isHorizontal():
            #print car.getName(), "is horizontal"

            #Checks if the car can be moved if trying to go RIGHT:
            # First, checks if it is possible. 
            #   1) Checks wether the car is moved inside the parking.
            if (startPos[-1][0] + distance) >= self.width:
                raise ValueError ("Cannot move car trough the parking walls.")
            #   2) For every tile in the way of moving checks wether the way is free of cars.
            if distance > 0:
                for x in range(startPos[-1][0] + 1, \
    startPos[-1][0] +1 + distance):
                    #print "x1",x
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")
            # # !!!This part only works if the car is moved by 1 tile!!!
            # newParking.parkList[startPos[0][0]][startPos[0][1]] = None
            # newParking.parkList[startPos[-1][0]+distance][startPos[0][1]] = car
            
            # Checks wether the car can be moved if trying to go LEFT
            elif distance < 0:
                for x in range(startPos[0][0] - 1, \
    startPos[0][0] -1 + distance, -1):
                    #print "x2",x
                    if x < 0:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")

            # Second, actually moves the car (horizontal).
            for coord in startPos:
                newParking.parkList[coord[0]][coord[1]] = None
            for coord in startPos:
                newParking.parkList[coord[0]+distance][coord[1]] = car

            # newParking.parkList[startPos[-1][0]][startPos[0][1]] = None
            # newParking.parkList[startPos[0][0]+distance][startPos[0][1]] = car
            


        # If car is vertical:
        else:
            #print car.getName(),"is vertical"
            # Checks wether the car can be moved DOWN
            if distance > 0:
                for y in range(startPos[-1][1] + 1, \
    startPos[-1][1] + 1 + distance):
                    #print "y3",y
                    if y >= self.height:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")
            # # Second, actually moves the car.
            # # !!!This part only works if the car is moved by 1 tile!!!
            # newParking.parkList[startPos[0][0]][startPos[0][1]] = None
            # newParking.parkList[startPos[0][0]][startPos[-1][1]+distance] = car

            # Checks wether the car can be moved UP
            elif distance < 0:
                for y in range(startPos[0][1] - 1, \
    startPos[0][1] -1 + distance, -1):
                    #print "y4",y
                    if y < 0:
                        raise ValueError\
    ("Cannot move car trough the parking walls.")
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")   
                 
            # Second, actually moves the car (vertical).
            for coord in startPos:
                newParking.parkList[coord[0]][coord[1]] = None
            for coord in startPos:
                newParking.parkList[coord[0]][coord[1] + distance] = car

            # # !!!This part only works if the car is moved by 1 tile!!!
            # newParking.parkList[startPos[0][0]][startPos[-1][1]] = None
            # newParking.parkList[startPos[0][0]][startPos[0][1]+distance] = car
                
        return newParking


    def __key(self):
        output = ''
        for i in self.parkList:
            for j in i:
                if j == None:
                    output += '0'
                else:
                    output += str(j.getName())

        return output

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        input_data = self.parkList[:]
        output = ''

        output += '*  '
        for i in xrange(self.width):
            output += '*  '
        output += '* \n'
            
        for y in xrange(self.height):
            output += '*  '
            for x in xrange(self.width):
                if type(input_data[x][y]) == Car:
                    if input_data[x][y].getName() > 9:
                        output += str(input_data[x][y].getName()) + ' '
                    else:
                        output += str(input_data[x][y].getName()) + '  '
                elif (x,y) == self.exitPos:
                    output += '@  '
                elif input_data[x][y] == None:
                    output += '.  '
                else:
                    output += 'R  '
            output += '* \n'

        for i in xrange(self.width + 2):
            output += '*  '
        output += '\n'

        return output
                
##==========================================================================##

           
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
            oplossing = currentParking
            break

        # if currentParking in visited:
        #     print 'duplicate'

        if currentParking not in visited:
            visited.add(currentParking)

            # Keeps track of the cars that were already tried to be moved.
            visitedCars = set()

            for column in currentParking.getParking():
                # evCar voor "eventual car" ;) 
                for evCar in column:
                    if evCar != None and evCar not in visitedCars:

                        # for move in [-4,-3,-2,-1,1,2,3,4]:
                        #     try:
                        #         q.put(currentParking.moveCarInParking((x,y,),\
                        #                                                 move))
                        #     except ValueError:
                        #         pass

                        try:
                            q.put(currentParking.moveCarInParking((x, y), 1) )
                        except ValueError:
                            pass
                        try:
                            q.put(currentParking.moveCarInParking((x, y), -1) )
                        except ValueError:
                            pass
                        visitedCars.add(evCar)
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

##==========================================================================##             
    
def board_1():
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)

    rood = RedCar(2,True)
    parking1.addCar(rood,(3,2))

    blauw = Car(2,True)
    parking1.addCar(blauw,(3,0))

    oranje = Car(2,True)
    parking1.addCar(oranje,(4,3))

    blauw2 = Car(2,True)
    parking1.addCar(blauw2,(1,4))

    groen = Car(2,True)
    parking1.addCar(groen,(4,5))

    oranje2 = Car(2,False)
    parking1.addCar(oranje2,(0,4))

    vracht1 = Car(3,False)
    parking1.addCar(vracht1,(2,0))

    vracht2 = Car(3,False)
    parking1.addCar(vracht2,(5,0))

    vracht3 = Car(3,False)
    parking1.addCar(vracht3,(3,3))

    boards = BreadthFirstSimulation(parking1)

    for board in boards:
        print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'


def board_2():
    h = True
    v = False
    
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    
    rood = RedCar(2,h)
    parking1.addCar(rood,(2,2))
    
    blauw = Car(2, h)
    parking1.addCar(blauw, (2,0))
    
    oranje = Car(2, h)
    parking1.addCar(oranje, (4,0))
    
    oranje2 = Car(2,h)
    parking1.addCar(oranje2, (1,1))
    
    groen = Car(2, h)
    parking1.addCar(groen, (3,1))
    
    groen2 = Car(2, h)
    parking1.addCar(groen2, (0, 3))
    
    blauw2 = Car(2, h)
    parking1.addCar(blauw2, (2,3))
    
    groen3 = Car(2, h)
    parking1.addCar(groen3, (4,4))
    
    oranje3 = Car(2,h)
    parking1.addCar(oranje3, (4,5))
    
    oranje4 = Car(2,v)
    parking1.addCar(oranje4, (0,4))
    
    cyan = Car(2,v)
    parking1.addCar(cyan, (4,2))
    
    cyan2 = Car(2,v)
    parking1.addCar(cyan2, (3,4))
    
    vracht = Car(3,v)
    parking1.addCar(vracht, (5,1))

        
def board_3():
    exitPos2 = (5,2)
    parking1 = Parking(6,6,exitPos2)

    rood = RedCar(2, True)
    parking1.addCar(rood,(0,2))

    blauw = Car(2, True)
    parking1.addCar(blauw,(1,0))

    blauw2 = Car(2, False)
    parking1.addCar(blauw2,(3,1))

    blauw3 = Car(2, True)
    parking1.addCar(blauw3,(3,3))

    oranje = Car(2, True)
    parking1.addCar(oranje,(1,1))

    oranje2 = Car(2, False)
    parking1.addCar(oranje2,(0,4))

    groen1 = Car(2, True)
    parking1.addCar(groen1,(4,1))

    groen2 = Car(2, False)
    parking1.addCar(groen2,(2,2))

    groen3 = Car(2,False)
    parking1.addCar(groen3,(5,2))

    groen4 = Car(2,True)
    parking1.addCar(groen4,(0,3))

    groen5 = Car(2,False)
    parking1.addCar(groen5,(2,4))

    groen6 = Car(2,True)
    parking1.addCar(groen6,(4,4))

    vracht1 = Car(3,True)
    parking1.addCar(vracht1,(3,0))

    for board in BreadthFirstSimulation(parking1):
        print board


def board_4():
    h = True
    v = False
    
    exitPos1 = (8,4)
    parking1 = Parking(9,9,exitPos1)
    
    rood = RedCar(2,h)
    parking1.addCar(rood,(1,4))
    
    groen = Car(2,v)
    parking1.addCar(groen,(0,0))
    
    vracht = Car(3,h)
    parking1.addCar(vracht,(1,0))
    
    vracht2 = Car(3,v)
    parking1.addCar(vracht2, (5,0))
    
    vracht3 = Car(3,v)
    parking1.addCar(vracht3, (3,1))
    
    vracht4 = Car(3,h)
    parking1.addCar(vracht4, (6,1))
    
    vracht5= Car(3,v)
    parking1.addCar(vracht5,(8,2))
    
    blauw = Car(2,h)
    parking1.addCar(blauw, (0,3))
    
    vracht6 = Car(3,h)
    parking1.addCar(vracht6, (5,3))
    
    cyan = Car(2,v)
    parking1.addCar(cyan,(0,4))
    
    groen2 = Car(2,v)
    parking1.addCar(groen2,(3,4))
    
    vracht7 = Car(3,v)
    parking1.addCar(vracht7, (2,5))
    
    vracht8 = Car(3,h)
    parking1.addCar(vracht8, (5,6))
    
    vracht9 = Car(3,v)
    parking1.addCar(vracht9, (8,6))
    
    oranje = Car(2,h)
    parking1.addCar(oranje, (0,6))
    
    blauw2 = Car(2,v)
    parking1.addCar(blauw2, (3,6))
    
    groen3 = Car(2,h)
    parking1.addCar(groen3, (4,6))
    
    blauw3 = Car(2,v)
    parking1.addCar(blauw3, (0,7))
    
    oranje2 = Car(2,v)
    parking1.addCar(oranje2,(4,7))
    
    vracht10 = Car(2,h)
    parking1.addCar(vracht10, (1,8))
    
    cyan2 = Car(2,h)
    parking1.addCar(cyan2, (5,8))
    
    groen4 = Car(2,h)
    parking1.addCar(groen4, (7,8))


def testMoveCarInParking():             
    audi = RedCar(2,True)
    seat = Car(2,False)
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    parking1.addCar(audi, (0,2))
    parking1.addCar(seat, (3,2))

    for board in BreadthFirstSimulation(parking1):
        print board



if __name__ == '__main__':
    #testMoveCarInParking()
    board_3()

#if __name__ == '__main__':
#    # Game #2
#    h = True
#    v = False
#    
#    exitPos1 = (5,2)
#    parking1 = Parking(6,6,exitPos1)
#    
#    rood = RedCar(2,h)
#    parking1.addCar(rood,(2,2))
#    
#    blauw = Car(2, h)
#    parking1.addCar(blauw, (2,0))
#    
#    oranje = Car(2, h)
#    parking1.addCar(oranje, (4,0))
#    
#    oranje2 = Car(2,h)
#    parking1.addCar(oranje2, (1,1))
#    
#    groen = Car(2, h)
#    parking1.addCar(groen, (3,1))
#    
#    groen2 = Car(2, h)
#    parking1.addCar(groen2, (0, 3))
#    
#    blauw2 = Car(2, h)
#    parking1.addCar(blauw2, (2,3))
#    
#    groen3 = Car(2, h)
#    parking1.addCar(groen3, (4,4))
#    
#    oranje3 = Car(2,h)
#    parking1.addCar(oranje3, (4,5))
#    
#    oranje4 = Car(2,v)
#    parking1.addCar(oranje4, (0,4))
#    
#    cyan = Car(2,v)
#    parking1.addCar(cyan, (4,2))
#    
#    cyan2 = Car(2,v)
#    parking1.addCar(cyan2, (3,4))
#    
#    vracht = Car(3,v)
#    parking1.addCar(vracht, (5,1))
#    
#
#if __name__ == '__main__':
#    # Game #3
#    h = True
#    v = False
#    
#    exitPos1 = (5,2)
#    parking1 = Parking(6,6,exitPos1)
#    
#    rood = RedCar(2,h)
#    parking1.addCar(rood,(0,2))
#    
#    blauw = Car(2, h)
#    parking1.addCar(blauw, (1,0))
#    
#    oranje = Car(2,h)
#    parking1.addCar(oranje,(1,1))
#    
#    groen = Car(2,h)
#    parking1.addCar(groen, (4,1))
#    
#    groen2 = Car(2,h)
#    parking1.addCar(groen2,(0,3))
#    
#    blauw2 = Car(2,h)
#    parking1.addCar(blauw2, (3,3))
#    
#    groen3 = Car(2,h)
#    parking1.addCar(groen3, (4,4))
#    
#    blauw3 = Car(2,v)
#    parking1.addCar(blauw3, (3,1))
#    
#    cyan = Car(2,v)
#    parking1.addCar(cyan, (2,2))
#    
#    cyan2 = Car(2,v)
#    parking1.addCar(cyan2,(5,2))
#    
#    oranje2 = Car(2,v)
#    parking1.addCar(oranje2, (0,4))
#    
#    groen3 = Car(2,v)
#    parking1.addCar(groen3,(2,4))
#    
#    vracht = Car(3,h)
#    parking1.addCar(vracht,(3,0))
#
#if __name__ == '__main__':
#    # Game #4
#    h = True
#    v = False
#    
#    exitPos1 = (8,4)
#    parking1 = Parking(9,9,exitPos1)
#    
#    rood = RedCar(2,h)
#    parking1.addCar(rood,(1,4))
#    
#    groen = Car(2,v)
#    parking1.addCar(groen,(0,0))
#    
#    vracht = Car(3,h)
#    parking1.addCar(vracht,(1,0))
#    
#    vracht2 = Car(3,v)
#    parking1.addCar(vracht2, (5,0))
#    
#    vracht3 = Car(3,v)
#    parking1.addCar(vracht3, (3,1))
#    
#    vracht4 = Car(3,h)
#    parking1.addCar(vracht4, (6,1))
#    
#    vracht5= Car(3,v)
#    parking1.addCar(vracht5,(8,2))
#    
#    blauw = Car(2,h)
#    parking1.addCar(blauw, (0,3))
#    
#    vracht6 = Car(3,h)
#    parking1.addCar(vracht6, (5,3))
#    
#    cyan = Car(2,v)
#    parking1.addCar(cyan,(0,4))
#    
#    groen2 = Car(2,v)
#    parking1.addCar(groen2,(3,4))
#    
#    vracht7 = Car(3,v)
#    parking1.addCar(vracht7, (2,5))
#    
#    vracht8 = Car(3,h)
#    parking1.addCar(vracht8, (5,6))
#    
#    vracht9 = Car(3,v)
#    parking1.addCar(vracht9, (8,6))
#    
#    oranje = Car(2,h)
#    parking1.addCar(oranje, (0,6))
#    
#    blauw2 = Car(2,v)
#    parking1.addCar(blauw2, (3,6))
#    
#    groen3 = Car(2,h)
#    parking1.addCar(groen3, (4,6))
#    
#    blauw3 = Car(2,v)
#    parking1.addCar(blauw3, (0,7))
#    
#    oranje2 = Car(2,v)
#    parking1.addCar(oranje2,(4,7))
#    
#    vracht10 = Car(2,h)
#    parking1.addCar(vracht10, (1,8))
#    
#    cyan2 = Car(2,h)
#    parking1.addCar(cyan2, (5,8))
#    
#    groen4 = Car(2,h)
#    parking1.addCar(groen4, (7,8))
