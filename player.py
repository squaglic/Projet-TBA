# Define the Player class.

from quest import QuestManager

class Player():

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.visited_rooms = []  # Liste pour tracker l'historique des pièces visitées
        self.inventory = {}  # Inventaire du joueur
        self.current_weight = 0  # Poids total de l'inventaire
        self.move_count = 0  # Compteur de déplacements
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
        
    
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
        
        # déplacer le joueur vers la pièce suivante

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

    
