class Command:
    def __init__(self,name,description,script):
        self.name = name
        self.description = description
        self.script = script

    def getScript(self):
        return self.script
