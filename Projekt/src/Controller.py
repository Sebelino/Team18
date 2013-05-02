import GestureHandler
import ProfileManager
import CommandHandler
import Gesture


def getListOfMappings():
    ProfileManager.getMappings()

def signalCommand(g):
    if g == None:
        pass
    else:
        mappings = getListOfMappings()
        d = dict(mappings)
        c = d[g]
        CommandHandler.execute(c)

#On touch events
def on_touch_down(self, touch):
    g = GestureHandler.on_touch_down(touch)
    signalCommand(g)

def on_touch_move(self, touch):
    g = GestureHandler.on_touch_move(touch)
    signalCommand(g)

def on_touch_up(self, touch):
    g = GestureHandler.on_touch_up(touch)
    signalCommand(g)

#command = ProfileManager.getCommand(gesture)
#CommandHandler.execute(command)

# For databasen
def getListOfMappings():
    return ProfileManager.getMappings()

def getListOfGestures():
    return ProfileManager.getGestures()

def getListOfCommands():
    return ProfileManager.getCommands()



