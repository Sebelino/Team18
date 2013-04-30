import Command
import Gesture as OwnGesture
import Profile
from kivy.gesture import Gesture, GestureDatabase
import DatabaseAdapter as db

gdb = GestureDatabase()

s = \
gdb.str_to_gesture('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')

kivygestures = dict()
for row in db.getGestures():
    kivygestures.update({row[2]:row[0]})
    gest = gdb.str_to_gesture(row[2].encode("ascii"))
    gdb.add_gesture(gest)

# add pre-recorded gestures to database

karta = {"s" : Command.Command("presskey s")}

#currentProfile = Profile.Profile()
#currentProfile.addMapping(OwnGesture.Gesture(gdb.gesture_to_str(s)),Command.Command("presskey s"))

def getCommand(gesture):
#    return Command.Command("presskey s")
    g = gdb.str_to_gesture(gesture.toString())
    print "i:", kivygestures.keys()[1]
    #print "s:", g.get_score(gdb.str_to_gesture(kivygestures.keys()[0]))
    #identifiedGesture = gdb.find(g, minscore=0.90)
    identifiedGesture = None
    current_max = 0
    for gi in [gdb.str_to_gesture(st) for st in kivygestures.keys()]:
        if(g.get_score(gi) > current_max):
            current_max = g.get_score(gi)
            identifiedGesture = gi

    if identifiedGesture != None:
        strang = gdb.gesture_to_str(identifiedGesture)
        name = kivygestures[strang]
        print("name"+name)
        script = db.getScript(name)
        return Command.Command(script)
    print("NOP")
    return Command.Command("nop")
    #return currentProfile.get(OwnGesture.Gesture(gdb.gesture_to_str(identifiedGesture)))

def getMappings():
    return db.getMappings()
