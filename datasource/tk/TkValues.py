from tkinter import StringVar, IntVar
import random

class TkValues:

    def __init__(self):
        self.soilMoisture = IntVar()
        self.soilPh = IntVar()
        self.light = StringVar()
        self.airTemp = IntVar()


    def simulateNumbers(self):
        mylist = ["Sjenovito", "Jarko"]
        self.soilPh.set(random.randrange(5, 8))
        self.soilMoisture.set(random.randrange(20, 100))
        self.airTemp.set(random.randrange(10, 30))
        self.light.set(random.choice(mylist))