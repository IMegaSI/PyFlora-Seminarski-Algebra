from  utils.DBUtils import DBUtils
from datasource.dto.PlantDTO import PlantDTO



class PlantService:

    TABLE_NAME = "plants"

    def __init__(self, sqlconnection):
        self.connection = sqlconnection
        self.createTable()
        #self._insertPlants() # zavrtit jednom da se napravi baza biljki (odrađeno)

    def createTable(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME}(
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            VARCHAR(30) NOT NULL UNIQUE,
                foto            VARCHAR(30),
                description     TEXT,
                zalijevanje     VARCHAR(30),
                osvjetljenje    VARCHAR(30),
                toplina         VARCHAR(30),
                dohrana         BOOLEAN NOT NULL);
                """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def createPlant (self, name, foto, description, zalijevanje, osvjetljenje, toplina, dohrana):
        query = f"""
                INSERT INTO {self.TABLE_NAME} (name, foto, description, zalijevanje, osvjetljenje, toplina, dohrana)
                VALUES ('{name}', '{foto}', '{description}', '{zalijevanje}', '{osvjetljenje}', '{toplina}', '{dohrana}');
                """
        DBUtils.izvrsiIZapisi(self.connection, query)


    # Opisi su ručno ubačeni u bazu nakon inserta
    def _insertPlants(self):
        self.createPlant("Aloe vera", "plants/aloa.jpg", "plants/aloe_vera.txt", "Mjesecno", "Sjenovito", "Umjerena", False)
        self.createPlant("Bosiljak", "plants/basil.jpg", "plants/bosiljak.txt", "Tjedno", "Jarko", "Toplija", True)
        self.createPlant("Kadulja", "plants/sage.jpg", "plants/kadulja.txt", "Tjedno", "Jarko", "Toplija", True)
        self.createPlant("Kopar", "plants/dill.jpg", "plants/kopar.txt", "Dnevno", "Sjenovito", "Umjerena", True)
        self.createPlant("Limuska Trava", "plants/lemongrass.png", "plants/limunska_trava.txt", "Dnevno", "Jarko", "Toplija", False)
        self.createPlant("Mazuran", "plants/marjoram.jpg", "plants/mazuran.txt", "Tjedno", "Sjenovito", "Toplija", True)
        self.createPlant("Metvica", "plants/mint.jpg", "plants/metvica.txt", "Dnevno", "Jarko", "Toplija", False)
        self.createPlant("Origano", "plants/oregano.jpg", "plants/origano.txt", "Tjedno", "Sjenovito", "Toplija", False)
        self.createPlant("Persin", "plants/parsely.jpg", "plants/persin.txt", "Dnevno", "Sjenovito", "Umjerena", True)
        self.createPlant("Ruzmarin", "plants/rosemary.jpg", "plants/ruzmarin.txt", "Tjedno", "Jarko", "Toplija", False)
        self.createPlant("Sljez", "plants/mallow.jpg", "plants/sljez.txt", "Dnevno", "Sjenovito", "Umjerena", True)
        self.createPlant("Timijan", "plants/thyme.jpg", "plants/timijan.txt", "Mjesecno", "Jarko", "Toplija", False)

    def getAllPlants(self):
        plants = []
        query = f"SELECT * FROM {self.TABLE_NAME}"
        rows = DBUtils.dohvatiPodatke(self.connection, query)
        for row in rows:
            newPlantDto = PlantDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            plants.append(newPlantDto)
        return plants


    def getPlantById(self, plant_id):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE id = {plant_id}"

        row = DBUtils.dohvatiPodatke(self.connection, query, True)

        if row is not None:
            newPlantDto = PlantDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return newPlantDto
        else:
            return None

    def getPlantByName(self, name):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE name = '{name}'"

        row = DBUtils.dohvatiPodatke(self.connection, query, True)

        if row is not None:
            newPlantDto = PlantDTO(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return newPlantDto
        else:
            return None





