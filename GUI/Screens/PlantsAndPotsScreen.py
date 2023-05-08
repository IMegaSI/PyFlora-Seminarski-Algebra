import tkinter as tk
from tkinter import ttk, Frame, Toplevel, messagebox
from PIL import Image, ImageTk
from service.PlantService import PlantService
from datasource.tk.TkPlant import TkPlant
from datasource.dto.PlantDTO import PlantDTO
import random
from datasource.tk.TkValues import TkValues

class PlantsAndPotsScreen(Frame):

    def __init__(self, mainwindow, plantService):
        super().__init__(master=mainwindow)
        self.grid()
        self.tkModelPlant = TkPlant()
        self.plantService: PlantService = plantService
        self.makeTabs()
        self.simNumbers = TkValues()
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
        self.plantsList.pack(anchor=tk.NW,  expand=True, side=tk.LEFT)
        self.plantsList.bind('<Double-Button-1>', self.plantingThePlantInPot)

        self.plantsInList = self.plantService.getAllPlants()
        for plant in self.plantsInList:
            self.plantsList.insert("end", plant.name)

        self.btnGetnumbers = ttk.Button(self.tabPots, text="Get info", command=self.simulateNumbers)
        self.btnGetnumbers.pack(side=tk.RIGHT)



    def plantingThePlantInPot(self, event):
        plantedPlantName = self.plantsList.get(self.plantsList.curselection())
        self.plantedPlantDTO = self.plantService.getPlantByName(plantedPlantName)
        print(self.plantedPlantDTO)


        self.potFrame = ttk.Labelframe(self.tabPots, text=plantedPlantName)
        self.potFrame.pack(side=tk.LEFT, expand=True, anchor=tk.S)

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
        self.lvlSoilMoistureValue = ttk.Label(self.potFrame, textvariable=self.simNumbers.soilMoisture)
        self.lvlSoilMoistureValue.pack()

        self.lblSoilPh = ttk.Label(self.potFrame, text="PH vrijednost zemlje:")
        self.lblSoilPh.pack()
        self.lblSoilPhValue = ttk.Label(self.potFrame, textvariable=self.simNumbers.soilPh)
        self.lblSoilPhValue.pack()

        self.lblLight = ttk.Label(self.potFrame, text="Količina svijetla")
        self.lblLight.pack()
        self.lblLightValue = ttk.Label(self.potFrame, textvariable=self.simNumbers.light)
        self.lblLightValue.pack()

        self.lblAirTemp = ttk.Label(self.potFrame, text="Temperatura zraka")
        self.lblAirTemp.pack()
        self.lblAirTempValue = ttk.Label(self.potFrame, textvariable=self.simNumbers.airTemp)
        self.lblAirTempValue.pack()

    """Edits tab"""

    def populateEditsTab(self):
        lblInstructions = ttk.Label(self.tabEdits, text="Editing, creating and erasing plants")
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
            self.tkModelPlant.description.set(self.editedPlantDTO.description)
            self.tkModelPlant.zalijevanje.set(self.editedPlantDTO.zalijevanje)
            self.tkModelPlant.osvjetljenje.set(self.editedPlantDTO.osvjetljenje)
            self.tkModelPlant.toplina.set(self.editedPlantDTO.toplina)
            self.tkModelPlant.dohrana.set(self.editedPlantDTO.dohrana)
        print(self.editedPlantDTO)

        self.editingWindow = tk.Toplevel(self.master)
        self.editingWindow.title(f"Editing Plants")
        self.editingWindow.geometry("800x1000")

        self.lblFrameEditing = ttk.LabelFrame(self.editingWindow, text="Editing plants")
        self.lblFrameEditing.grid(row=0, column=0)

        lblPlantName = ttk.Label(self.lblFrameEditing, text="Ime biljke:")
        lblPlantName.grid(row=0, column=0)

        entryPlantName = ttk.Entry(self.lblFrameEditing, textvariable=self.tkModelPlant.name)
        entryPlantName.grid(row=0, column=1)

        lblDescription = ttk.Label(self.lblFrameEditing, text="Description:")
        lblDescription.grid(row=0, column=2)

        self.textPlantDescription = tk.Text(self.lblFrameEditing, width=60)
        self.textPlantDescription.grid(row=1, column=2)
        self.textPlantDescription.config(state=tk.NORMAL)
        self.textPlantDescription.insert("1.0", self.tkModelPlant.description.get())

        lblPlantZalijevanje = ttk.Label(self.lblFrameEditing, text="Zalijevanje:")
        lblPlantZalijevanje.grid(row=1, column=0, sticky=tk.N)

        entryZalijevanje = ttk.Entry(self.lblFrameEditing, textvariable=self.tkModelPlant.zalijevanje)
        entryZalijevanje.grid(row=1, column=1, sticky=tk.N)

        lblPlantOsvjetljenje = ttk.Label(self.lblFrameEditing, text="Osvjetljenje:")
        lblPlantOsvjetljenje.grid(row=2, column=0, sticky=tk.N)

        entryOsvjetljenje = ttk.Entry(self.lblFrameEditing, textvariable=self.tkModelPlant.osvjetljenje)
        entryOsvjetljenje.grid(row=2, column=1, sticky=tk.N)

        lblPlantToplina = ttk.Label(self.lblFrameEditing, text="Toplina:")
        lblPlantToplina.grid(row=3, column=0, sticky=tk.N)

        entryToplina = ttk.Entry(self.lblFrameEditing, textvariable=self.tkModelPlant.toplina)
        entryToplina.grid(row=3, column=1, sticky=tk.N)

        self.btnSpremi = ttk.Button(self.lblFrameEditing, text="Save Changes", command=self.saveChangees)
        self.btnSpremi.grid(row=2, column=2, sticky=tk.SE)

        rbIzmjeni = ttk.Radiobutton(
            self.lblFrameEditing,
            variable=self.tkModelPlant.opcija,
            text="Edit",
            value=1,
            command=self.provjeriAkciju
        )
        rbIzmjeni.grid(row=0, column=3, pady=10)

        rbUnesi = ttk.Radiobutton(
            self.lblFrameEditing,
            variable=self.tkModelPlant.opcija,
            text="Insert",
            value=2,
            command=self.provjeriAkciju
        )
        rbUnesi.grid(row=1, column=3, pady=10)

        rbObrisi = ttk.Radiobutton(
            self.lblFrameEditing,
            variable=self.tkModelPlant.opcija,
            text="Delete",
            value=3,
            command=self.provjeriAkciju
        )
        rbObrisi.grid(row=2, column=3, pady=10)
        self.tkModelPlant.opcija.set(1)

    def provjeriAkciju(self):
        match(self.tkModelPlant.opcija.get()):
            case 1:
                self.lblFrameEditing.config(text="Edit Plant")
                self.btnSpremi.config(text="Save Changes")
            case 2:
                self.lblFrameEditing.config(text="Insert Plant")
                self.btnSpremi.config(text="Insert Plant")
            case 3:
                self.lblFrameEditing.config(text="Delete Plant")
                self.btnSpremi.config(text="Delete Plant")
    def saveChangees(self):
        match (self.tkModelPlant.opcija.get()):
            case 1:
                dto = PlantDTO(id=self.editedPlantDTO.id,
                                name=self.tkModelPlant.name.get(),
                                photo=self.editedPlantDTO.photo,
                                description=self.textPlantDescription.get("1.0", tk.END),
                                zalijevanje=self.tkModelPlant.zalijevanje.get(),
                                osvjetljenje=self.tkModelPlant.osvjetljenje.get(),
                                toplina=self.tkModelPlant.toplina.get(),
                                dohrana=self.editedPlantDTO.dohrana)
                self.plantService.updatePlant(dto)
            case 2:
                self.plantService.createPlant(
                    self.tkModelPlant.name.get(),
                    None,
                    self.textPlantDescription.get("1.0", tk.END),
                    self.tkModelPlant.zalijevanje.get(),
                    self.tkModelPlant.osvjetljenje.get(),
                    self.tkModelPlant.toplina.get(),
                    self.tkModelPlant.dohrana.get()

                )
            case 3:
                dto = PlantDTO(id=self.editedPlantDTO.id,
                                name=self.tkModelPlant.name.get(),
                                photo=self.editedPlantDTO.photo,
                                description=self.textPlantDescription.get("1.0", tk.END),
                                zalijevanje=self.tkModelPlant.zalijevanje.get(),
                                osvjetljenje=self.tkModelPlant.osvjetljenje.get(),
                                toplina=self.tkModelPlant.toplina.get(),
                                dohrana=self.editedPlantDTO.dohrana)
                self.plantService.deleteplant(dto)


    def simulateNumbers(self):
        mylist = ["Sjenovito", "Jarko"]
        self.simNumbers.soilPh.set(random.randrange(5, 8))
        self.simNumbers.soilMoisture.set(random.randrange(20, 100))
        self.simNumbers.airTemp.set(random.randrange(10, 30))
        self.simNumbers.light.set(random.choice(mylist))





























