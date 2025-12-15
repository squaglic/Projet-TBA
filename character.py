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
    
    def move_pnj(self):
        """
        Déplace le personnage non-joueur de manière aléatoire.
        
        Le personnage a une chance sur deux de se déplacer vers une salle adjacente.
        S'il se déplace, il choisit une direction aléatoire parmi celles disponibles.
        
        Returns:
            bool: True si le personnage s'est déplacé, False sinon.
        
        Exemple:
            >>> from room import Room
            >>> from character import Character
            >>> room1 = Room("Forest", "une forêt")
            >>> room2 = Room("Castle", "un château")
            >>> room1.exits = {"N": room2, "E": None, "S": None, "O": None}
            >>> character = Character("Gandalf", "un magicien", room1, ["Salut!"])
            >>> moved = character.move_pnj()
            >>> moved in [True, False]
            True
        """
        import random
        
        # Chance sur deux de se déplacer
        if random.random() > 0.5:
            # Le personnage reste sur place
            return False
        
        # Le personnage se déplace
        # Récupérer toutes les directions disponibles (N, E, S, O)
        directions = ["N", "E", "S", "O"]
        
        # Choisir une direction aléatoire
        direction = random.choice(directions)
        
        # Vérifier que la salle existe dans cette direction
        next_room = self.current_room.exits.get(direction)
        
        # Si la salle n'existe pas ou est bloquée, rester sur place
        if next_room is None or next_room == "passage interdit":
            return False
        
        # Se déplacer vers la nouvelle salle
        self.current_room = next_room
        return True
