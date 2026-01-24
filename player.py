"""Module contenant la classe `Player`.

Ce module gère le joueur du jeu d'aventure, y compris ses déplacements,
son inventaire, ses récompenses et ses quêtes.
"""

from quest import QuestManager

class Player():
    """
    Représente le joueur du jeu d'aventure.
    
    Attributes:
        name (str): Le nom du joueur.
        current_room (Room): La salle actuellement occupée par le joueur.
        visited_rooms (list): Historique des salles visitées.
        inventory (dict): Dictionnaire des objets possédés par le joueur.
        current_weight (float): Poids total de l'inventaire en kg.
        move_count (int): Nombre de déplacements effectués.
        quest_manager (QuestManager): Gestionnaire des quêtes du joueur.
        rewards (list): Liste des récompenses obtenues.
    
    Methods:
        __init__(name): Initialise le joueur avec un nom.
        move(direction): Déplace le joueur dans une direction cardinale.
        add_reward(reward): Ajoute une récompense à la liste.
        show_rewards(): Affiche toutes les récompenses obtenues.
        get_history(): Retourne l'historique des salles visitées.
    """

    def __init__(self, name):
        """
        Initialise un joueur avec un nom donné.
        
        Args:
            name (str): Le nom du joueur.
        
        Crée les structures de base : inventaire vide, liste de salles visitées,
        quêtes et récompenses vides.
        """
        self.name = name
        self.current_room = None
        self.visited_rooms = []
        self.inventory = {}
        self.current_weight = 0
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []

    def move(self, direction):
        """
        Déplace le joueur dans la direction cardinale spécifiée.
        
        Args:
            direction (str): Direction cardinale (N, E, S, O).
        
        Returns:
            bool: True si le déplacement a été effectué avec succès, False sinon.
        
        Cette méthode :
        - Récupère la salle adjacente dans la direction donnée
        - Ajoute la salle actuelle à l'historique
        - Met à jour la salle actuelle du joueur
        - Vérifie les objectifs de quête (visite de salle, compteur de déplacement)
        """
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

        # Move the player to the next room

        self.visited_rooms.append(self.current_room)

        # Set the current room to the next room.
        self.current_room = next_room

        print(self.current_room.get_long_description())

        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)

        return True


    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

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
