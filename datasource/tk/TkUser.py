from tkinter import StringVar

class TkUser:

    def __init__(self):
        self.id = None
        self.name = StringVar()
        self.lastname = StringVar()
        self.user = StringVar()
        self.password = StringVar()
        self.warning = StringVar()