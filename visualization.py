# visualization.py

import Tkinter as tk
#import Rush_Hour_BF as rh
import testsimulatie as tst

class App:

    def __init__(self, master, parking):
        '''
        Initializes the Tkinter application, places button widgets, calls
        a function for drawing and placing the initial Rush Hour parking in the
        app and calls a function that generates several handy instance
        attributes.
        
        takes the final, solved Parking instance of the puzzle.
        '''
                
        buttonframe = tk.Frame(master)
        buttonframe.grid(row = 2)
        
        self.canvasframe = tk.Frame(master)
        self.canvasframe.grid(row = 0)
        
        self.step = 0
        self.createStepList(parking)
        self.drawBeginParking()


        self.quit = tk.Button(
            buttonframe, text="QUIT", fg="red", command=buttonframe.quit
            )
        self.quit.grid(row = 2, column = 0)

        self.prevStep = tk.Button(buttonframe, text="<<",\
            command=self.oneStepBack)
        self.prevStep.grid(row = 1, column = 0)
        
        self.nextStep = tk.Button(buttonframe, text=">>",\
            command=self.oneStep)
        self.nextStep.grid(row = 1, column = 2)
        
        self.run = tk.Button(buttonframe, text="Run",\
            command=self.oneStep)
        self.run.grid(row = 1, column = 1)
        
        self.stopRun = tk.Button(buttonframe, text="Pause",\
            command=self.stopRun)
        self.stopRun.grid(row = 2, column = 1)
        
    
    def createStepList(self, child):
        '''
        Generates a list containing all steps done to complete the puzzle in
        the form [car x, coordinates before move, coordinates after move], from
        start to end. Also finds and denotes the initial Parking instance.
        
        takes the final Parking instance of the Rush Hour puzzle
        
        returns: nothing, but makes its creations into instance attribute.
        '''
        parent = child.getParent()
        steplist = []
        
        while parent != None:
            
            childParking = child.getParking()
            parentParking = parent.getParking()
            
            stop = False
            cfound = False
            pfound = False
            for row in xrange(len(childParking)):
                if stop:
                    break
                for column in xrange(len(childParking[0])):
                    if childParking[row][column] != None and\
                        parentParking[row][column] == None and not cfound:
                        cfound = True
                        car = childParking[row][column]
                        newcoord = [row,column]
                        
                    elif childParking[row][column] == None and\
                        parentParking[row][column] != None and not pfound:
                        pfound = True
                        car = parentParking[row][column]
                        oldcoord = [row,column]
                        
                    elif cfound and parentParking[row][column] != None:
                        if car.getName()==parentParking[row][column].getName():
                            oldcoord = [row,column]
                            stop = True
                            break
                            
                    elif pfound and childParking[row][column] != None:
                        if car.getName()==childParking[row][column].getName():
                            newcoord = [row,column]
                            stop = True
                            break

            steplist.append([car, oldcoord, newcoord])
            
            child = parent
            parent = child.getParent()
        self.steplist = steplist[::-1]
        self.beginParking = child
            
            
    def drawBeginParking(self):
        '''
        Uses the parking instance 'beginParking', the initial parking of the
        puzzle, draws a grid of the appropriate size and places the cars as
        indicated. The red car is coloured red, the others are blue.
        
        takes and returns nothing.
        '''
        
        beginParking = self.beginParking
        
        size = len(beginParking.getParking())*50+1
        
        self.canvas = tk.Canvas(self.canvasframe, width = size, height = size\
            , bg="white")
        for x in xrange(2, size +2 ,50):
            for y in xrange(2, size +2 ,50):
                self.canvas.create_line(y, 1, y, size+2)
                self.canvas.create_line(2, x, size+2, x)
        
        beginParking = beginParking.getParking()
        
        placedcars = set()        
        for row in xrange(len(beginParking)):
            for column in xrange(len(beginParking[0])):
                
                car = beginParking[row][column]
                if car in placedcars:
                    continue   
                
                try:
                    # generates error if not a car on position (column, row).
                    coords = car.getPos((row,column))
                    placedcars.add(car)
                except:
                    continue
                
                if isinstance(car, tst.RedCar):
                    self.canvas.create_rectangle(coords[0][0]*50+5,\
                    coords[0][1]*50+5, coords[-1][0]*50+49,\
                    coords[-1][1]*50+49, fill = 'red', tag = 'car'+str(car.getName()))
                else:
                    self.canvas.create_rectangle(coords[0][0]*50+5,\
                    coords[0][1]*50+5, coords[-1][0]*50+49,\
                    coords[-1][1]*50+49, fill = 'blue', tag = 'car'+str(car.getName()))
                
        self.canvas.grid(row = 0)#, columnspan = 2)
        
    def stopRun(self):
        self.stop = True
                
    def oneStep(self, speed = 5, backward = False, gotostep = False, run = False):
        '''
        TODO
        
        Animates a single step taken to solve the Rush Hour puzzle. The current
        step is remembered in self.step.
        
        takes:
        speed, defines how fast the cars are moved in the grid
        gotostep, allows to jump to a specified step.
        backward, allows to go back steps instead of forwards.
        run, allows to autorun to the solution
        
        returns nothing, but updates the app.
        '''
        move = self.steplist[self.step]

        try:
            self.canvas.move('car'+str(move[0].getName()),\
            (move[2][0]-move[1][0])*50, (move[2][1]-move[1][1])*50)
        except:
            print 'already solved!'
        self.step+=1

        self.canvas.update()
#        if run:
#            if self.stop:(move[2][0]-move[1][0])*
#                pass (move[2][1]-move[1][1])*
#            else:
#                self.oneStep(speed, run = True)
    def oneStepBack(self):
        move = self.steplist[self.step-1]
        try:
            self.canvas.move('car'+str(move[0].getName()),\
            (move[2][0]-move[1][0])*-50, (move[2][1]-move[1][1])*-50)
        except:
            print 'already at start!'
        self.step-=1
    
root = tk.Tk()

def testParking():             
    audi = tst.RedCar(2,True)
    seat = tst.Car(2,False)
    exitPos1 = (5,2)
    parking1 = tst.Parking(6,6,exitPos1)
    parking1.addCar(audi, (0,2))
    parking1.addCar(seat, (3,2))
    return tst.BreadthFirstSimulation(parking1)

app = App(root, testParking()[-1])

root.mainloop()
root.destroy()
