# Description: Item class

class Item:
    """
    ff
    
    
    
    """

    #Define the constructor
    def __init__(self,name,description):
        self.name = name
        self.description = description

    #Define the __str__() method

    def __str__(self):
        return f"{self.name} : {self.description}"