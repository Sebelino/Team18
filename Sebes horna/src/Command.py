class Command:
    def __init__(self,script):
        self.name = "(Unnamed)"
        self.description = "(No description)"
        self.script = script

    def getScript(self):
        return self.script
