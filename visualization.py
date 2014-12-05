# visualization.py

import Tkinter as tk
import Rush_Hour_BF as rh
#voor testsimulatie gebruik rh.testMoveCarInParking()
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
        command=self.buttonStepBack)
        prevStep.grid(row = 1, column = 0)
        
        nextStep = tk.Button(buttonframe, text=">>",command=self.buttonStep)
        nextStep.grid(row = 1, column = 2)
        
        run = tk.Button(buttonframe, text="Run", command=self.run)
        run.grid(row = 1, column = 1)
        
        stopRun = tk.Button(buttonframe, text="Pause", command=self.stopRun)
        stopRun.grid(row = 2, column = 1)
        
        self.stepdisplay = tk.StringVar()
        stepDisplayLabel = tk.Label(buttonframe,\
        textvariable=self.stepdisplay)
        
        self.stepdisplay.set(str(self.step)+'/'+str(len(self.steplist)-1))
        stepDisplayLabel.grid(row = 2, column = 5, sticky = 'E')
        
        self.goto = tk.StringVar()
        gotoEntry = tk.Entry(buttonframe, textvariable=self.goto, width = 4)
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
                    
                    if childParking[row][column] != None and not pfound and\
                        parentParking[row][column] == None and not cfound:
                        cfound = True
                        car = childParking[row][column]
                        newcoord = [row,column]
                        
                    elif childParking[row][column]==None and not cfound and\
                        parentParking[row][column] != None and not pfound:
                        pfound = True
                        car = parentParking[row][column]
                        oldcoord = [row,column]
                        
                    elif cfound and parentParking[row][column] != None:
                        if car == parentParking[row][column]:
                            oldcoord = [row,column]
                            stop = True
                            break
                            
                    elif pfound and childParking[row][column] != None:
                        if car == childParking[row][column]:
                            newcoord = [row,column]
                            stop = True
                            break
                        
            steplist.append([car, oldcoord, newcoord])
            
            child = parent
            parent = child.getParent()
            
        self.steplist = steplist[::-1]
        self.steplist += [[1,[0,0],[1,0]]]
        self.beginParking = child            
            
    def drawBeginParking(self):
        '''
        Uses the parking instance 'beginParking', the initial parking of the
        puzzle, draws a grid of the appropriate size and places the cars as
        indicated. The red car is coloured red, the others are blue.
        
        takes and returns nothing, but draws the visualization.
        '''
        parkingInst = self.beginParking
        
        size = len(parkingInst.getParking())*50+1
        
        self.canvas = tk.Canvas(self.canvasframe, width = size,\
            height = size, bg="white")
        for x in xrange(2, size +2 ,50):
            for y in xrange(2, size +2 ,50):
                self.canvas.create_line(y, 1, y, size+2)
                self.canvas.create_line(2, x, size+2, x)
        
        parking = parkingInst.getParking()
        
        placedcars = set()        
        for row in xrange(len(parking)):
            for column in xrange(len(parking[0])):
                
                car = parking[row][column]
                if car in placedcars:
                    continue   
                
                try:
                    # generates error if not a car on position (column, row).
                    carInst = parkingInst.occupiedBy((row,column))
                    coords = carInst.getPos((row,column))
                    placedcars.add(car)
                    
                except:
                    continue
                
                if car == 1:
                    self.canvas.create_rectangle(coords[0][0]*50+5,\
                    coords[0][1]*50+5, coords[-1][0]*50+49,\
                    coords[-1][1]*50+49, fill = 'red',\
                    tag = 'car'+str(car))
                else:
                    self.canvas.create_rectangle(coords[0][0]*50+5,\
                    coords[0][1]*50+5, coords[-1][0]*50+49,\
                    coords[-1][1]*50+49, fill = 'blue',\
                    tag = 'car'+str(car))
                
        self.canvas.grid(row = 0)#, columnspan = 2)
        
    def stopRun(self):
        '''
        Stops the 'run' command
        '''
        self.stop = True
        
    def run(self):
        '''
        Animates all steps towards solving the puzzle, or up until the 'stop'
        or 'goto' button is pressed.
        '''
        self.stop = False
        while not self.stop:
            self.oneStep()
            time.sleep(self.delay*5)
            
    def gotoStep(self):
        '''
        Rapidly follows the moves to the step specified in the entry window.
        '''
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
    
    def buttonStep(self):
        self.stop = True
        self.oneStep()
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
            for interval in xrange(10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0]), dx*5, 0)
                self.canvas.update()
        elif dy != 0:
            for interval in xrange(10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0]), 0, dy*5)
                self.canvas.update()
                
    def buttonStepBack(self):
        self.stop = True
        self.oneStepBack()
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
            for interval in xrange(10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0]), dx*5, 0)
                self.canvas.update()
        elif dy != 0:
            for interval in xrange(10):
                time.sleep(self.delay)
                self.canvas.move('car'+str(move[0]), 0, dy*5)
                self.canvas.update()


def runApp(parking):
    root = tk.Tk()
    
    app = App(root,parking)
    
    root.mainloop()
    root.destroy()


runApp(rh.board_1()[-1])
