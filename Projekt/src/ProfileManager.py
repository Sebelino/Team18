import Command
import Gesture as OwnGesture
import Profile
from kivy.gesture import Gesture, GestureDatabase
import DatabaseAdapter as db
from sqlite3 import IntegrityError

def getCurrentProfile(): return db.getCurrentProfile()[0][0]
def setCurrentProfile(name):
    print "SETTING PROFILE TO %s!"% name
    db.setCurrentProfile(name)
def getCurrentGestures():
    return set(db.query("SELECT gestures.name,gestures.description,gestures.representation FROM\
            gestures,profiles,activeprofile WHERE activeprofile.name=profiles.name AND\
            gestures.name=profiles.gesturename"))

gdb = GestureDatabase()

kivygestures = dict()
for row in getCurrentGestures():
    kivygestures.update({row[2]:row[0]})
    gest = gdb.str_to_gesture(row[2].encode("ascii"))
    gdb.add_gesture(gest)

def getCommand(gesture):
    g = gdb.str_to_gesture(gesture.toString())
    identifiedGesture = None
    current_max = 0.7 # Minimum score
    for gi in [gdb.str_to_gesture(st) for st in kivygestures.keys()]:
        if(g.get_score(gi) > current_max):
            current_max = g.get_score(gi)
            identifiedGesture = gi

    print "current_max="+str(current_max)
    if identifiedGesture != None:
        strang = gdb.gesture_to_str(identifiedGesture)
        gesturename = kivygestures[strang]
        (name,description,script) = db.getCommand(gesturename)
        return Command.Command(name,description,script)
    print("NOP")
    return Command.Command("No operation","Does nothing.","nop")

def getGestures(): return db.query("SELECT * FROM gestures")
def getCurrentMacros():
    return set(db.query("SELECT commands.name,commands.description,commands.script FROM commands,profiles,activeprofile WHERE\
            activeprofile.name=profiles.name AND commands.name=profiles.commandname"))
def getCommands(): return db.query("SELECT * FROM commands")
def getMappings(): return db.getMappings()
def getProfiles(): return set([x[0] for x in db.getProfiles()])
def createProfile(profilename):
    db.createProfile(profilename)
    setCurrentProfile(profilename)
def removeProfile(profilename):
    db.removeProfile(profilename)
    anyOtherProfile = list(getProfiles())[0]
    setCurrentProfile(anyOtherProfile)
def renameProfile(old,new): db.renameProfile(old,new)
def removeMacro(name): db.removeMacro(name)
def createMapping(gesturename,commandname): db.insertMapping(getCurrentProfile(),gesturename,commandname)
def removeMapping(gesturename): db.removeMapping(getCurrentProfile(),gesturename)
def editMapping(oldGesture,newGesture,newCommand):
    if newGesture:
        db.updateGesture(oldGesture,newGesture)
    if newCommand:
        db.updateCommand(oldGesture,newCommand)
def createGesture(name,description,representation): db.insertGesture(name,description,representation)
def removeGesture(name):
    if name == "(No gesture)":
        print "Sorry, that gesture is special. Get your filthy hand off of it!"
    else:
        db.removeGesture(name)
