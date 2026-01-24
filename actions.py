"""Module contenant les actions du jeu.

Ce module contient toutes les fonctions qui exécutent les actions du jeu en réponse
aux commandes du joueur. Chaque fonction action :
- Prend 3 paramètres : le jeu, la liste des mots de la commande, et le nombre attendu de paramètres
- Retourne True si l'action s'est exécutée avec succès, False sinon
- Affiche un message d'erreur si le nombre de paramètres est incorrect
"""

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """
    Classe regroupant toutes les actions exécutables dans le jeu.
    
    Chaque méthode représente une action que le joueur peut effectuer via une commande.
    Les méthodes de cette classe sont des fonctions statiques qui traitent les entrées
    du joueur et modifient l'état du jeu en conséquence.
    
    Methods:
        go(game, list_of_words, number_of_parameters): Déplace le joueur dans une direction.
        quit(game, list_of_words, number_of_parameters): Quitte le jeu.
        help(game, list_of_words, number_of_parameters): Affiche l'aide.
        back(game, list_of_words, number_of_parameters): Retourne à la salle précédente.
        look(game, list_of_words, number_of_parameters): Affiche les objets de la salle.
        take(game, list_of_words, number_of_parameters): Prend un objet.
        check(game, list_of_words, number_of_parameters): Affiche l'inventaire.
        drop(game, list_of_words, number_of_parameters): Dépose un objet.
        talk(game, list_of_words, number_of_parameters): Parle à un personnage.
        quests(game, list_of_words, number_of_parameters): Affiche les quêtes.
        quest(game, list_of_words, number_of_parameters): Affiche détails d'une quête.
        activate(game, list_of_words, number_of_parameters): Active une quête.
        rewards(game, list_of_words, number_of_parameters): Affiche les récompenses.
        use(game, list_of_words, number_of_parameters): Utilise un objet.
    """

    def go(self, game, list_of_words, number_of_parameters):
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
        - quests : afficher la liste des quêtes
        - quest <titre> : afficher les détails d'une quête

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

    def quit(self, game, list_of_words, number_of_parameters):
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

    def help(self, game, list_of_words, number_of_parameters):
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

    def back(self, game, list_of_words, number_of_parameters):
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
        if len(player.visited_rooms)  == 0:
            print("\nAucune pièce précédente à laquelle revenir.\n")
            return False

        # Revenir à la dernière pièce visitée
        player.current_room = player.visited_rooms.pop()
        print(player.current_room.get_long_description())
        # Afficher l'historique des pièces visitées
        history = player.get_history()
        if history:
            print(history)
        return True

    def look(self, game, list_of_words, number_of_parameters):
        """
        Regarder autour de soi dans la pièce actuelle.
        Affiche la description de la salle, les items et les personnages présents.
        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.
        Returns:
            bool: True si l'action a réussi, False sinon.
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

        player = game.player
        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = player.current_room
        output = room.get_long_description()
        output += room.get_inventory()
        output += room.get_characters()
        print(output)
        return True


    def take(self, game, list_of_words, number_of_parameters):
        """
        Prendre un item présent dans la room actuelle.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi, False sinon.
        """
        player = game.player
        room = player.current_room

        # Vérifier le nombre de paramètres
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]

        # Vérifier si l'item existe dans la room
        item = room.inventory.get(item_name)
        if item is None:
            print(f"\nL'objet '{item_name}' n'existe pas dans cette salle.\n")
            return False

        # Ajouter l'item à l'inventaire du joueur
        player.inventory[item_name] = item
        player.current_weight += item.weight

        # Retirer l'item de l'inventaire de la room
        del room.inventory[item_name]
        room.current_weight -= item.weight

        print(f"\nVous avez pris l'objet '{item_name}'.\n")

        # Vérifier les objectifs de quête liés à la prise d'items
        player.quest_manager.check_action_objectives("prendre", item_name)

        return True

    def check(self, game, list_of_words, number_of_parameters):
        """
        Vérifier l'inventaire du joueur.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi, False sinon.
        """
        player = game.player

        # Vérifier le nombre de paramètres
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Afficher l'inventaire du joueur
        if len(player.inventory) == 0:
            print("\nVotre inventaire est vide.\n")
            return True

        print("\nVotre inventaire contient les objets suivants:")
        for item in player.inventory.values():
            print(f" - {item.name}: {item.description} (poids: {item.weight})")
        print(f"\nPoids total de l'inventaire: {player.current_weight}\n")
        return True

    def drop(self, game, list_of_words, number_of_parameters):
        """
        Lâcher un item de l'inventaire du joueur dans la room actuelle.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi, False sinon.
        """
        player = game.player
        room = player.current_room

        # Vérifier le nombre de paramètres
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]

        # Vérifier si l'item existe dans l'inventaire du joueur
        item = player.inventory.get(item_name)
        if item is None:
            print(f"\nL'objet '{item_name}' n'existe pas dans votre inventaire.\n")
            return False

        # Ajouter l'item à l'inventaire de la room
        room.inventory[item_name] = item
        room.current_weight += item.weight

        # Retirer l'item de l'inventaire du joueur
        del player.inventory[item_name]
        player.current_weight -= item.weight

        print(f"\nVous avez lâché l'objet '{item_name}'.\n")
        return True

    def talk(self, game, list_of_words, number_of_parameters):
        """
        Parler à un personnage non-joueur (PNJ) présent dans la salle actuelle.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi, False sinon.
        """
        player = game.player
        room = player.current_room

        # Vérifier le nombre de paramètres
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        character_name = list_of_words[1]

        # Vérifier s'il y a un personnage avec ce nom dans la room
        character = None
        for char in room.characters:
            if char.name.lower() == character_name.lower():
                character = char
                break

        if character is None:
            print(f"\n'{character_name}' ne se trouve pas ici.\n")
            return False

        # Afficher le message du personnage
        msg = character.get_msg()
        print(f"\n{character.name} : {msg}\n")

        # Vérifier les objectifs de quête liés à parler à un personnage
        player.quest_manager.check_action_objectives("parler", character_name)

        return True

    def quests(self, game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True

    def use(self, game, list_of_words, number_of_parameters):
        """
        Utiliser un objet de l'inventaire du joueur.

        Args:
            game (Game): L'objet de jeu.
            list_of_words (list): Les mots de la commande.
            number_of_parameters (int): le nombre de paramètre attendu.

        Returns:
            bool: True si l'action a réussi, False sinon.
        """
        player = game.player
        room = player.current_room

        # Vérifier le nombre de paramètres
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]

        # Vérifier si l'item existe dans l'inventaire du joueur
        item = player.inventory.get(item_name)
        if item is None:
            print(f"\nL'objet '{item_name}' n'est pas dans votre inventaire.\n")
            return False

        # Vérifier si c'est le poison
        if item_name == "poison":
            # Marquer le poison comme utilisé (termine la partie)
            player.used_poison = True

            # Vérifier si toutes les quêtes sont complétées
            all_quests_completed = all(quest.is_completed for quest in player.quest_manager.quests)

            # Vérifier si le joueur est à Verdenfall
            if not all_quests_completed or room.name != "Château de Verdenfall":
                print(f"\nVous avez utilisé le '{item.description}'.\n")
                print("Vous avez révélé les secrets de la malédiction sans sauver le royaume !\n")
                return True

            # Conditions de victoire respectées
            print(f"\nVous avez utilisé le '{item.description}'.\n")
            print("Vous donnez votre vie ainsi que les âmes pour sauver le royaume.\n")
            print("Les ténèbres se dissipent enfin du royaume...\n")
            return True

        # Pour les autres objets
        print("\nVous ne pouvez pas utiliser cet objet maintenant.\n")
        return False
        