

class PlantDTO:
    def __init__(self, id, name, photo, description, zalijevanje, osvjetljenje, toplina, dohrana):
        self.id = id
        self.name = name
        self.photo = photo
        self.description = description
        self.zalijevanje = zalijevanje
        self.osvjetljenje = osvjetljenje
        self.toplina = toplina
        self.dohrana = dohrana

    def __repr__(self):
        return f"{self.id}, {self.name}"

