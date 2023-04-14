from GUI.Screens.MainWindow import MainWindow
from SQLstuff.sqlBaseInit import * # sql3 i DBusers zasad
from service.UserService import UserService
from service.PlantService import PlantService


if __name__ == '__main__':
    sqlconnection = DBusers()
    userService = UserService(sqlconnection)
    plantService = PlantService(sqlconnection)
    App = MainWindow(userService, plantService)
    App.mainloop()

#ako ja ode napravim neke promjene