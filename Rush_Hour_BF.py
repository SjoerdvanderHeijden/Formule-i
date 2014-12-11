# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu

import math, copy, Queue, time, heapq

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput

version = "V3"

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
        # start = time.time()
        # global getpostime
        
        coordinates = [upperLeftCoord]
        length = self.length
        horizontal = self.horizontal
        # For every "piece" of the car, adds a tuple to the list coordinates, corresponding to the coordinates of that
        # piece.
        for n in xrange(1,length):
            if horizontal:
                coordinates.append((upperLeftCoord[0]+n, upperLeftCoord[1]))
            else:
                coordinates.append((upperLeftCoord[0],upperLeftCoord[1]+n))
        
        
        # getpostime += time.time() - start

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

    
    def moveCarInParking(self, upperLeftCoord):
        """
        A generator object that yields parking instances.

        Tries to move a car in both directions, by making a copy of the parking instance and 
        changing the position of the car in parkList of the copy.
        
        @upperLeftCoord: upper left coordinate of the car to be moved.
        (tuple containing two integers)
        """
        # Retrieves a list of tuples corresponding to the coordinates of the car
        car = self.occupiedBy(upperLeftCoord)
        startPos = car.getPos(upperLeftCoord)

        if car.isHorizontal():
            prevx = startPos[0][0] - 1
            firstx = startPos[0][0]
            lastx = startPos[-1][0]
            nextx = startPos[-1][0] + 1

            # Checks if the car can be moved to the RIGHT:
            if nextx < self.width and self.parkList[nextx][startPos[0][1]] == None:
                # Makes a copy of the current parking. The new position of the car will 
                # be stored in this copy 
                newParking = copy.copy(self)
                newParking.setParent(self)
                tempList = list(newParking.parkList)
                y = upperLeftCoord[1]      

                canMove = True          

                while canMove:
                    #remove:
                    tempCol = list(tempList[firstx])
                    tempCol[y] = None
                    tempList[firstx] = tuple(tempCol)

                    #place:
                    tempCol = list(tempList[nextx])
                    tempCol[y] = car.getName()
                    tempList[nextx] = tuple(tempCol)

                    # return new parking:
                    newParking.parkList = tuple(tempList)
                    yield newParking

                    firstx +=1
                    nextx +=1

                    if nextx >= self.width or self.parkList[nextx][startPos[0][1]] != None:
                        canMove = False

            # Checks if the car can be moved to the LEFT:
            if prevx >= 0 and self.parkList[prevx][startPos[0][1]] == None:
                # Makes a copy of the current parking. The new position of the car will 
                # be stored in this copy 
                newParking = copy.copy(self)
                newParking.setParent(self)
                tempList = list(newParking.parkList)
                y = upperLeftCoord[1]      

                canMove = True          

                while canMove:
                    #remove:
                    tempCol = list(tempList[lastx])
                    tempCol[y] = None
                    tempList[lastx] = tuple(tempCol)

                    #place:
                    tempCol = list(tempList[prevx])
                    tempCol[y] = car.getName()
                    tempList[prevx] = tuple(tempCol)

                    # return new parking:
                    newParking.parkList = tuple(tempList)
                    yield newParking

                    prevx -=1
                    lastx -=1

                    if prevx < 0 or self.parkList[prevx][startPos[0][1]] != None:
                        canMove = False


        # If car is vertical:
        else:
            prevy = startPos[0][1] - 1
            firsty = startPos[0][1]
            lasty = startPos[-1][1]
            nexty = startPos[-1][1] + 1

            # Checks if the car can be moved DOWN:
            if nexty < self.height and self.parkList[startPos[0][0]][nexty] == None:
                # Makes a copy of the current parking. The new position of the car will 
                # be stored in this copy 
                newParking = copy.copy(self)
                newParking.setParent(self)

                x = upperLeftCoord[0]
                tempList = list(newParking.parkList)
                tempCol = list(tempList[x])

                canMove = True

                while canMove:
                    #remove:
                    tempCol[firsty] = None

                    #place:
                    tempCol[nexty] = car.getName()

                    # return new parking:
                    tempList[x] = tuple(tempCol)                    
                    newParking.parkList = tuple(tempList)
                    yield newParking

                    firsty +=1
                    nexty +=1

                    if nexty >= self.height or self.parkList[startPos[0][0]][nexty] != None:
                        canMove = False
            
            # Checks if the car can be moved UP:
            if prevy >= 0 and self.parkList[startPos[0][0]][prevy] == None:
                # Makes a copy of the current parking. The new position of the car will 
                # be stored in this copy 
                newParking = copy.copy(self)
                newParking.setParent(self)

                x = upperLeftCoord[0]
                tempList = list(newParking.parkList)
                tempCol = list(tempList[x])

                canMove = True

                while canMove:
                    #remove:
                    tempCol[lasty] = None

                    #place:
                    tempCol[prevy] = car.getName()

                    # return new parking:
                    tempList[x] = tuple(tempCol)                    
                    newParking.parkList = tuple(tempList)
                    yield newParking

                    lasty -=1
                    prevy -=1

                    if prevy < 0 or self.parkList[startPos[0][0]][prevy] != None:
                        canMove = False



    def __eq__(a, b):
        return a.parkList == b.parkList

    def __hash__(self):
        return hash(self.parkList)

    def __str__(self):
        input_data = self.parkList[:]
        output = ''

        # exitRow = self.exitPos[1]
        
        for y in xrange(self.height):
            output += ' '
            for x in xrange(self.width):
                if input_data[x][y] > 0:
                    if input_data[x][y] > 9:
                        output += str(input_data[x][y]) + ' '
                    else:
                        output += str(input_data[x][y]) + '  '
                elif input_data[x][y] == None:
                    output += '.  '

                # Als er een onbekend object in staat (iets fout is gegaan)
                else:
                    output += '#  '

            # if y == exitRow:
            #     output += '<--'
            output += '\n'

        output += '\n'

        return output

    def printOutput(self):
        input_data = self.parkList[:]
        output = ''

        # exitRow = self.exitPos[1]
        
        for x in xrange(self.width):
            output += ' '
            for y in xrange(self.height):
                if input_data[x][y] > 0:
                    if input_data[x][y] > 9:
                        output += str(input_data[x][y]) + ' '
                    else:
                        output += str(input_data[x][y]) + '  '
                elif input_data[x][y] == None:
                    output += '.  '
                else:
                    output += '#  '

            # if y == exitRow:
            #     output += '<--'
            output += '\n'

        output += '\n'

        return output
        
