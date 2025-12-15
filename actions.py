# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1].upper()
        # Validate the direction entered by the player.
        if direction not in ("N", "E", "S", "O"):
            print(f"\nDirection '{direction}' invalide. Utilisez N, E, S ou O.\n")
            return False

        # Move the player in the direction specified by the parameter.
        moved = player.move(direction)
        if moved:
            print(player.current_room.get_long_description())
            history = player.get_history()
            if history:
                print(history)
        return moved

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    def back(game, list_of_words, number_of_parameters):
        """
        revenir à la pièce précédente (retour en arrière).

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi , False sinon.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> back(game, ["back"], 0)
        True
        >>> back(game, ["back", "N"], 0)
        False
        >>> back(game, ["back", "N", "E"], 0)
        False

        """

        # Vérifier le nombre de paramètre.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        if len(player.visited_rooms) < 2:
            print("\nAucune pièce précédente à laquelle revenir.\n")
            return False

        # Revenir à la dernière pièce visitée
        previous_room = player.visited_rooms.pop()
        player.current_room = previous_room
        print(player.current_room.get_long_description())
        # Afficher l'historique des pièces visitées
        history = player.get_history()
        if history:
            print(history)
        return True
    def look (game, list_of_words, number_of_parameters):
        """
        Affiche la description complète de la pièce actuelle.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi , False sinon.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> look(game, ["look"], 0)
        True
        >>> look(game, ["look", "N"], 0)
        False
        >>> look(game, ["look", "N", "E"], 0)
        False

        """

        # Vérifier le nombre de paramètre.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(player.current_room.get_long_description())
        return True
        # affcher les objets dans la pièce actuelle
        if curruent_room.items:
            print("\nOn voit:")
            for item in current_room.items:
                print(f" - {item.name} : {item.description} ({item.weight} kg)")
        else:
            print("\nIl n'y a rien ici.")
        print()
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Vérifie le contenu de l'inventaire du joueur.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi , False sinon.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> check(game, ["check"], 0)
        True
        >>> check(game, ["check", "N"], 0)
        False
        >>> check(game, ["check", "N", "E"], 0)
        False

        """

        # Vérifier le nombre de paramètre.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print("\n" + player.get_inventory() +"\n")
        return True



    def take(game, list_of_words, number_of_parameters):
    # prendre un objet dans la pièce 
        """
        Prendre un objet dans la pièce actuelle et l'ajouter à l'inventaire du joueur.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi , False sinon.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> take(game, ["take", "sword"], 1)
        True
        >>> take(game, ["take"], 1)
        False
        >>> take(game, ["take", "sword", "shield"], 1)
        False

        """

        l= len(list_of_words)
        player= game.player
        current_room= player.current_room
        if l < 2: 
            print("\n")
    
    def drop (game, list_of_words, number_of_parameters):
    # déposer un objet dans la pièce actuelle depuis l'inventaire du joueur
        """
        Déposer un objet de l'inventaire du joueur dans la pièce actuelle.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi , False sinon.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> drop(game, ["drop", "sword"], 1)
        True
        >>> drop(game, ["drop"], 1)
        False
        >>> drop(game, ["drop", "sword", "shield"], 1)
        False

        """

        l= len(list_of_words)
        player= game.player
        current_room= player.current_room
        # on vérifie ici le nombre de paramètres 
        if l!= number_of_parameters + 1:
            command_word = list_of_words[0]
            print(f"\n La commande '{command_word}' prend 1 seul paramètre.\n")
            return False
        
        # on vérifie si un nom d'objet a été fourni
        if l < 2:
            print("\nVeuillez spécifier le nom de l'objet à déposer.\n")
            return False
        item_name = " ".join(list_of_words[1:])

        # on vérifie si l'objet est dans l'inventaire du joueur
        item_to_drop = None
        exact_key = None
        for key, item in player.inventory.items():
            if item.name.lower() == item_name.lower():
                item_to_drop = item
                exact_key = key
                break
                
        # si l'objet n'est pas trouvé dans l'inventaire
        if item_to_drop is None:
            print(f"\nVous n'avez pas '{item_name}' dans votre inventaire.\n")
            return False
        # on dépose l'objet dans la pièce actuelle

        current_room.items.append(item_to_drop)
        # on le retire de l'inventaire du joueur

        del player.inventory[exact_key]
        print(f"\nVous avez déposé '{item_to_drop.name}' dans la pièce.\n")
        return True