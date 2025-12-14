# Description: Item class

class Item:
    """Représente un item du jeu avec un nom, une description et un poids."""

    #Define the constructor
    def __init__(self, name, description, weight=0):
        self.name = name
        self.description = description
        self.weight = weight

    #Define the __str__() method

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"