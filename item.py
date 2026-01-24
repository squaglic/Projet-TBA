"""Module contenant la classe `Item`.

Ce module gère les objets du jeu d'aventure que le joueur et les salles
peuvent contenir.
"""

class Item:
    """
    Représente un objet du jeu d'aventure.
    
    Un objet possède un nom, une description et un poids. Il peut être
    ramassé par le joueur et placé dans son inventaire.
    
    Attributes:
        name (str): Le nom de l'objet.
        description (str): La description détaillée de l'objet.
        weight (float): Le poids de l'objet en kilogrammes.
    
    Methods:
        __init__(name, description, weight): Initialise un objet.
        __str__(): Retourne une représentation textuelle de l'objet.
    
    Exemple:
        >>> item = Item("Épée rouillée", "Une vieille épée avec du sang séché", 2.5)
        >>> str(item)
        'Épée rouillée : Une vieille épée avec du sang séché  (2.5 kg)'
    """

    def __init__(self, name, description, weight):
        """
        Initialise un nouvel objet.
        
        Args:
            name (str): Le nom de l'objet.
            description (str): La description détaillée de l'objet.
            weight (float): Le poids de l'objet en kilogrammes.
        """
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet.
        
        Returns:
            str: Une chaîne au format "Nom : description (poids kg)"
        """
        return f"{self.name} : {self.description}  ({self.weight} kg)"
