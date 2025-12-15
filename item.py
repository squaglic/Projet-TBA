# Description: Item class

class Item:
    """
    ff
    
    
    
    """

    #Define the constructor
    def __init__(self,name,description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    #Define the __str__() method

    def __str__(self):
        return f"{self.name} : {self.description}  ({self.weight} kg)"