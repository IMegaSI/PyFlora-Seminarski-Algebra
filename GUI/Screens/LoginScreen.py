from tkinter import Frame, Tk, ttk
import tkinter as tk
from PIL import Image, ImageTk
from service.UserService import UserService
from service.PlantService import PlantService
from datasource.dto.UserDTO import UserDTO
from datasource.tk.TkUser import TkUser
from GUI.Screens.PlantsAndPotsScreen import PlantsAndPotsScreen

class LoginScreen(Frame):


    def __init__(self, mainwindow, userService, tkmodel, plantService):
        super().__init__(master=mainwindow)
        self.UserService: UserService = userService
        self.PlantService: PlantService = plantService
        self.grid()
        self.tkModel: TkUser = tkmodel
        self['relief'] = tk.RAISED
        self['borderwidth'] = 5
        self.toggleVisibility = False
        self.prozorZaLogiranje()

    def prozorZaLogiranje(self):
        #Import pictures for hiding and showing password
        imgShow = Image.open("./GUI/img/show.png")
        imgHide = Image.open("./GUI/img/hide.png")

        # Create Login Frame group
        self.loginProzor = ttk.LabelFrame(self, text="Login Window")
        self.loginProzor.grid(row=0, column=0, pady=5, padx=5)


        # creating label and entry for username that is saved to a variable
        self.username_label = ttk.Label(self.loginProzor, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)

        self.username_entry = ttk.Entry(self.loginProzor, textvariable=self.tkModel.user)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # creating label and entry for password that is saved to a variable
        self.password_label = ttk.Label(self.loginProzor, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry = ttk.Entry(self.loginProzor, show="*", textvariable=self.tkModel.password)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # binding enter to login method
        self.password_entry.bind("<Return>", self.newlogin)

        self.tkImgShow = ImageTk.PhotoImage(imgShow)
        self.tkImgHide = ImageTk.PhotoImage(imgHide)
        self.visbitlity_Button = ttk.Button(self.loginProzor, image=self.tkImgHide,
                                            command=self.changeVisibility)
        self.visbitlity_Button.grid(row=1, column=2, padx=5, pady=5)

        login_button = ttk.Button(self.loginProzor, text="Login", command=self.newlogin)
        login_button.grid(row=3, column=1,  padx=5, pady=5, sticky=tk.EW)

        # creating warning
        self.warning_label = ttk.Label(self.loginProzor, textvariable=self.tkModel.warning)
        self.warning_label.grid(row=4, column=1, padx=5, pady=5)

    # method for toggling visibility
    def changeVisibility(self):
        if not self.toggleVisibility:
            self.password_entry.config(show="")
            self.visbitlity_Button.config(image=self.tkImgShow)
            self.toggleVisibility = True
        else:
            self.password_entry.config(show="*")
            self.visbitlity_Button.config(image=self.tkImgHide)
            self.toggleVisibility = False


    def newlogin(self, event=None):
        self.userdto = self.UserService.grabUserfromDB(self.tkModel.user.get(), self.tkModel.password.get())
        #self.tkModel.warning.set(self.tkModel.user.get())
        if self.userdto is not None:
            self.tkModel.name.set(self.userdto.name)
            self.tkModel.lastname.set(self.userdto.lastname)
            self.loginProzor.grid_remove()
            self.menuFrame()
            # napravit neki frame u gornjem desnom kantunu sa ispisom userovin name i lastname?, napravljeno

        else:
            self.tkModel.warning.set("Username ili password ne odgovaraju!")

    def menuFrame(self):


        self.menu_frame = ttk.LabelFrame(self, text="Menu Frame")
        self.menu_frame.grid(row=0, column=0, pady=5, padx=5)

        change_user = ttk.Button(self.menu_frame, text="Edit User", command=self.userChangeFrame)
        change_user.grid(row=0, column=0, padx=20, pady=20, sticky=tk.EW)

        main_menu = ttk.Button(self.menu_frame, text="Main Menu", command=self.createPlantsAndPotsWindow) # dodat komadu koja ce otvorit tabove biljaka i pitara
        main_menu.grid(row=1,column=0,padx=20,pady=20)

    def userChangeFrame(self):

        self.menu_frame.grid_remove()
        self.change_frame = ttk.LabelFrame(self, text="Please enter new info")
        self.change_frame.grid(row=0, column=0, pady=5, padx=5)

        self.user_name_change_label = ttk.Label(self.change_frame, text="New name:")
        self.user_name_change_label.grid(row=0, column=0, padx=5, pady=5)

        self.user_name_change_entry = ttk.Entry(self.change_frame, textvariable=self.tkModel.name)
        self.user_name_change_entry.grid(row=0, column=1, padx=5, pady=5)

        self.user_last_name_change_label = ttk.Label(self.change_frame, text="New lastname")
        self.user_last_name_change_label.grid(row=1, column=0, padx=5, pady=5)

        self.user_last_name_change_entry = ttk.Entry(self.change_frame, textvariable=self.tkModel.lastname)
        self.user_last_name_change_entry.grid(row=1, column=1, padx=5, pady=5)

        self.username_change_label = ttk.Label(self.change_frame, text="New username")
        self.username_change_label.grid(row=2, column=0, padx=5, pady=5)

        self.username_name_change_entry = ttk.Entry(self.change_frame, textvariable=self.tkModel.user)
        self.username_name_change_entry.grid(row=2, column=1, padx=5, pady=5)

        self.user_password_change_label = ttk.Label(self.change_frame, text="New password")
        self.user_password_change_label.grid(row=3, column=0, padx=5, pady=5)

        self.user_password_change_entry = ttk.Entry(self.change_frame, textvariable=self.tkModel.password)
        self.user_password_change_entry.grid(row=3, column=1, padx=5, pady=5)

        # botun spremi promjene i vrati na prethodni frame
        button_save_changes = ttk.Button(self.change_frame, text="Spremi", command=self.PressSpremiButton)
        button_save_changes.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)


    def PressSpremiButton(self):

        changeddto = UserDTO(id=self.userdto.id,
                             name=self.tkModel.name.get(),
                             lastname=self.tkModel.lastname.get(),
                             user=self.tkModel.user.get(),
                             password=self.tkModel.password.get()
                             )
        self.UserService.updateUser(changeddto)
        self.change_frame.grid_remove()
        self.menuFrame()

    def createPlantsAndPotsWindow(self):
        self.menu_frame.grid_remove()
        self.PaP_screen = PlantsAndPotsScreen(self, self.PlantService)
        self.PaP_screen.grid(row=0, column=0, padx=5, pady=5)















