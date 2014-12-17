# Rush Hour.py
# Contributors: Patrick Schilder, Sjoerd van der Heijden and Alix Dodu

import math, copy, Queue, time, heapq

# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput

version = "v+1+1+1"


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
        self.numMoves = 0

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

    def carsBlockExit(self):
        """
        Return: The number of cars between the red car and the exit. (int) 
        """
        carsBlocking = 0
        
        for x in range(0, self.width-3):
            if self.parkList[x][self.exitpos] == 1:
                for x2 in range(x+2, self.width-1):
                    if self.parkList[x2][self.exitpos] != None:
                        carsBlocking += 1
        return carsBlocking
                
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
                newParking.numMoves +=1

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
                newParking.numMoves +=1

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
                newParking.numMoves +=1

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
                newParking.numMoves +=1

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
        output = '\n'
#        output = ''        

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

#        output += '\n'

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
    boards = function(algorithm=aStarSimulation)
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
           
def breadthFirstSimulation(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x = 0
    y = 0

    length = max(parking.width, parking.height)-1
    exit = parking.getExit()
    exitRow = exit[1]
    exitColumn = exit[0]

    q = Queue.Queue()
    q.put(parking)

    visitedParkings = set()

    search = True

    while search:
        currentParking = q.get()

        if currentParking not in visitedParkings:
            visitedParkings.add(currentParking)

            # Keeps track of the cars that were already tried to be moved.
            visitedCars = set()

            for column in currentParking.getParking():
                # evCar voor "eventual car" ;) 
                for evCar in column:
                    if evCar != None and evCar not in visitedCars:

                        for move in currentParking.moveCarInParking((x,y)):
                            if move.parkList[exitColumn][exitRow] == 1:
                                oplossing = move
                                search = False
                                break

                            q.put(move)

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

def breadthFirstSimulation2(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x = 0
    y = 0

    length = max(parking.width, parking.height)-1
    exit = parking.getExit()
    exitRow = exit[1]
    exitColumn = exit[0]

    q = Queue.Queue()
    q.put(parking)

    visitedParkings = set()
    visitedParkings.add(parking)

    search = True

    while search:
        currentParking = q.get()

        # Keeps track of the cars that were already tried to be moved.
        visitedCars = set()
        print len(visitedParkings)

        for column in currentParking.getParking():
            # evCar voor "eventual car" ;) 
            for evCar in column:
                if evCar != None and evCar not in visitedCars:

                    for move in currentParking.moveCarInParking((x,y)):
                        if move.parkList[exitColumn][exitRow] == 1:
                            oplossing = move
                            search = False
                            break

                        if move not in visitedParkings:
                    
                            visitedParkings.add(move)

                            q.put(move)

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

def aStarSimulation(parking):
    """
    @parking: parking to be solved. (instance of Parking)
    """ 
    # Looks at every tile of parking, to see if there is a car there that
    # can be moved. Starts in the upper left corner, and goes down, first the 
    # first column, then the second..
    
    x = 0
    y = 0

    length = max(parking.width, parking.height)-1
    exit = parking.getExit()
    exitRow = exit[1]
    exitColumn = exit[0]

    h = []
    heapq.heappush(h, (1, parking))

    visitedParkings = set()

    search = True

    while search:
        currentParking = heapq.heappop(h)[1]

        if currentParking not in visitedParkings:
            visitedParkings.add(currentParking)

            # Keeps track of the cars that were already tried to be moved.
            visitedCars = set()

            for column in currentParking.getParking():
                # Checks for every tile if a car is parked there. 
                # evCar stands for "eventual car"
                for evCar in column:
                    if evCar != None and evCar not in visitedCars and search:

                        for move in currentParking.moveCarInParking((x,y)):
                            if move.parkList[exitColumn][exitRow] == 1:
                                oplossing = move
                                search = False
                                break
                        
                            heuristic = move.numMoves

                            carsInTheWay = set()
                            exitSearch = True
                            exitx = exitColumn-1

                            while exitSearch:
                                carNum = move.parkList[exitx][exitRow]
                                carsInTheWay.add(carNum)

                                if carNum == 1:
                                    exitSearch = False
                                    break

                                elif carNum != None:

                                    #### LEVEL 1  ####
                                    heuristic += 1


                                    #### LEVEL 2  ####
                                    # # Checks wether there are cars(2) in the way of the car(1) between RedCar and exit.
                                    # # Adds a penalty for every car(2).
                                    belowInTheWay = 0
                                    aboveInTheWay = 0
                                    carNumLength = cars[carNum].length


                                    # for y2 in range(exitRow - carNumLength, exitRow + carNumLength +1):

                                    #     evCar2 = move.parkList[exitx][y2]

                                    #     if (evCar2 != None) and (evCar2 != carNum) and (cars[evCar2].horizontal):
                                    #         heuristic += 1

                                    #        # Checks wether there are cars(3) in the way of the car(2) in the way of the car(1) between RedCar and exit.
                                    #        # Adds a penalty for every car(3).
                                    #         car2Length = cars[evCar2].length

                                    #         for x3 in range(exitx-car2Length, exitx):
                                    #             try:
                                    #                 evCar3 = move.parkList[x3][y2]
                                    #                 if (evCar3 != None) and (evCar3 != evCar2) and (not cars[evCar3].isHorizontal()):
                                    #                     heuristic += 1


                                    #                     car3Length = cars[evCar3].getLength()

                                    #                     for y4 in range(y2 - car3Length, y2):
                                    #                         try:
                                    #                             evCar4 = move.parkList[x3][y4]
                                    #                             if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                                 heuristic += 1
                                    #                         except IndexError:
                                    #                             break
 
                                    #                     for y4 in range(y2 + 1, y2 + car3Length + 1):
                                    #                         try:
                                    #                             evCar4 = move.parkList[x3][y4]
                                    #                             if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                                 heuristic += 1
                                    #                         except IndexError:
                                    #                             break
 
 
                                    #             except IndexError:
                                    #                 break
 
                                    #         for x3 in range(exitx +1, exitx + car2Length +1):
                                    #             try:
                                    #                 evCar3 = move.parkList[x3][y2]
                                    #                 if (evCar3 != None) and (evCar3 != evCar2) and (not cars[evCar3].isHorizontal()):
                                    #                     heuristic += 1
 
 
                                    #                     car3Length = cars[evCar3].getLength()
 
                                    #                     for y4 in range(y2 - car3Length, y2):
                                    #                         try:
                                    #                             evCar4 = move.parkList[x3][y4]
                                    #                             if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                                 heuristic += 1
 
                                    #                     # for y4 in range(y2 - car3Length, y2):
                                    #                     #     try:
                                    #                     #         evCar4 = move.parkList[x3][y4]
                                    #                     #         if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                     #             heuristic += 1
                                    #                     #     except IndexError:
                                    #                     #         break
 
                                    #                     # for y4 in range(y2 + 1, y2 + car3Length + 1):
                                    #                     #     try:
                                    #                     #         evCar4 = move.parkList[x3][y4]
                                    #                     #         if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                     #             heuristic += 1
                                    #                     #     except IndexError:
                                    #                     #         break
 
                                                                                                                                    
                                    #                         except IndexError:
                                    #                             break
 
                                    #                     for y4 in range(y2 + 1, y2 + car3Length + 1):
                                    #                         try:
                                    #                             evCar4 = move.parkList[x3][y4]
                                    #                             if (evCar4 != None) and (evCar4 != evCar3) and cars[evCar4].isHorizontal():
                                    #                                 heuristic += 1
                                    #                         except IndexError:
                                    #                             break
 
 
                                    #             except IndexError:
                                    #                 break
 
                                    for y2 in range(exitRow-1,exitRow-carNumLength-1, -1):
                                        evCar2 = move.parkList[exitx][y2]

                                        if (evCar2 != None) and (evCar2 not in carsInTheWay):
                                            aboveInTheWay += 1
                                            carsInTheWay.add(evCar2)

                                    for y2 in range(exitRow+1,exitRow+carNumLength+1):
                                        evCar2 = move.parkList[exitx][y2]

                                        if (evCar2 != None) and (evCar2 not in carsInTheWay):
                                            belowInTheWay += 1
                                            carsInTheWay.add(evCar2)

                                    
                                    heuristic += min(aboveInTheWay, belowInTheWay)
 
                                        # # Checks wether there are cars in the way of the car in the way of the car in the way of the exit.
                                        # for carAndy in carsInTheWay:
                                        #     carInTheWay = cars[carAndy[0]]
                                        #     y3 = carAndy[1]
                                        #     if not carInTheWay.horizontal:
                                        #         continue
                                        #     else:
                                        #         if carInTheWay.length == 2:
                                        #             try:
                                        #                 if (move.parkList[exitx+2][y3] != None) or (move.parkList[exitx+1][y3] != None):
                                        #                     try:
                                        #                         if (move.parkList[exitx-2][y3] != None) or (move.parkList[exitx-1][y3] != None):
                                        #                             heuristic += 1
                                        #                     except IndexError:
                                        #                         heuristic += 1
                                        #             except IndexError:
                                        #                 if (move.parkList[exitx-2][y3] != None) or (move.parkList[exitx-1][y3] != None):
                                        #                     heuristic += 1
                                        #         else:
                                        #             try:
                                        #                 if (move.parkList[exitx+3][y3] != None) or (move.parkList[exitx+2][y3] != None) or (move.parkList[exitx+1][y3] != None):
                                        #                     try:
                                        #                         if (move.parkList[exitx-3][y3] != None) or (move.parkList[exitx-2][y3] != None) or (move.parkList[exitx-1][y3] != None):
                                        #                             heuristic += 1
                                        #                     except IndexError:
                                        #                         heuristic += 1
                                        #             except IndexError:
                                        #                 if (move.parkList[exitx-3][y3] != None) or (move.parkList[exitx-2][y3] != None) or (move.parkList[exitx-1][y3] != None):
                                        #                     heuristic += 1
 
 
 
                                    # Checks if a car stands in the way of the car between RedCar and exit
                                    # if cars[carNum].length == 2:
                                    #     if ((move.parkList[exitx][exitRow+2] != None) or (move.parkList[exitx][exitRow+1]))\
                                    #      and ((move.parkList[exitx][exitRow-2] != None) or (move.parkList[exitx][exitRow-1])):
                                    #         heuristic += 1
 
 
                                    #     # if move.parkList[exitx][exitRow-2] != None:
                                    #     #     if move.parkList[exitx][exitRow+2] != None:
                                    #     #         heuristic += 1
                                    #     #         exitCarCanMove = False
                                    #     #     if move.parkList[exitx][exitRow+1] != None:
                                    #     #         heuristic += 1
                                    #     #         exitCarCanMove = False
                                    #     # if move.parkList[exitx][exitRow-1] != None:
                                    #     #     if move.parkList[exitx][exitRow+2] != None:
                                    #     #         heuristic += 1
                                    #     #         exitCarCanMove = False
                                    #     #     if move.parkList[exitx][exitRow+1] != None:
                                    #     #         heuristic += 1
                                    #     #         exitCarCanMove = False
                                     # else:
                                    #     if ((move.parkList[exitx][exitRow+3] != None) or (move.parkList[exitx][exitRow+2] != None) or (move.parkList[exitx][exitRow+1] != None)) \
                                    #     and ((move.parkList[exitx][exitRow-3] != None) or (move.parkList[exitx][exitRow-2] != None) or (move.parkList[exitx][exitRow-1] != None)):
                                    #         heuristic += 1

                                exitx -=1

                            # Voor bord 5: geeft penalty als de vrachtwagen rechtsonder de weg verspert (en vaststaat)
                            # 
                            # for ycheck in xrange(exitRow-1, exitRow-4, -1):
                            #     if (move.parkList[8][ycheck] != None) and (move.parkList[8][ycheck] != 24):
                            #         heuristic += 1
                        

                            heapq.heappush(h,(heuristic, move))

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
    
def board_1(algorithm = breadthFirstSimulation):
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

    boards = algorithm(parking1)


    # for board in boards:
    #     print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards

def board_2(algorithm = breadthFirstSimulation):
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

    boards = algorithm(parking1)


    # for board in boards:
    #     print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards
        

def board_3(algorithm = breadthFirstSimulation):
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

    boards = algorithm(parking1)


    # for board in boards:
    #     print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


def board_4(algorithm = breadthFirstSimulation):
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

    boards = algorithm(parking1)

 #   for board in boards:
#        print board
#
    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards



def board_5(algorithm = aStarSimulation):
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

    
    boards = algorithm(parking5)

 #   for board in boards:
#        print board
#
    print 'Opgelost in:', len(boards)-1, ' stappen.'
    return boards


def board_6(algorithm = breadthFirstSimulation):
    h = True
    v = False

    exitPos6 = (8,4)
    parking6 = Parking(9,9,exitPos6)

    global cars
    cars = [None]

    cars.append(RedCar(2,h))
    parking6.addCar(cars[-1],(0,4))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(0,0))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(2,0))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(5,1))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(2,2))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(7,2))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(4,5))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(6,5))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(2,6))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(2,7))

    cars.append(Car(2,h))
    parking6.addCar(cars[-1],(5,7))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(4,0))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(7,0))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(0,1))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(4,2))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(5,2))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(2,3))

    cars.append(Car(2,v))
    parking6.addCar(cars[-1],(1,5))    

    cars.append(Car(3,h))
    parking6.addCar(cars[-1],(5,6))

    cars.append(Car(3,h))
    parking6.addCar(cars[-1],(1,1))

    cars.append(Car(3,h))
    parking6.addCar(cars[-1],(6,3))

    cars.append(Car(3,h))
    parking6.addCar(cars[-1],(1,8))

    cars.append(Car(3,v))
    parking6.addCar(cars[-1],(0,6))

    cars.append(Car(3,v))
    parking6.addCar(cars[-1],(4,6))

    cars.append(Car(3,v))
    parking6.addCar(cars[-1],(8,5))

    cars.append(Car(3,v))
    parking6.addCar(cars[-1],(3,3))

    
    boards = algorithm(parking6)

 #   for board in boards:
