import Command
import Gesture as OwnGesture
import Profile
from kivy.gesture import Gesture, GestureDatabase
import DatabaseAdapter as db

gdb = GestureDatabase()

currentProfile = 'Sebbes profil'

kivygestures = dict()
for row in db.getProfileGestures(currentProfile):
    kivygestures.update({row[2]:row[0]})
    gest = gdb.str_to_gesture(row[2].encode("ascii"))
    gdb.add_gesture(gest)
print "profilegestures="+str(db.getProfileGestures(currentProfile))

# add pre-recorded gestures to database

karta = {"s" : Command.Command("presskey s")}

#currentProfile = Profile.Profile()
#currentProfile.addMapping(OwnGesture.Gesture(gdb.gesture_to_str(s)),Command.Command("presskey s"))

def getCommand(gesture):
#    return Command.Command("presskey s")
    g = gdb.str_to_gesture(gesture.toString())
    #identifiedGesture = gdb.find(g, minscore=0.90)
    identifiedGesture = None
    current_max = 0.7 # Minimum score
    for gi in [gdb.str_to_gesture(st) for st in kivygestures.keys()]:
        if(g.get_score(gi) > current_max):
            current_max = g.get_score(gi)
            identifiedGesture = gi

    print "current_max="+str(current_max)
    if identifiedGesture != None:
        strang = gdb.gesture_to_str(identifiedGesture)
        name = kivygestures[strang]
        script = db.getScript(name)
        return Command.Command(script)
    print("NOP")
    return Command.Command("nop")
    #return currentProfile.get(OwnGesture.Gesture(gdb.gesture_to_str(identifiedGesture)))

def getGestures(): return db.getGestures()
def getCommands(): return db.getCommands()
def getMappings(): return db.getMappings()
def getProfiles(): return [x[0] for x in db.getProfiles()]
