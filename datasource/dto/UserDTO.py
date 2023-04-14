

class UserDTO:

    def __init__(self, id, name, lastname, user, password):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.user = user
        self.password = password

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.lastname}, {self.user}, {self.password}"