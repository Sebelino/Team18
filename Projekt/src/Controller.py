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
    print "DOWN!!!"
    
def on_touch_move(touch):
    g = GestureHandler.on_touch_move(touch)
    signalCommand(g)
    print "MOVE!!!!!!!!"
    
def on_touch_up(touch):
    g = GestureHandler.on_touch_up(touch)
    signalCommand(g)
    print "UP"


# For databasen
def getListOfMappings(): return ProfileManager.getMappings()
def getListOfGestures(): return ProfileManager.getGestures()
def getListOfMacros(): return ProfileManager.getCommands()
def getListOfProfiles(): return ProfileManager.getProfiles()
def getCurrentProfile(): return ProfileManager.currentProfile
def setCurrentProfile(newProfile): ProfileManager.currentProfile = newProfile
def createProfile(profilename): ProfileManager.createProfile(profilename)
def removeProfile(profilename): ProfileManager.removeProfile(profilename)
def setProfile(profilename): ProfileManager.currentProfile = profilename
def renameProfile(old,new): ProfileManager.renameProfile(old,new)



