# Description: Game class

# Debug mode
DEBUG = False

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

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
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : afficher la liste des items présents dans la zone où se situe le joueur", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " : prendre un Item présent dans la zone où se situe le joueur", Actions.take, 1)
        self.commands["take"] = take
        check = Command("check", " : vérifier l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        drop = Command("drop", " : déposer un Item de l'inventaire du joueur dans la zone où il se situe", Actions.drop, 1)
        self.commands["drop"] = drop
        talk = Command("talk", " <nom> : parler à un personnage non-joueur (PNJ) présent dans la zone où se situe le joueur", Actions.talk, 1)
        self.commands["talk"] = talk
    
        
        # Setup rooms

        Eldregrove = Room("forêtd’Eldregrove","une forêt ancienne où les arbres semblent observer les voyageurs, et où la magie sauvage imprègne chaque souffle de vent.")
        self.rooms.append(Eldregrove)
        Verdenfall = Room("Château de Verdenfall", "une ancienne couronne du royaume, ce château en ruines résonne encore des murmures d’un pouvoir oublié.")
        self.rooms.append(Verdenfall)
        Brunnhold = Room("Brunnhold", "un village partiellement ravagé, dont les habitants vivent dans une méfiance constante envers tout ce qui leur est étranger.")
        self.rooms.append(Brunnhold)
        Mireval = Room("Mireval", "un Hameau noyé dans une brume perpétuelle, marqué par une étrange épidémie que nul ne parvient à comprendre.")
        self.rooms.append(Mireval)
        Stonebridge = Room("Stonebridge", "une Forteresse-village robuste, dernier rempart organisé de l’humanité contre les ténèbres grandissantes.")
        self.rooms.append(Stonebridge)
        Dornhollow = Room("Dornhollow", "un village englouti par les marécages, où les habitants jurent entendre des voix sous la boue.")
        self.rooms.append(Dornhollow)
        Blackmere = Room("Blackmere", "un Hameau lacustre dont les pêcheurs disparaissent dans les eaux sombres.")
        self.rooms.append(Blackmere)
        Grisepierre = Room("Grisepierre", "un Hameau minier hanté par un minerai étrange qui semble respirer.")
        self.rooms.append(Grisepierre)
        Val_Cendré = Room("Val-Cendré", "un village couvert d’une cendre éternelle, marqué par un incendie surnaturel.")
        self.rooms.append(Val_Cendré)
        Ravenglade = Room("Ravenglade" , "un Hameau forestier envahi de corbeaux, où aucune naissance n’a eu lieu depuis des années.")
        self.rooms.append(Ravenglade)
        Sangrun = Room("Sangrun", "une grotte où résident les âmes tourmentées du village."         )
        self.rooms.append(Sangrun)

        #Setup pnjs
        guardian = Character("Gardien", "Un vieux gardien mystérieux", Brunnhold, ["Bienvenue voyageur, je suis le gardien de ce village.", "Attention aux ombres qui rôdent dans ces terres!"])
        Brunnhold.characters.append(guardian)


        # Create exits for rooms

        # Bloquer le passage direct entre Forest et Tower :
        # - forest.E ne mène plus à tower
        # - tower.O ne mène plus à forest
        Verdenfall.exits = {"N" : None , "E" : None, "S" : Sangrun , "O" : None }
        Brunnhold.exits = {"N" : None, "E" : Blackmere, "S" : Eldregrove , "O" : Dornhollow }
        Mireval.exits = {"N" : None, "E" : Sangrun, "S" : Stonebridge, "O" : None}
        Dornhollow.exits = {"N" : Stonebridge, "E" : Val_Cendré, "S" : Brunnhold , "O" : None }
        Sangrun.exits = {"N" : Verdenfall, "E" : None, "S" :Ravenglade  , "O" : Mireval}
        Eldregrove.exits = {"N" : Brunnhold, "E" : None, "S" : None  , "O" : None}
        Stonebridge.exits = {"N" : Mireval, "E" : None, "S" : Dornhollow  , "O" : None}
        # Blackmere : passage à sens unique. On peut y aller depuis Brunnhold mais pas revenir en arrière.
        Blackmere.exits = {"N" : Grisepierre, "E" : None, "S" : None  , "O" : Val_Cendré}
        Grisepierre.exits = {"N" : None, "E" : None, "S" : Blackmere  , "O" : Ravenglade}
        Val_Cendré.exits = {"N" : Ravenglade, "E" : Blackmere, "S" : None  , "O" : Dornhollow}
        Ravenglade.exits = {"N" : Sangrun, "E" : Grisepierre, "S" : Val_Cendré  , "O" : None}
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Eldregrove

        #Setup item
        épée = Item("épée", "Épée des Ténèbres", 2)
        Masque_anti_brume = Item("masque", "Masque anti-brume", 1)
        filet = Item("filet", "Filet de pêche renforcé", 3) 


        #Setup item location
        Brunnhold.inventory["épée"] = épée
        Mireval.inventory["masque"] = Masque_anti_brume
        Blackmere.inventory["filet"] = filet


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
        
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()