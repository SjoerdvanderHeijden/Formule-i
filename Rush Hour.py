# Rush Hour.py

class Car(object):
    """
    (vracht)auto
    input: poslist = lijst met coordinaten van voertuig (variabele lengte),
                     elke coordinaat opgeslagen als tuple.
    """
    def __init__(self, poslist):
        self.poslist = poslist

        # uirekenen van richting
        if poslist[0][0] == poslist[1][0]:
            self.richting = 'h'
        elif poslist[0][1] == poslist[1][1]:
            self.richting = 'v'
        else:
            raise ValueError("Ongeldige coordinaten")

    def getPos(self):
        return self.poslist

    def getDirection(self):
        return self.richting

    def getLength(self):
        return len(self.poslist)

    def moveCar(self, distance):
        crd = self.poslist
        
        if self.richting == 'h':
            for i in xrange(len(crd)):
                # x-coordinaten worden aangepast
                crd[i] = (crd[i][0] + distance, crd[i][1])
        else:
            for i in xrange(len(crd)):
                # x-coordinaten worden aangepast
                crd[i] = (crd[i][0], crd[i][1] + distance)
                
        self.poslist = crd

    def isAt(self, pos):
        # @pos: type: tuple
        return pos in self.poslist

class RedCar(Car):
    #het lijkt me het handigst als simulatie checkt of RedCar bij de uitgang is.
    pass

class Parking(object):
    def __init__(self, width, height, carlist):
        # werk rustig verder hieraan als je wilt, ik ben gestopt (voorlopig :p)
        pass

def runSimulation():
    pass
