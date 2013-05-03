import GestureHandler
import ProfileManager
import CommandHandler
import Gesture
import Command

def signalCommand(g):
    print g
    if g == None:
        print "g is None\n\n\n!!!"
        pass
    else:
        c = ProfileManager.getCommand(g)
        CommandHandler.execute(c)


#On touch events
def on_touch_down(touch):
    g = GestureHandler.on_touch_down(touch)
    signalCommand(g)
    print "hi\nhi\nhi\nDOWN!!!"
    
def on_touch_move(touch):
    g = GestureHandler.on_touch_move(touch)
    signalCommand(g)
    print "hi\nhi\nhi\nMOVE!!!!!!!!"
    
def on_touch_up(touch):
    g = GestureHandler.on_touch_up(touch)
    signalCommand(g)
    print "hi\nhi\nhi\nUP"


# For databasen
def getListOfMappings(): return ProfileManager.getMappings()
def getListOfGestures(): return ProfileManager.getGestures()
def getListOfCommands(): return ProfileManager.getCommands()
def getListOfProfiles(): return ProfileManager.getProfiles()
def getCurrentProfile(): return ProfileManager.currentProfile
def setCurrentProfile(newProfile): ProfileManager.currentProfile = newProfile



