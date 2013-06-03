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


# For the database
def getListOfMappings(): return ProfileManager.getMappings()
def getListOfGestures(): return ProfileManager.getGestures()
def getCustomGestures(): return ProfileManager.getCustomGestures()
def getListOfMacros(): return ProfileManager.getCommands()
def getCustomMacros(): return ProfileManager.getCustomCommands()
def getListOfProfiles(): return ProfileManager.getProfiles()
def getCurrentProfile(): return ProfileManager.getCurrentProfile()
def setCurrentProfile(newProfile): ProfileManager.setCurrentProfile(newProfile.replace("'","''"))
def createProfile(profilename): ProfileManager.createProfile(profilename.replace("'","''"))
def removeProfile(profilename): ProfileManager.removeProfile(profilename.replace("'","''"))
def setProfile(profilename): ProfileManager.setCurrentProfile(profilename.replace("'","''"))
def renameProfile(old,new): ProfileManager.renameProfile(old.replace("'","''"),new.replace("'","''"))
def removeMacro(name): ProfileManager.removeMacro(name.replace("'","''"))
def createMapping(): ProfileManager.createMapping()
def removeMapping(gesturename): ProfileManager.removeMapping(gesturename.replace("'","''"))
def editMapping(oldGesture,newGesture,newMacro):
    ProfileManager.editMapping(oldGesture.replace("'","''"),newGesture.replace("'","''"),newMacro.replace("'","''"))
def editMacro(oldMacro,newMacro,description,script): ProfileManager.editCommand(oldMacro.replace("'","''"),newMacro.replace("'","''"),description.replace("'","''"),script.replace("'","''"))
def createGesture(name,description,representation): ProfileManager.createGesture(name.replace("'","''"),description.replace("'","''"),representation.replace("'","''"))
def createMacro(): ProfileManager.createCommand()
def removeGesture(name): ProfileManager.removeGesture(name.replace("'","''"))
def popError(): return ProfileManager.popError()


