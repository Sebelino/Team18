import GestureHandler
import ProfileManager
import CommandHandler
import Gesture


def getListOfMappings():
    ProfileManager.getMappings()

#On touch events
def on_touch_down(self, touch):
    g = GestureHandler.on_touch_down(touch)
    #TODO
    '''
    if g == None:
        pass
    else:
        getListOfMappings().[sla upp gesten och returnera kommando]
    '''
    
def on_touch_move(self, touch):
    g = GestureHandler.on_touch_move(touch)

def on_touch_up(self, touch):
    g = GestureHandler.on_touch_up(touch)

#command = ProfileManager.getCommand(gesture)
#CommandHandler.execute(command)

# For databasen
def getListOfMappings():
    return ProfileManager.getMappings()

def getListOfGestures():
    return ProfileManager.getGestures()

def getListOfCommands():
    return ProfileManager.getCommands()
