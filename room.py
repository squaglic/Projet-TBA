"""Module contenant la classe `Room`.

La classe `Room` représente un lieu (salle) du jeu d'aventure. Chaque
instance possède un nom, une description et un dictionnaire de sorties
(exits) vers d'autres salles.

Les sorties utilisent les directions cardinales :
  - "N" pour Nord
  - "E" pour Est
  - "S" pour Sud
  - "O" pour Ouest

Une valeur `None` pour une sortie signifie qu'il n'y a pas de salle dans
cette direction.
"""

class Room:

    """Représente une salle du jeu.

    Attributes:
        name (str): Nom de la salle (ex: "Forest").
        description (str): Description courte de la salle affichée au joueur.
        exits (dict): Dictionnaire des sorties cardinales vers d'autres
            objets `Room`. Les clés sont des chaînes "N", "E", "S", "O".

    Methods:
        get_exit(direction): Retourne la `Room` située dans la direction
            donnée (ou `None` si aucune sortie).
        get_exit_string(): Retourne une chaîne listant les directions
            disponibles (ex: "Sorties: N, E").
        get_long_description(): Retourne la description complète affichée
            au joueur (description + sorties).

    Exemple:
        >>> r = Room("Test", "dans une salle de test.")
        >>> r.exits = {"N": None, "E": None, "S": None, "O": None}
        >>> r.get_exit("N") is None
        True
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
    
    def add_item(self, item):
        """Ajoute un item à la salle.

        Args:
            item (Item): L'objet `Item` à ajouter à la salle.
        """
        self.items.append(item)
        
    
    def get_exit(self, direction):

        """Retourne la salle reliée par la sortie `direction`.

        Args:
            direction (str): Une des valeurs "N", "E", "S", "O".

        Returns:
            Room | None: L'objet `Room` si la sortie existe, sinon `None`.
                        Retourne "Passage interdit" si le passage est à sens unique (interdit).
        """
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return "passage interdit"
    
    def get_exit_string(self):
        """Retourne une chaîne décrivant les sorties disponibles.

        Ne liste que les directions qui pointent vers une salle (non-None).
        """
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    def get_long_description(self):
        """Retourne la description complète de la salle, incluant les sorties."""
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
