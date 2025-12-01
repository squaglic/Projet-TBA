# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
    
        
        # Setup rooms

        Eldregrove = Room("forêtd’Eldregrove"," dans une forêt ancienne où les arbres semblent observer les voyageurs, et où la magie sauvage imprègne chaque souffle de vent.")
        self.rooms.append(Eldregrove)
        Verdenfall = Room("Château de Verdenfall", " dans une ancienne couronne du royaume, ce château en ruines résonne encore des murmures d’un pouvoir oublié.")
        self.rooms.append(Verdenfall)
        Brunnhold = Room("Brunnhold", " dans une village partiellement ravagé, dont les habitants vivent dans une méfiance constante envers tout ce qui leur est étranger.")
        self.rooms.append(Brunnhold)
        Mireval = Room("Mireval", "dans un Hameau noyé dans une brume perpétuelle, marqué par une étrange épidémie que nul ne parvient à comprendre.")
        self.rooms.append(Mireval)
        Stonebridge = Room("Stonebridge", "dans une Forteresse-village robuste, dernier rempart organisé de l’humanité contre les ténèbres grandissantes.")
        self.rooms.append(Stonebridge)
        Dornhollow = Room("Dornhollow", " dans une village englouti par les marécages, où les habitants jurent entendre des voix sous la boue.")
        self.rooms.append(Dornhollow)
        Blackmere = Room("Blackmere", "dans un Hameau lacustre dont les pêcheurs disparaissent dans les eaux sombres.")
        self.rooms.append(Blackmere)
        Grisepierre = Room("Grisepierre", "dans un Hameau minier hanté par un minerai étrange qui semble respirer.")
        self.rooms.append(Grisepierre)
        Val_Cendré = Room("Val-Cendré", "dans une village couvert d’une cendre éternelle, marqué par un incendie surnaturel.")
        self.rooms.append(Val_Cendré)
        Ravenglade = Room("Ravenglade" , "dans un Hameau forestier envahi de corbeaux, où aucune naissance n’a eu lieu depuis des années.")
        self.rooms.append(Ravenglade)
        Sangrun = Room("Sangrun", "dans une grotte où réside les âmes tourmentées du village."         )
        self.rooms.append(Sangrun)
        # Create exits for rooms

        # Bloquer le passage direct entre Forest et Tower :
        # - forest.E ne mène plus à tower
        # - tower.O ne mène plus à forest
        Verdenfall.exits = {"N" :Brunnhold , "E" : None, "S" : None , "O" : None }
        Brunnhold.exits = {"N" : None, "E" : None, "S" :Verdenfall , "O" :Mireval }
        Mireval.exits = {"N" : Dornhollow, "E" : Brunnhold, "S" : None, "O" : None}
        Dornhollow.exits = {"N" : None, "E" : Sangrun, "S" : Mireval , "O" : None }
        # Sangrun : passage à sens unique. On peut y aller (depuis Dornhollow à l'O), mais on ne peut pas revenir au S vers Brunnhold
        Sangrun.exits = {"N" : None, "E" : None, "S" :Brunnhold  , "O" : Dornhollow}
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Verdenfall

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}'  non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()