#def priorityqueuesimulation():
    # https://docs.python.org/2/library/heapq.html#module-heapq
        
##==========================================================================##

def saveResults(function, fileName):
    """
    Creates text file with the solution to a board described in the argument 
    function. The solution is written to the text file as boards, as coded in 
    __str__ of the class board. saveResults will overwrite the previously made 
    file if fileName is not changed. 

    @function: Function that returns the solution to a board as a list of boards.
    @fileName: Name of the result file. The version of the code that was used 
    to obtain the solution will automatically be added to the name of the 
    file (string)
    """
    name = str(fileName + "_" + version + ".txt")

    file = open(name, 'w')

    start = time.time()
    boards = function()
    stop = time.time()

    file.write("Solved in " + str(len(boards)-1) + " steps.\n")

    file.write("Time took: " + str(stop-start) + "seconds." + "\n")

    file.write("Exit coordinate: "+ '\n' + str(boards[0].exitPos[0])\
    + "\n"+ str(boards[0].exitPos[1])+"\n")

    for board in boards:
        file.write(board.printOutput())
        
    file.write("--------------------END--------------------\n")
        
    for board in boards:
        file.write(str(board))

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

    length = max(parking.width, parking.height)-1

    # q = Queue.Queue()
    # q.put(parking)

    h = []
    heapq.heappush(h, (1, parking))

    visitedParkings = set()

    while True:
        currentParking = heapq.heappop(h) #q.get()

        if type(currentParking.occupiedBy(currentParking.getExit())) == RedCar:
            oplossing = currentParking
            break

        if currentParking not in visitedParkings:
            visitedParkings.add(currentParking)

            # Keeps track of the cars that were already tried to be moved.
            visitedCars = set()

            for column in currentParking.getParking():
                # evCar voor "eventual car" ;) 
                for evCar in column:
                    if evCar != None and evCar not in visitedCars:

                        for move in currentParking.moveCarInParking((x,y)):
                            # q.put(move)
                            heapq.heappush(h,(heuristiek, move))

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


    # for board in boards:
    #     print board

    # print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards

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


    # for board in boards:
    #     print board

    # print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards
        

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


    # for board in boards:
    #     print board

    # print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


