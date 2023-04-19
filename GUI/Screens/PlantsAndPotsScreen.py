import tkinter as tk
from tkinter import ttk, Frame, Toplevel, messagebox
from PIL import Image, ImageTk
from utils.DBUtils import DBUtils
from service.PlantService import PlantService
import  os

class PlantsAndPotsScreen(Frame):

    def __init__(self, mainwindow, plantService):
        super().__init__(master=mainwindow)
        self.grid()
        self.plantService: PlantService = plantService
        self.makeTabs()
        self.populatePlantsTab()
        self.populatePotsTab()




    def makeTabs(self):
        self.plantsAndPotsFrame = ttk.LabelFrame(self, text="Plants and Pots")
        self.plantsAndPotsFrame.grid(row=0, column=0, pady=5, padx=5)

        self.tabs = ttk.Notebook(self.plantsAndPotsFrame)
        self.tabs.grid(row=0, column=0, pady=5, padx=5)

        self.tabPlants = ttk.Frame(self.tabs)
        self.tabPots = ttk.Frame(self.tabs)

        self.tabs.add(self.tabPlants, text="Plants")
        self.tabs.add(self.tabPots, text="Pots")

    def populatePlantsTab(self):
        plants = self.plantService.getAllPlants()

        row_num = 0
        col_num = 0

        for i, plant in enumerate(plants):
            # Create a label for the plant name
            plant_name_label = ttk.Label(self.tabPlants, text=plant.name)
            plant_name_label.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="w")

            # Load the plant image using PIL and create a Tkinter PhotoImage object
            plant_image = Image.open(plant.photo)
            plant_image = plant_image.resize((100, 100))
            plant_photo = ImageTk.PhotoImage(plant_image)

            # Create a label to display the plant image
            plant_image_label = ttk.Label(self.tabPlants, image=plant_photo)
            plant_image_label.image = plant_photo
            plant_image_label.grid(row=row_num, column=col_num + 1, padx=10, pady=10)
            plant_image_label.bind("<Button-1>", lambda event, index=plant.id: self.showPlantDetails(index))

            # Increment the column number
            col_num += 2

            # If we've reached the end of a row, reset the column number and increment the row number
            if col_num == 8:
                col_num = 0
                row_num += 1

    def showPlantDetails(self, plant_id):
        print(f"Plant ID: {plant_id}")
        plant = self.plantService.getPlantById(plant_id)


        if plant is None:
            messagebox.showerror('Error', 'Plant not found')
            return

        # Create a new Toplevel window to display the plant details
        plant_window = Toplevel(self.master)
        plant_window.title(plant.name)

        # Create a label to display the plant name
        plant_name_label = ttk.Label(plant_window, text=plant.name)
        plant_name_label.pack(pady=10)

        # Load the plant image using PIL and create a Tkinter PhotoImage object
        plant_image = Image.open(plant.photo)
        plant_image = plant_image.resize((200, 200))
        plant_photo = ImageTk.PhotoImage(plant_image)

        # Create a label to display the plant image
        plant_image_label = ttk.Label(plant_window, image=plant_photo)
        plant_image_label.image = plant_photo
        plant_image_label.pack(pady=10)

        # Create a label to display the plant description
        plant_desc_label = ttk.Label(plant_window, text=plant.description)
        plant_desc_label.pack(pady=10)

        # Create a button to close the window
        close_button = ttk.Button(plant_window, text="Close", command=plant_window.destroy)
        close_button.pack(pady=10)

    def populatePotsTab(self):
        self.plantsList = tk.Listbox(self.tabPots, width=20, selectmode=tk.SINGLE)
        self.plantsList.grid(pady=5, padx=5, row=0, column=0)

        self.plantsInList = self.plantService.getAllPlants()
        for plant in self.plantsInList:
            self.plantsList.insert("end", plant.name)



        """napravit funkciju koja ce posadit biljku"""
         # možda prebacit na kraj funkcije

    def PlantingThePlantInPot(self, event):

        self.potFrame = ttk.Labelframe(self.tabPots, text=f"{self.plantsList.get(self.plantsList.curselection())}")

        self.plantsList.bind('<<ListboxSelect>>', self.PlantingThePlantInPot)











