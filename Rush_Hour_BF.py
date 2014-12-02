# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu

import math, copy, Queue

from timeit import Timer

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput

version = "V1a"

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

        # Parking representation is a tuple of tuples. The tuples correspond to x-coordinates, and their indexes to y-coordinates.
        # Thus: Element at position (x,y) is found at parkList[x][y]
        # If a car is positioned at (x,y), parkList[x][y] returns the car as the name of the Car, if no car is positioned at 
        # (x,y), parkList[x][y] returns None. 
        self.parkList =  tuple( ( tuple((None for y in xrange(height))) for x in xrange(width)) )


    def addCar(self, car, upperLeftCoord):
        """
        Adds the name of a Car object to Parking.

        @car: car object.
        @upperLeftCoord: position (tuple) of upper left coordinate.
        """
        for pos in car.getPos(upperLeftCoord):
            x, y = pos[0], pos[1]

            try:
                if self.parkList[x][y] == None:
                    tempList = list(self.parkList)
                    tempCol = list(tempList[x])
                    tempCol[y] = car.getName()
                    tempList[x] = tuple(tempCol)
                    self.parkList = tuple(tempList)
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
        if self.parkList[pos[0]][pos[1]] == None:
            return None

        return cars[self.parkList[pos[0]][pos[1]]]

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

        # debugging
        #print "hi", distance, upperLeftCoord, car.getName()
        if distance == 0:
            raise ValueError("0")
                
        if car.isHorizontal():
            #print car.getName(), "is horizontal"

            #Checks if the car can be moved if trying to go RIGHT:
            # First, checks if it is possible. 
            #   1) Checks wether the car is moved inside the parking.
            if (startPos[-1][0] + distance) >= self.width or (startPos[0][0] + distance) < 0:
                raise ValueError ("Cannot move car trough the parking walls.")
            #   2) For every tile in the way of moving checks whether the way is free of cars.
            if distance > 0:
                nextTile = startPos[-1][0] + 1
                for x in range(nextTile, nextTile + distance):
                    #print "x1",x
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")

            
            # Checks wether the car can be moved if trying to go LEFT
            else:
                nextTile = startPos[0][0] - 1
                for x in range(nextTile, nextTile + distance, -1):
                    #print "x2",x
                    if self.parkList[x][startPos[0][1]] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")

            # Second, actually moves the car (horizontal).

            # Makes a copy of the current parking. The new position of the car will 
            # be stored in this copy 
            newParking = copy.copy(self)#copy.deepcopy(self)
            newParking.setParent(self)  

            ## Attention!! Road work ahead!!!!! ################################################
            y = upperLeftCoord[1]
            tempList = list(newParking.parkList)

            #remove:
            for pos in startPos:
                x = pos[0]

                try:
                    if tempList[x][y] == car.getName():
                        tempCol = list(tempList[x])
                        tempCol[y] = None
                        tempList[x] = tuple(tempCol)
                    else:
                        raise ValueError("Cannot remove cars other then selected!")
                    
                except IndexError:
                    raise ValueError("Cannot remove outside parking range!")

            #place:
            for pos in startPos:
                x = pos[0]+distance

                try:
                    if tempList[x][y] == None:
                        tempCol = list(tempList[x])
                        tempCol[y] = car.getName()
                        tempList[x] = tuple(tempCol)
                    else:
                        raise ValueError("Double car placing!")
                    
                except IndexError:
                    raise ValueError("Car out of parking range!")

            newParking.parkList = tuple(tempList)

            # newParking.clearTiles(car, startPos[0])
            # newParking.addCar(car, (startPos[0][0]+distance,startPos[0][1]) )
            


        # If car is vertical:
        else:
            if (startPos[-1][1] + distance) >= self.height or (startPos[0][1] + distance) < 0:
                raise ValueError ("Cannot move car trough the parking walls.")
            # Checks wether the car can be moved DOWN
            if distance > 0:
                nextTile = startPos[-1][1] + 1
                for y in range(nextTile, nextTile + distance):
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")


            # Checks wether the car can be moved UP
            else:
                nextTile = startPos[0][1] - 1
                for y in range(nextTile, nextTile + distance, -1):
                    if self.parkList[startPos[0][0]][y] != None:
                        raise ValueError\
    ("Cannot move car, there is another car in the way.")   
                 
            # Second, actually moves the car (vertical).

            # Makes a copy of the current parking. The new position of the car will 
            # be stored in this copy 
            newParking = copy.copy(self)
            newParking.setParent(self)  


            ## Attention!! Road work ahead!!!!! ################################################
            x = upperLeftCoord[0]
            tempList = list(newParking.parkList)
            tempCol = list(tempList[x])

            #clear:
            for pos in startPos:
                y = pos[1]

                try:
                    if tempCol[y] == car.getName():
                        tempCol[y] = None
                    else:
                        raise ValueError("Cannot remove cars other then selected!")
                    
                except IndexError:
                    raise ValueError("Cannot remove outside parking range!")

            #place:
            for pos in startPos:
                y = pos[1]+distance

                try:
                    if tempCol[y] == None:
                        tempCol[y] = car.getName()
                    else:
                        raise ValueError("Double car placing!")
                    
                except IndexError:
                    raise ValueError("Car out of parking range!")

            tempList[x] = tuple(tempCol)
            newParking.parkList = tuple(tempList)

            # newParking.clearTiles(car, startPos[0])
            # newParking.addCar(car, (startPos[0][0],startPos[0][1]+distance) )

                
        return newParking


    def __eq__(x, y):
        return x.parkList == y.parkList

    def __hash__(self):
        return hash(self.parkList)

    def __str__(self):
        input_data = self.parkList[:]
        output = ''

        exitRow = self.exitPos[1]

                   
        for y in xrange(self.height):
            output += ' '
            for x in xrange(self.width):
                if input_data[x][y] > 1:
                    if input_data[x][y] > 9:
                        output += str(input_data[x][y]) + ' '
                    else:
                        output += str(input_data[x][y]) + '  '
                elif input_data[x][y] == None:
                    output += '.  '
                elif input_data[x][y] == 1:
                    output += 'R  '
                else:
                    output += '#  '

            if y == exitRow:
                output += '<--'
            output += '\n'

        output += '\n'

        return output
        
