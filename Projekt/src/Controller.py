import GestureHandler
import ProfileManager
import CommandHandler
import Gesture
import Command

def signalCommand(g):
    if not g:
        pass
    else:
        c = ProfileManager.getCommand(g)
        CommandHandler.execute(c)

moveprinted = False
#On touch events
def on_touch_down(touch):
    global moveprinted
    g = GestureHandler.on_touch_down(touch)
    print "Touch down"
    signalCommand(g)

def on_touch_move(touch):
    global moveprinted
    g = GestureHandler.on_touch_move(touch)
    if not moveprinted:
        print "Touch move"
        moveprinted = True
    signalCommand(g)
    
def on_touch_up(touch):
    global moveprinted
    g = GestureHandler.on_touch_up(touch)
    print "Touch up"
    signalCommand(g)

def sanitize(param):
    if isinstance(param,basestring):
        return param.replace("'","''")
    return param


# For the database
def getListOfMappings(): return ProfileManager.getMappings()
def getListOfGestures(): return ProfileManager.getGestures()
def getCustomGestures(): return ProfileManager.getCustomGestures()
def getListOfMacros(): return ProfileManager.getCommands()
def getCustomMacros(): return ProfileManager.getCustomCommands()
def getListOfProfiles(): return ProfileManager.getProfiles()
def getCurrentProfile(): return ProfileManager.getCurrentProfile()
def setCurrentProfile(newProfile): ProfileManager.setCurrentProfile(sanitize(newProfile))
def createProfile(profilename): ProfileManager.createProfile(sanitize(profilename))
def removeProfile(profilename): ProfileManager.removeProfile(sanitize(profilename))
def setProfile(profilename): ProfileManager.setCurrentProfile(sanitize(profilename))
def renameProfile(old,new): ProfileManager.renameProfile(sanitize(old),sanitize(new))
def removeMacro(name): ProfileManager.removeMacro(sanitize(name))
def createMapping(): ProfileManager.createMapping()
def removeMapping(gesturename): ProfileManager.removeMapping(sanitize(gesturename))
def editMapping(oldGesture,newGesture,newMacro):
    ProfileManager.editMapping(sanitize(oldGesture),sanitize(newGesture),sanitize(newMacro))
def editMacro(oldMacro,newMacro,description,script):
    ProfileManager.editCommand(sanitize(oldMacro),sanitize(newMacro),sanitize(description),sanitize(script))
def createGesture(name,description,representation):
    ProfileManager.createGesture(sanitize(name),sanitize(description),sanitize(representation))
def createMacro(): ProfileManager.createCommand()
def removeGesture(name): ProfileManager.removeGesture(sanitize(name))
def popError(): return ProfileManager.popError()