def board_4():
    h = True
    v = False
    
    exitPos1 = (8,4)
    parking1 = Parking(9,9,exitPos1)

    global cars
    cars = [None]
    
    cars.append(RedCar(2,h))
    parking1.addCar(cars[-1],(1,4))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1],(0,0))
    
    cars.append(Car(3,h))
    parking1.addCar(cars[-1],(1,0))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1], (5,0))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1], (3,1))
    
    cars.append(Car(3,h))
    parking1.addCar(cars[-1], (6,1))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1],(8,2))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (0,3))
    
    cars.append(Car(3,h))
    parking1.addCar(cars[-1], (5,3))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1],(0,4))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1],(3,4))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1], (2,5))
    
    cars.append(Car(3,h))
    parking1.addCar(cars[-1], (5,5))
    
    cars.append(Car(3,v))
    parking1.addCar(cars[-1], (8,5))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (0,6))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1], (3,6))
  
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (4,6))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1], (0,7))
    
    cars.append(Car(2,v))
    parking1.addCar(cars[-1],(4,7))
    
    cars.append(Car(3,h))
    parking1.addCar(cars[-1], (1,8))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (5,8))
    
    cars.append(Car(2,h))
    parking1.addCar(cars[-1], (7,8))

    boards = BreadthFirstSimulation(parking1)

 #   for board in boards:
#        print board
#
#    print 'Opgelost in:', len(boards)-1, ' stappen.'
    return boards



def board_5():
    h = True
    v = False

    exitPos5 = (8,4)
    parking5 = Parking(9,9,exitPos5)

    global cars
    cars = [None]

    cars.append(RedCar(2,h))
    parking5.addCar(cars[-1],(6,4))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(7,1))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(4,2))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(4,3))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(7,3))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(3,6))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(6,6))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(2,7))

    cars.append(Car(2,h))
    parking5.addCar(cars[-1],(2,8))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(5,0))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(6,0))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(6,2))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(0,5))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(2,5))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(0,7))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(1,7))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(4,7))

    cars.append(Car(2,v))
    parking5.addCar(cars[-1],(8,7))

    cars.append(Car(3,h))
    parking5.addCar(cars[-1],(0,0))

    cars.append(Car(3,h))
    parking5.addCar(cars[-1],(2,4))

    cars.append(Car(3,h))
    parking5.addCar(cars[-1],(5,7))

    cars.append(Car(3,v))
    parking5.addCar(cars[-1],(3,0))

    cars.append(Car(3,v))
    parking5.addCar(cars[-1],(5,4))

    cars.append(Car(3,v))
    parking5.addCar(cars[-1],(8,4))


    boards = BreadthFirstSimulation(parking5)

 #   for board in boards:
#        print board
#
#    print 'Opgelost in:', len(boards)-1, ' stappen.'
    return boards


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

    # for board in boards:
    #     print board

    # print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


if __name__ == '__main__':

    # saveResults(board_4, "board_4")


    ##------------------------------------------

    # board_1()
    # testMoveCarInParking()

    ##------------------------------------------


    # horizontaltime = 0
    # verticaltime = 0
    # getpostime = 0

    starttot = time.time()
    boards = board_3()
    stoptot = time.time()

    print "total time: ", stoptot-starttot
    # print "horizontal: ", horizontaltime
    # print "vertical: ", verticaltime
    # print "getpos: ", getpostime

    ##------------------------------------------

    # with PyCallGraph(output=GraphvizOutput()):
    #     board_3()