##==========================================================================##
def saveResults(name, output):
"""
Create text file with results
@name: string
@output: List of boards, solution of simulation
"""
    name = name+".txt"
    
    try: 
        file = open(name,'r+')
        raise ValueError("File already exists.")
    except:
        file = open(name, 'w')
        file.write(output simulation as string)

##==========================================================================##
#profilers
           
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

                        ##### more tiles is 1 step: #####

                        for move in xrange(-1,-5,-1):
                            try:
                                q.put(currentParking.moveCarInParking((x,y,),\
                                                                        move))
                            except ValueError:
                                break

                        for move in xrange(1,5):
                            try:
                                q.put(currentParking.moveCarInParking((x,y,),\
                                                                        move))
                            except ValueError:
                                break

                        ##### 1 tile is 1 step: #####

                        # try:
                        #     q.put(currentParking.moveCarInParking((x, y), 1) )
                        # except ValueError:
                        #     pass
                        # try:
                        #     q.put(currentParking.moveCarInParking((x, y), -1) )
                        # except ValueError:
                        #     pass
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

    global cars
    cars = [None]

    cars.append(RedCar(2,True))
    parking1.addCar(cars[-1],(3,2))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(3,0))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(4,3))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(1,4))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(4,5))

    cars.append(Car(2,False))
    parking1.addCar(cars[-1],(0,4))

    cars.append(Car(3,False))
    parking1.addCar(cars[-1],(2,0))

    cars.append(Car(3,False))
    parking1.addCar(cars[-1],(5,0))

    cars.append(Car(3,False))
    parking1.addCar(cars[-1],(3,3))

    boards = BreadthFirstSimulation(parking1)

    for board in boards:
        print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'


def board_2():
    h = True
    v = False
    
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)

    global cars
    cars = [None]
    
    cars.append(RedCar(2,h))
    parking1.addCar(cars[-1],(2,2))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (2,0))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (4,0))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (1,1))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (3,1))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (0,3))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (2,3))
    
    cars.append(Car(2, h))
    parking1.addCar(cars[-1], (4,4))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (4,5))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1], (0,4))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1], (4,2))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1], (3,4))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1], (5,1))

    boards = BreadthFirstSimulation(parking1)

    for board in boards:
        print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

        
def board_3():
    exitPos2 = (5,2)
    parking1 = Parking(6,6,exitPos2)
    global cars
    cars = [None]

    cars.append(RedCar(2, True))
    parking1.addCar(cars[-1],(0,2))

    cars.append(Car(2, True))
    parking1.addCar(cars[-1],(1,0))

    cars.append(Car(2, False))
    parking1.addCar(cars[-1],(3,1))

    cars.append(Car(2, True))
    parking1.addCar(cars[-1],(3,3))

    cars.append(Car(2, True))
    parking1.addCar(cars[-1],(1,1))

    cars.append(Car(2, False))
    parking1.addCar(cars[-1],(0,4))

    cars.append(Car(2, True))
    parking1.addCar(cars[-1],(4,1))

    cars.append(Car(2, False))
    parking1.addCar(cars[-1],(2,2))

    cars.append(Car(2,False))
    parking1.addCar(cars[-1],(5,2))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(0,3))

    cars.append(Car(2,False))
    parking1.addCar(cars[-1],(2,4))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1],(4,4))

    cars.append(Car(3,True))
    parking1.addCar(cars[-1],(3,0))

    boards = BreadthFirstSimulation(parking1)

    for board in boards:
        print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'


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

    boards = BreadthFirstSimulation(parking1)

 #   for board in boards:
#        print board
#
#    print 'Opgelost in:', len(boards)-1, ' stappen.'
    return boards, len(boards)-1 

def testMoveCarInParking():             
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    global cars
    cars = [None]

    cars.append(RedCar(2,True))
    parking1.addCar(cars[-1], (0,2))

    cars.append(Car(2,False))
    parking1.addCar(cars[-1], (3,2))

    boards = BreadthFirstSimulation(parking1)

    for board in boards:
        print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'



if __name__ == '__main__':
    #board_3()
    #testMoveCarInParking()

    t = Timer(lambda: board_3())
    print t.timeit(number=1)


    # with PyCallGraph(output=GraphvizOutput()):
    #     board_3()

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