#        print board
#
    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


def board_7(algorithm = breadthFirstSimulation):
    h = True
    v = False

    exitPos7 = (11,5)
    parking7 = Parking(12,12,exitPos7)
    
    global cars
    cars = [None]

    cars.append(RedCar(2, h))
    parking7.addCar(cars[-1],(2,5))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(10,0))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(3,2))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(7,2))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(7,3))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(9,3))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(10,6))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(4,7))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(10,7))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(0,8))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(8,9))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(1,11))

    cars.append(Car(2,h))
    parking7.addCar(cars[-1],(7,11))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(7,0))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(0,2))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(2,4))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(7,4))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(0,6))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(0,7))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(3,8))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(7,8))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(3,9))

    cars.append(Car(3,h))
    parking7.addCar(cars[-1],(3,11))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(0,0))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(2,9))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(3,6))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(4,5))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(5,1))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(5,3))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(5,5))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(6,0))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(7,6))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(9,6))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(9,10))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(10,1))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(11,1))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(11,8))

    cars.append(Car(2,v))
    parking7.addCar(cars[-1],(11,10))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(0,3))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(1,3))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(6,2))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(6,6))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(6,9))

    cars.append(Car(3,v))
    parking7.addCar(cars[-1],(10,9))

    boards = algorithm(parking7)

    # for board in boards:
    #     print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


