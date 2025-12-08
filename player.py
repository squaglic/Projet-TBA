# Define the Player class.
class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.visited_rooms = []  # Liste pour tracker l'historique des pièces visitées
        self.inventory = {} # Dictionnaire de l'inventaire
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is "blocked", c'est un passage à sens unique.
        if next_room == "Pasage interdit":
            print("\nPassage interdit !\n")
            print(self.current_room.get_long_description())
            return False

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        
        # Set the current room to the next room.
        self.current_room = next_room 

        
        # déplacer le joueur vers la pièce suivante

        self.visited_rooms.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
    
    # Define the get_history method.
    def get_history(self):
        """
        Retourne une chaîne affichant les pièces déjà visitées.
        Format conforme à l’énoncé du projet.
        """
        if len(self.visited_rooms) == 0:
            return ""  # rien à afficher si on n’a visité qu’une pièce
    
        history = "Vous avez déjà visité les pièces suivantes:\n"
    
        # On ne liste pas la pièce actuelle, uniquement les précédentes
        for room in self.visited_rooms:
            history += f"  - {room.description}\n"
    
        return history

    # Define the get_inventory method.
    def get_inventory(self):

        # Test if the inventory is empty
        if len(self.inventory) == 0:
            return "\n Inventaire vide"
        
        inventory = "Items possédés : \n"

        for item in self.inventory.values():
            inventory += f"  - {item.name} : {item.description} \n"
        return inventory
