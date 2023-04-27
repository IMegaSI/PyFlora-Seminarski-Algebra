import tkinter as tk
from tkinter import ttk, Frame, Toplevel, messagebox
from PIL import Image, ImageTk
from utils.DBUtils import DBUtils
from service.PlantService import PlantService
import  os
from datasource.tk.TkPlant import TkPlant

class PlantsAndPotsScreen(Frame):

    def __init__(self, mainwindow, plantService):
        super().__init__(master=mainwindow)
        self.grid()
        self.tkModelPlant = TkPlant()
        self.plantService: PlantService = plantService
        self.makeTabs()
        self.populatePlantsTab()
        self.populatePotsTab()
        self.populateEditsTab()



    def makeTabs(self):
        self.plantsAndPotsFrame = ttk.LabelFrame(self, text="Plants and Pots")
        self.plantsAndPotsFrame.grid(row=0, column=0, pady=5, padx=5)

        self.tabs = ttk.Notebook(self.plantsAndPotsFrame)
        self.tabs.grid(row=0, column=0, pady=5, padx=5)

        self.tabPlants = ttk.Frame(self.tabs)
        self.tabPots = ttk.Frame(self.tabs)
        self.tabEdits = ttk.Frame(self.tabs)

        self.tabs.add(self.tabPlants, text="--PLANTS--")
        self.tabs.add(self.tabPots, text="-- POTS --")
        self.tabs.add(self.tabEdits, text="--EDITS--")



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

    """Plant details tab"""

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

    """Pots details tab"""

    def populatePotsTab(self):
        lblInstructions = ttk.Label(self.tabPots, text="Dvoklikom na ime posadite biljku")
        lblInstructions.pack()

        self.plantsList = tk.Listbox(self.tabPots, width=20, height=12, selectmode=tk.SINGLE)
        self.plantsList.pack(anchor=tk.NW,  expand=True)
        self.plantsList.bind('<Double-Button-1>', self.plantingThePlantInPot)

        self.plantsInList = self.plantService.getAllPlants()
        for plant in self.plantsInList:
            self.plantsList.insert("end", plant.name)



    def plantingThePlantInPot(self, event):
        plantedPlantName = self.plantsList.get(self.plantsList.curselection())
        self.plantedPlantDTO = self.plantService.getPlantByName(plantedPlantName)
        print(self.plantedPlantDTO)


        self.potFrame = ttk.Labelframe(self.tabPots, text=plantedPlantName)
        self.potFrame.pack(side=tk.LEFT, expand=True)

        # Load the plant image using PIL and create a Tkinter PhotoImage object
        plant_image = Image.open(self.plantedPlantDTO.photo)
        plant_image = plant_image.resize((200, 200))
        plant_photo = ImageTk.PhotoImage(plant_image)

        # Create a label to display the plant image
        self.imgPlanted = ttk.Label(self.potFrame, image=plant_photo)
        self.imgPlanted.image = plant_photo
        self.imgPlanted.pack(anchor=tk.NE, expand=True)

        # labels for simulated info
        self.lblSoilMoisture = ttk.Label(self.potFrame, text="Vlažnost zemlje:")
        self.lblSoilMoisture.pack()
        self.lvlSoilMoistureValue = ttk.Label(self.potFrame, text="33%")    # Ubacit simuliranu vrijednost kroz textvariable
        self.lvlSoilMoistureValue.pack()

        self.lblSoilPh = ttk.Label(self.potFrame, text="PH vrijednost zemlje:")
        self.lblSoilPh.pack()
        self.lblSoilPhValue = ttk.Label(self.potFrame, text="4.4")  # Ubacit simuliranu vrijednost kroz textvariable
        self.lblSoilPhValue.pack()

        self.lblLight = ttk.Label(self.potFrame, text="Količina svijetla")
        self.lblLight.pack()
        self.lblLightValue = ttk.Label(self.potFrame, text="Umjereno")  # Ubacit simuliranu vrijednost kroz textvariable
        self.lblLightValue.pack()

        self.lblAirTemp = ttk.Label(self.potFrame, text="Temperatura zraka")
        self.lblAirTemp.pack()
        self.lblAirTempValue = ttk.Label(self.potFrame, text="28")   # Ubacit simuliranu vrijednost kroz textvariable
        self.lblAirTempValue.pack()

    """Edits tab"""

    def populateEditsTab(self):
        lblInstructions = ttk.Label(self.tabEdits, text="Izmjena, brisanje i dodavanje novih biljaka")
        lblInstructions.pack()

        self.plantsListEditing = tk.Listbox(self.tabEdits, width=20, height=12, selectmode=tk.SINGLE)
        self.plantsListEditing.pack(anchor=tk.NW, expand=True)
        self.plantsListEditing.bind('<<ListboxSelect>>', self.editngPlants)

        self.plantsEditing = self.plantService.getAllPlants()
        for plant in self.plantsEditing:
            self.plantsListEditing.insert("end", plant.name)


    def editngPlants(self, event):
        editedPlantName = self.plantsListEditing.get(self.plantsListEditing.curselection())
        self.editedPlantDTO = self.plantService.getPlantByName(editedPlantName)
        if self.editedPlantDTO is not None:
            self.tkModelPlant.name.set(self.editedPlantDTO.name)
            self.tkModelPlant.description.set((self.editedPlantDTO.description))
            self.tkModelPlant.zalijevanje.set(self.editedPlantDTO.zalijevanje)
            self.tkModelPlant.osvjetljenje.set(self.editedPlantDTO.osvjetljenje)
            self.tkModelPlant.toplina.set(self.editedPlantDTO.toplina)
        print(self.editedPlantDTO)

        editingWindow = tk.Toplevel(self.master)
        editingWindow.title(f"Editing Plant")
        editingWindow.geometry("800x1000")

        lblPlantName = ttk.Label(editingWindow, text="Ime biljke:")
        lblPlantName.grid(row=0, column=0)

        entryPlantName = ttk.Entry(editingWindow, textvariable=self.tkModelPlant.name)
        entryPlantName.grid(row=0, column=1)

        lblDescription = ttk.Label(editingWindow, text="Description:")
        lblDescription.grid(row=0, column=2)

        textPlantDescription = tk.Text(editingWindow, width=60)
        textPlantDescription.grid(row=1, column=2)
        textPlantDescription.insert("1.0", self.tkModelPlant.description.get())





















