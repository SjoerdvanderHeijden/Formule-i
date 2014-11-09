import Tkinter as tk

class App:

    def __init__(self, master):

        buttonframe = tk.Frame(master)
        buttonframe.grid(row = 2)
        
        canvasframe = tk.Frame(master)
        canvasframe.grid(row = 0)

        self.button = tk.Button(
            buttonframe, text="QUIT", fg="red", command=buttonframe.quit
            )
        self.button.grid(row = 2)

        self.hi_there = tk.Button(buttonframe, text="Hello", command=self.say_hi)
        self.hi_there.grid(row = 2, column = 1)
        
        self.canvas = tk.Canvas(canvasframe, width = 501, height = 501, bg="white")
        for x in xrange(2,503,50):
            for y in xrange(2,503,50):
                self.canvas.create_line(y, 1, y, 504)
                self.canvas.create_line(2, x, 503, x)

        self.canvas.grid(row = 0)#, columnspan = 2)
        
    def say_hi(self):
        print "hi there, everyone!"
    
    def visualize(self, parkings):
        for parking in parkings:
            for y in xrange(len(parking)):
                for x in xrange(len(y)):
                    if parking[y][x] != None:
                        if isinstance(parking[y][x], RedCar):
                            
                        else:
                            
    
root = tk.Tk()

app = App(root)

root.mainloop()
root.destroy()
