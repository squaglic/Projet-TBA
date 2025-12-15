# command.py
# Description: The Command class.

class Command:
    def __init__(self, word, help_text, action, number_of_parameters):
        self.word = word
        self.help_text = help_text
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    def __str__(self):
        return f"{self.word}{self.help_text}"