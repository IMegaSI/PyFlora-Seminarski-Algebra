from tkinter import StringVar, BooleanVar, IntVar

class TkPlant:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.description = StringVar()
        self.zalijevanje = StringVar()
        self.osvjetljenje = StringVar()
        self.toplina = StringVar()
        self.dohrana = BooleanVar()
        self.opcija = IntVar()