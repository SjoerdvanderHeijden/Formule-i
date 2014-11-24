# visualization.py

import Tkinter as tk
#import Rush_Hour_BF as rh
import testsimulatie as tst
import time

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
        self.delay = .03

        quitbutton = tk.Button(
            buttonframe, text="QUIT", fg="red", command=buttonframe.quit
            )
        quitbutton.grid(row = 2, column = 0)

        prevStep = tk.Button(buttonframe, text="<<",\
            command=self.oneStepBack)
        prevStep.grid(row = 1, column = 0)
        
        nextStep = tk.Button(buttonframe, text=">>",\
            command=self.oneStep)
        nextStep.grid(row = 1, column = 2)
        
        run = tk.Button(buttonframe, text="Run",\
            command=self.run)
        run.grid(row = 1, column = 1)
        
#        self.stop = tk.IntVar()
        stopRun = tk.Button(buttonframe, text="Pause",\
            command=self.stopRun)
        stopRun.grid(row = 2, column = 1)
        
        self.stepdisplay = tk.StringVar()
        stepDisplayLabel = tk.Label(buttonframe, textvariable=self.stepdisplay)
        self.stepdisplay.set(str(self.step)+'/'+str(len(self.steplist)))
        stepDisplayLabel.grid(row = 2, column = 5, sticky = 'E')
        
        self.goto = tk.StringVar()
        gotoEntry = tk.Entry(buttonframe, textvariable = self.goto, width = 4)
        gotoEntry.grid(row = 2, column = 3)
        gotoButton = tk.Button(buttonframe, text = 'Go to step',\
            command = self.gotoStep)
        gotoButton.grid(row = 2, column = 4)

    
    def createStepList(self, child):
        '''
        Generates a list containing all steps done to complete the puzzle in
        the form [car x, coordinates before move, coordinates after move], from
        start to end. Also finds and denotes the initial Parking instance.
        
        takes the final Parking instance of the Rush Hour puzzle
        
        returns: nothing, but saves its creations as instance attributes.
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
        
        takes and returns nothing, but draws the visualization.
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
        
    def run(self):
        '''
        Animates all steps towards solving the puzzle, or up until 
        '''
        self.stop = False
        while not self.stop:
            self.oneStep()
            time.sleep(self.delay*5)
            
    def gotoStep(self):
        self.stop = True
        self.delay = 0
        diff = int(self.goto.get())-self.step
        if diff > 0:
            for i in xrange(diff):
                self.oneStep()
        elif diff < 0:
            for i in xrange(-diff):
                self.oneStepBack()
        self.delay = .03
            
    def oneStep(self):
        '''
        Animates a single step taken to solve the Rush Hour puzzle. The current
        step is remembered in self.step.
        
        returns nothing, but updates the app.
        '''
        try:
            move = self.steplist[self.step]
        except:
            self.stop = True
            return
        
        self.step+=1
        self.stepdisplay.set(str(self.step)+'/'+str(len(self.steplist)))        
        
        dx = move[2][0]-move[1][0]
        dy = move[2][1]-move[1][1]
        
        if dx != 0:
            for interval in xrange(dx*10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0].getName()), dx*5, 0)
                self.canvas.update()
        elif dy != 0:
            for interval in xrange(dy*10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0].getName()), 0, dy*5)
                self.canvas.update()


    def oneStepBack(self):
        '''
        Animates a single step back 'towards' solving the Rush Hour puzzle.
        The current step is remembered in self.step.
        
        returns nothing, but updates the app.
        '''
        if self.step == 0:
            self.stop = True
            return
            
        self.step-=1
        self.stepdisplay.set(str(self.step)+'/'+str(len(self.steplist)))
        
        move = self.steplist[self.step]
        
        dx = move[1][0]-move[2][0]
        dy = move[1][1]-move[2][1]
        
        if dx != 0:
            for interval in xrange(0,dx*10,-1):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0].getName()), dx*5, 0)
                self.canvas.update()
        elif dy != 0:
            for interval in xrange(0,dy*10,-1):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0].getName()), 0, dy*5)
                self.canvas.update()


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
