# Description: Character class

class Character:
    """
    Représente un personnage non-joueur (PNJ) du jeu d'aventure.
    
    Attributes:
        name (str): Le nom du personnage.
        description (str): La description du personnage.
        current_room (Room): La salle où se trouve le personnage.
        msgs (list): Une liste des messages à afficher lors d'une interrogation.
    
    Methods:
        talk(): Retourne un message aléatoire de la liste des messages.
    
    Exemple:
        >>> from character import Character
        >>> character = Character("Gardien", "Un vieux gardien mystérieux", None, ["Bienvenue...", "Attention aux ombres!"])
        >>> character.talk()
        'Bienvenue...'
    """
    
    def __init__(self, name, description, current_room, msgs):
        """
        Initialise un personnage.
        
        Args:
            name (str): Le nom du personnage.
            description (str): La description du personnage.
            current_room (Room): La salle où se trouve le personnage.
            msgs (list): Une liste des messages à afficher.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.msgs_cycle = list(msgs)  # Copie mutable pour le cycle des messages
    
    def __str__(self):
        """
        Retourne une représentation textuelle du personnage.
        
        Returns:
            str: Une chaîne au format "Nom : description"
        """
        return f"{self.name} : {self.description}"
    
    def talk(self):
        """
        Retourne un message aléatoire de la liste des messages du personnage.
        
        Returns:
            str: Un message sélectionné aléatoirement dans la liste des messages.
        """
        import random
        if self.msgs:
            return random.choice(self.msgs)
        return ""
    
    def get_msg(self):
        """
        Affiche cycliquement les messages associés au personnage non-joueur.
        
        Cette méthode affiche les messages dans l'ordre, et une fois un message affiché,
        il est supprimé de la liste. Quand tous les messages ont été affichés,
        on recommence depuis le début (cycliquement).
        
        Returns:
            str: Le message à afficher, ou une chaîne vide s'il n'y a aucun message.
        
        Exemple:
            >>> from character import Character
            >>> character = Character("Gandalf", "un magicien", None, ["Bienvenue!", "Au revoir!"])
            >>> character.get_msg()
            'Bienvenue!'
            >>> character.get_msg()
            'Au revoir!'
            >>> character.get_msg()
            'Bienvenue!'
        """
        # Si la liste cyclique est vide, la réinitialiser
        if len(self.msgs_cycle) == 0:
            self.msgs_cycle = list(self.msgs)
        
        # Si le personnage n'a pas de messages, retourner une chaîne vide
        if len(self.msgs_cycle) == 0:
            return ""
        
        # Récupérer et supprimer le premier message
        msg = self.msgs_cycle.pop(0)
        return msg
    
    def move(self):
        """
        Déplace le personnage dans une pièce adjacente au hasard avec une probabilité de 50%.
        
        À chaque appel :
        - Le personnage a une chance sur deux de se déplacer ou de rester sur place
        - S'il se déplace, il va dans une pièce adjacente au hasard
        
        Returns:
            bool: True si le personnage s'est déplacé, False sinon.
        
        Exemple:
            >>> from character import Character
            >>> from room import Room
            >>> room1 = Room("Salle 1", "Une salle")
            >>> room2 = Room("Salle 2", "Une autre salle")
            >>> room1.exits = {"nord": room2}
            >>> character = Character("Gardien", "Un gardien", room1, ["Bonjour"])
            >>> character.move()  # Retourne True ou False
        """
        import random
        
        # Le personnage a une chance sur deux de se déplacer
        if random.choice([True, False]):
            # Vérifier qu'il y a des sorties disponibles
            if self.current_room and self.current_room.exits:
                # Filtrer les sorties pour ne garder que les vraies salles (pas None)
                exit_rooms = [room for room in self.current_room.exits.values() if room is not None]
                # Vérifier qu'il y a au moins une sortie valide
                if exit_rooms:
                    self.current_room = random.choice(exit_rooms)
                    return True
        
        # Le personnage ne se déplace pas
        return False