def testMoveCarInParking(algorithm = breadthFirstSimulation):             
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    global cars
    cars = [None]

    cars.append(RedCar(2,True))
    parking1.addCar(cars[-1], (0,2))

    cars.append(Car(2,False))
    parking1.addCar(cars[-1], (3,2))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1], (3,1))

    cars.append(Car(2,True))
    parking1.addCar(cars[-1], (3,4))

        
    boards = algorithm(parking1)

    # for board in boards:
    #     print board

    print 'Opgelost in:', len(boards)-1, ' stappen.'

    return boards


def testMoveCarInParking2(algorithm = breadthFirstSimulation):             
    exitPos1 = (5,2)
    parking1 = Parking(6,6,exitPos1)
    global cars
    cars = [None]

    cars.append(RedCar(2,True))
    parking1.addCar(cars[-1], (0,2))

    cars.append(Car(3,False))
    parking1.addCar(cars[-1], (3,3))

    cars.append(Car(3,True))
    parking1.addCar(cars[-1], (3,0)) 

    cars.append(Car(2,True))
    parking1.addCar(cars[-1], (0,0))  

    # cars.append(Car(2,False))
    # parking1.addCar(cars[-1], (3,0))

    # cars.append(Car(2,True))
    # parking1.addCar(cars[-1], (3,4))

        
    boards = algorithm(parking1)

    # for board in boards:
    #     print board

    return boards


if __name__ == '__main__':

#    saveResults(board_5, "board_5")



    ##------------------------------------------

    # board_3()
    # testMoveCarInParking()

    ##------------------------------------------


    # horizontaltime = 0
    # verticaltime = 0
    # getpostime = 0

    starttot = time.time()
    boards = board_6(algorithm=aStarSimulation)
    stoptot = time.time()

    print "total time: ", stoptot-starttot
    # print "horizontal: ", horizontaltime
    # print "vertical: ", verticaltime
    # print "getpos: ", getpostime

    ##------------------------------------------

    # with PyCallGraph(output=GraphvizOutput()):
    #     board_3()


