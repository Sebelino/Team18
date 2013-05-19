import Command
import Gesture as OwnGesture
import Profile
from kivy.gesture import Gesture, GestureDatabase
import DatabaseAdapter as db
from sqlite3 import IntegrityError

gdb = GestureDatabase()

currentProfile = 'Sebbes profil'

kivygestures = dict()
for row in db.getProfileGestures(currentProfile):
    kivygestures.update({row[2]:row[0]})
    gest = gdb.str_to_gesture(row[2].encode("ascii"))
    gdb.add_gesture(gest)
print "profilegestures="+str(db.getProfileGestures(currentProfile))

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

def getGestures(): return db.getGestures()
def getCommands(): return db.getCommands()
def getMappings(): return db.getMappings()
def getProfiles(): return [x[0] for x in db.getProfiles()]
def createProfile(profilename): db.createProfile(profilename)
def removeProfile(profilename): db.removeProfile(profilename)
def renameProfile(old,new): db.renameProfile(old,new)
def removeMacro(name): db.removeMacro(name)
def createMapping(gesturename,commandname): db.insertMapping(currentProfile,gesturename,commandname)
