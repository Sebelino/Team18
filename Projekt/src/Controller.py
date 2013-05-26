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


# For the database
def getListOfMappings(): return ProfileManager.getMappings()
def getListOfGestures(): return ProfileManager.getGestures()
def getCurrentGestures(): return ProfileManager.getCurrentGestures()
def getListOfMacros(): return ProfileManager.getCommands()
def getCurrentMacros(): return ProfileManager.getCurrentCommands()
def getListOfProfiles(): return ProfileManager.getProfiles()
def getCurrentProfile(): return ProfileManager.getCurrentProfile()
def setCurrentProfile(newProfile): ProfileManager.setCurrentProfile(newProfile)
def createProfile(profilename): ProfileManager.createProfile(profilename)
def removeProfile(profilename): ProfileManager.removeProfile(profilename)
def setProfile(profilename): ProfileManager.setCurrentProfile(profilename)
def renameProfile(old,new): ProfileManager.renameProfile(old,new)
def removeMacro(name): ProfileManager.removeMacro(name)
def createMapping(): ProfileManager.createMapping()
def removeMapping(gesturename): ProfileManager.removeMapping(gesturename)
def editMapping(oldGesture,newGesture,newMacro):
    ProfileManager.editMapping(oldGesture,newGesture,newMacro)
def editMacro(oldMacro,newMacro,description,script): ProfileManager.editCommand(oldMacro,newMacro,description,script)
def createGesture(name,description,representation): ProfileManager.createGesture(name,description,representation)
def createMacro(): ProfileManager.createCommand()
def removeGesture(name): ProfileManager.removeGesture(name)
def popError(): ProfileManager.popError()


