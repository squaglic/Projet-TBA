"""Module contenant la classe `Command`.

Ce module gère les commandes du jeu d'aventure. Chaque commande est représentée
par un mot-clé, une chaîne d'aide, une fonction d'action associée et le nombre
de paramètres requis.
"""


class Command:
    """Représente une commande exécutable du jeu.

    Une commande est composée d'un mot-clé (ex: "go", "help"), d'une description
    d'aide, d'une fonction action à exécuter et du nombre de paramètres attendus.

    Attributes:
        command_word (str): Le mot-clé de la commande.
        help_string (str): La chaîne d'aide décrivant la commande.
        action: La fonction à exécuter pour cette commande.
        number_of_parameters (int): Le nombre de paramètres requis.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    # The string representation of the command.
    def __str__(self):
        return  self.command_word \
                + self.help_string
