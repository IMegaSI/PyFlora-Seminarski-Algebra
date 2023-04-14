from utils.DBUtils import DBUtils
from datasource.dto.UserDTO import UserDTO
from datasource.tk.TkUser import TkUser

class UserService:

    TABLE_NAME = "users"

    def __init__(self, sqlconnection):
        self.connection = sqlconnection
        self.createTable()
        self._insertAdmin() #ovo triba samo jednom zavrtit (uspjesno napravljeno)


    def createTable(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                lastname VARCHAR(30) NOT NULL,
                user VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(5) NOT NULL 
                );
                """
        DBUtils.izvrsiIZapisi(self.connection, query)

    def createUser(self, name, lastname, user, password):
        query = f"""
                INSERT INTO {self.TABLE_NAME} (name, lastname, user, password)
                VALUES ('{name}', '{lastname}', '{user}', '{password}');
                """
        DBUtils.izvrsiIZapisi(self.connection, query)

    # admin ubacen u bazu, pa ovo nije vise potrebno,
    # eventualno neka izmjena ili rucni unos
    def _insertAdmin(self):
        self.createUser("Admin", "Admin", "user", "admin")

    def grabUserfromDB(self, user, password):
        query = f"SELECT * FROM {self.TABLE_NAME} WHERE user = '{user}' AND password ='{password}';"
        result = DBUtils.dohvatiPodatke(self.connection, query, one=True)
        if result is not None:
            dto = UserDTO(result[0], result[1], result[2], result[3], result[4])
            print(dto)
            return dto
        else:
            return None

    def updateUser(self, dto: UserDTO):
        query = f"""
                UPDATE {self.TABLE_NAME}
                SET name='{dto.name}', lastname='{dto.lastname}', user='{dto.user}', password='{dto.password}'
                WHERE id={dto.id};
                """
        DBUtils.izvrsiIZapisi(self.connection, query)

