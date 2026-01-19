# Description: Game class

# Debug mode
DEBUG = False

# Import modules


from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self, player_name=None):
        

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
        

        #Quests
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)
        use = Command("use", " <objet> : utiliser un objet de votre inventaire", Actions.use, 1)
        self.commands["use"] = use
    
        
        # Setup rooms

        Eldregrove = Room("Eldregrove","une forêt ancienne où les arbres semblent observer les voyageurs, et où la magie sauvage imprègne chaque souffle de vent.", "Eldregrove.png")
        self.rooms.append(Eldregrove)
        Verdenfall = Room("Verdenfall", "une ancienne couronne du royaume, ce château en ruines résonne encore des murmures d'un pouvoir oublié.", "Verdenfall.png")
        self.rooms.append(Verdenfall)
        Brunnhold = Room("Brunnhold", "un village partiellement ravagé, dont les habitants vivent dans une méfiance constante envers tout ce qui leur est étranger.", "Brunnhold.png")
        self.rooms.append(Brunnhold)
        Mireval = Room("Mireval", "un Hameau noyé dans une brume perpétuelle, marqué par une étrange épidémie que nul ne parvient à comprendre.", "Mireval.png")
        self.rooms.append(Mireval)
        Stonebridge = Room("Stonebridge", "une Forteresse-village robuste, dernier rempart organisé de l'humanité contre les ténèbres grandissantes.", "Stonebridge.png")
        self.rooms.append(Stonebridge)
        Dornhollow = Room("Dornhollow", "un village englouti par les marécages, où les habitants jurent entendre des voix sous la boue.", "Dornhollow.png")
        self.rooms.append(Dornhollow)
        Blackmere = Room("Blackmere", "un Hameau lacustre dont les pêcheurs disparaissent dans les eaux sombres.", "Blackmere.png")
        self.rooms.append(Blackmere)
        Grisepierre = Room("Grisepierre", "un Hameau minier hanté par un minerai étrange qui semble respirer.", "Grisepierre.png")
        self.rooms.append(Grisepierre)
        Val_Cendré = Room("Val-Cendré", "un village couvert d'une cendre éternelle, marqué par un incendie surnaturel.", "Val_Cendre.png")
        self.rooms.append(Val_Cendré)
        Ravenglade = Room("Ravenglade" , "un Hameau forestier envahi de corbeaux, où aucune naissance n'a eu lieu depuis des années.", "Ravenglade.png")
        self.rooms.append(Ravenglade)
        Sangrun = Room("Sangrun", "une grotte où résident les âmes tourmentées du village.", "Sangrun.png")
        self.rooms.append(Sangrun)



        #Setup pnjs
        guardian = Character("Gardien", "Un vieux gardien mystérieux", Brunnhold, ["Bienvenue voyageur, je suis le gardien de ce village.", "Attention aux ombres qui rôdent dans ces terres!"])
        Brunnhold.characters.append(guardian)
        messenger = Character("Messager", "Un messager essoufflé", Stonebridge, ["Les ténèbres avancent rapidement, nous devons rester vigilants.", "Avez-vous entendu parler de la malédiction de Mireval?", "Seul un vaillant guerrier atteindra le Château de Verdenfall."])
        Stonebridge.characters.append(messenger)


        # Create exits for rooms

        # Bloquer le passage direct entre Forest et Tower :
        # - forest.E ne mène plus à tower
        # - tower.O ne mène plus à forest
        Verdenfall.exits = {"N" : None , "E" : None, "S" : Sangrun , "O" : None }
        Brunnhold.exits = {"N" : Dornhollow, "E" : Blackmere, "S" : Eldregrove , "O" : None }
        Mireval.exits = {"N" : None, "E" : Sangrun, "S" : Stonebridge, "O" : None}
        Dornhollow.exits = {"N" : Stonebridge, "E" : Val_Cendré, "S" : Brunnhold , "O" : None }
        Sangrun.exits = {"N" : Verdenfall, "E" : None, "S" :Ravenglade  , "O" : Mireval}
        Eldregrove.exits = {"N" : Brunnhold, "E" : None, "S" : None  , "O" : None}
        Stonebridge.exits = {"N" : Mireval, "E" : None, "S" : Dornhollow  , "O" : None}
        # Blackmere : passage à sens unique. On peut y aller depuis Brunnhold mais pas revenir en arrière.
        Blackmere.exits = {"N" : Grisepierre, "E" : None, "S" : None  , "O" : None}
        Grisepierre.exits = {"N" : None, "E" : None, "S" : Blackmere  , "O" : Ravenglade}
        Val_Cendré.exits = {"N" : Ravenglade, "E" : None, "S" : None  , "O" : Dornhollow}
        Ravenglade.exits = {"N" : Sangrun, "E" : Grisepierre, "S" : Val_Cendré  , "O" : None}
        # Setup player and starting room

        if player_name is None:
            player_name = input("\nEntrez votre nom: ")
        self.player = Player(player_name)
        self.player.current_room = Eldregrove

        #Setup item
        épée = Item("épée", "Épée des Ténèbres", 2)
        Masque_anti_brume = Item("masque", "Masque anti-brume", 1)
        bouclier = Item("bouclier", "Bouclier de protection magique", 3)
        âme_mineur = Item("âme_mineur", "Âme du mineur", 1)
        âme_pêcheur = Item("âme_pêcheur", "Âme du pêcheur", 1)
        âme_seigneur = Item("âme_seigneur", "Âme du Seigneur", 2)
        poison = Item("poison", "Poison de vérité", 1)


        #Setup item location
        Brunnhold.inventory["épée"] = épée
        Mireval.inventory["masque"] = Masque_anti_brume
        Blackmere.inventory["bouclier"] = bouclier
        Grisepierre.inventory["âme_mineur"] = âme_mineur
        Blackmere.inventory["âme_pêcheur"] = âme_pêcheur
        Mireval.inventory["âme_seigneur"] = âme_seigneur
        Verdenfall.inventory["poison"] = poison

        # Setup quests
        self._setup_quests()
        


    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Initialiser la flag used_poison du joueur
        self.player.used_poison = False
        # Loop until the game is finished
        while not self.finished:
            # Vérifier les conditions de victoire et défaite
            if self.win():
                print("\n🏆 Vous avez sauvé le royaume ! Victoire !\n")
                self.finished = True
                break
            if self.loose():
                print("\n☠️  Vous avez perdu... Le poison vous a vaincu.\n")
                self.finished = True
                break
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
        
        # Déplacer tous les personnages non-joueurs après chaque commande
        self.move_characters()

    def win(self):
        """
        Check if the player has won the game.
        Win condition: All quests are completed AND the player has used poison at Verdenfall.
        
        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check if all quests are completed
        all_quests_completed = all(quest.is_completed for quest in self.player.quest_manager.quests)
        
        # Check if player has used poison at Verdenfall
        used_poison_at_verdenfall = self.player.used_poison
        
        return all_quests_completed and used_poison_at_verdenfall
    
    def loose(self):
        """
        Check if the player has lost the game.
        Loss condition: The player has used poison.
        
        Returns:
            bool: True if the player has lost, False otherwise.
        """
        return self.player.used_poison

    def _setup_quests(self):
        """Initialize all quests."""
        travel_quest = Quest(
            title="Grand Voyageur",
            description="Déplacez-vous 10 fois entre les lieux.",
            objectives=["Se déplacer 10 fois"],
            reward="Bottes de voyageur"
        )

        dark_sword_quest = Quest(
            title="Récupérer l'Épée des Ténèbres",
            description="Retrouvez et récupérez l'Épée des Ténèbres cachée quelque part dans le monde.",
            objectives=["prendre épée"],
            reward="Épée des Ténèbres"
        )

        messenger_quest = Quest(
            title="Parler avec le Messager",
            description="Allez à Stonebridge et parlez avec le Messager pour en savoir plus sur les ténèbres.",
            objectives=["parler avec Messager"],
            reward="Information précieuse"
        )

        verdenfall_quest = Quest(
            title="Atteindre Verdenfall",
            description="Trouvez votre chemin jusqu'au Château de Verdenfall, l'ancienne couronne du royaume.",
            objectives=["Visiter Château de Verdenfall"],
            reward="Accès à Verdenfall"
        )

        souls_quest = Quest(
            title="Récupérer les âmes",
            description="Collectez les trois âmes perdues dispersées dans le monde.",
            objectives=["prendre âme_mineur", "prendre âme_pêcheur", "prendre âme_seigneur"],
            reward="Pouvoir des âmes"
        )

        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(travel_quest)
        self.player.quest_manager.add_quest(dark_sword_quest)
        self.player.quest_manager.add_quest(messenger_quest)
        self.player.quest_manager.add_quest(verdenfall_quest)
        self.player.quest_manager.add_quest(souls_quest)


    def move_characters(self):
        """
        Déplace tous les personnages non-joueurs présents dans le jeu.
        Affiche un message si un personnage se déplace dans ou hors de la salle du joueur.
        """
        player_room = self.player.current_room
        
        # Parcourir toutes les salles pour trouver les personnages
        for room in self.rooms:
            # Créer une copie de la liste des personnages pour éviter les problèmes de modification pendant l'itération
            characters_in_room = list(room.characters)
            for character in characters_in_room:
                old_room = character.current_room
                # Déplacer le personnage
                moved = character.move()
                
                if moved:
                    new_room = character.current_room
                    # Retirer le personnage de l'ancienne salle
                    old_room.characters.remove(character)
                    # Ajouter le personnage à la nouvelle salle
                    new_room.characters.append(character)
                    
                    # Afficher un message si le joueur est concerné
                    if old_room == player_room:
                        print(f"\n{character.name} quitte la salle.\n")
                    elif new_room == player_room:
                        print(f"\n{character.name} entre dans la salle.\n")

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        
        print(self.player.current_room.get_long_description())




##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""


class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)  # Pass name to avoid double prompt

        # Build UI layers
        self._build_layout()

        # Initialiser la flag used_poison du joueur
        self.game.player.used_poison = False

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        
        # Vérifier les conditions de victoire et défaite
        if self.game.win():
            print("\n🏆 Vous avez sauvé le royaume ! Victoire !\n")
            self.game.finished = True
        elif self.game.loose():
            print("\n☠️  Vous avez perdu... Le poison vous a vaincu.\n")
            self.game.finished = True
        
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()
    

if __name__ == "__main__":
    main()