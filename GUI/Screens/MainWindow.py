import tkinter as tk
from tkinter import ttk, Tk
from GUI.Screens.LoginScreen import LoginScreen
from datasource.tk.TkUser import TkUser



class MainWindow(Tk):

    def __init__(self, userService, plantService):
        super().__init__()
        self.title("PyFlora Posuda App")
        self.geometry("1000x800")
        self.UserService = userService
        self.plantService = plantService
        self.tkglavni = TkUser()
        self.createLoginWindow()
        self.config(background="gray")
        self.userInfoDisplay()


    def createLoginWindow(self):
        login_screen = LoginScreen(self, self.UserService, self.tkglavni, self.plantService)
        login_screen.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def userInfoDisplay(self):

        self.userInfo = ttk.Labelframe(self, text="USER")
        self.userInfo.place(relx=1, rely=0, anchor=tk.NE)


        self.username = ttk.Label(self.userInfo, textvariable=self.tkglavni.name)
        self.username.grid(row=0, column=0, pady=5, padx=5)

        self.userLastname = ttk.Label(self.userInfo, textvariable=self.tkglavni.lastname)
        self.userLastname.grid(row=1, column=0, pady=5, padx=5)


