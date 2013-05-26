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
def getGestures(): return db.query("SELECT * FROM gestures")
def getCommands(): return db.query("SELECT * FROM commands")
def getCurrentGestures():
    return filter(lambda r: r[0] != u'(No gesture)',getGestures())
def getCurrentCommands():
    return filter(lambda r: r[0] != u'(No macro)',getCommands())

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
def createMapping():
    db.insertMapping(getCurrentProfile(),'(No gesture)','(No macro)')
def removeMapping(gesturename): db.removeMapping(getCurrentProfile(),gesturename)
def editMapping(oldGesture,newGesture,newCommand):
    if newGesture:
        db.updateGesture(oldGesture,newGesture)
    if newCommand:
        db.updateCommand(oldGesture,newCommand)
def editCommand(oldName,name,description,script):
    db.updateMulti("commands",("name","description","script"),("'%s'"% name,"'%s'"%
                description,"'%s'"% script),"name = '%s'"% oldName)
def createGesture(name,description,representation): db.insertGesture(name,description,representation)
def createCommand(): db.insert("commands",("Untitled macro","",""))
def removeGesture(name):
    if name == "(No gesture)":
        print "Sorry, that gesture is special. Get your filthy hand off of it!"
    else:
        db.removeGesture(name)
