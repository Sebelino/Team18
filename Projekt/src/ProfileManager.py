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
def getGestures(): return db.query("SELECT * FROM gestures ORDER BY LOWER(name)")
def getCommands(): return db.query("SELECT * FROM commands ORDER BY LOWER(name)")
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
def getProfiles():
    profiles = list(set([x[0] for x in db.query("SELECT name from profiles")]))
    profiles.sort()
    return profiles
def createProfile(profilename):
    try:
        insertMapping(profilename,"(No gesture)","(No macro)")
        setCurrentProfile(profilename)
    except IntegrityError as err:
        print 'Sorry, a profile with the name "%s" already exists.'% profilename
def removeProfile(profilename):
    db.removeProfile(profilename)
    anyOtherProfile = list(getProfiles())[0]
    setCurrentProfile(anyOtherProfile)
def renameProfile(old,new):
    try:
        if db.query("SELECT name from profiles WHERE name = '%s'"% new):
            raise IntegrityError
        db.update("profiles","name","'%s'"% new,"name = '%s'"% old)
        setCurrentProfile(new)
    except IntegrityError as err:
        print 'Sorry, a profile with the name "%s" already exists.'% new
def removeMacro(name): db.removeMacro(name)
def createMapping():
    availableGestures = [r[0] for r in db.query("SELECT name from gestures WHERE name NOT IN\
            (SELECT profiles.gesturename FROM profiles,activeprofile WHERE profiles.name =\
             activeprofile.name)")]
    if not availableGestures:
        print "Sorry, all gestures are occupied."
        return
    db.insert("profiles",(getCurrentProfile(),availableGestures[0],'(No macro)'))
def removeMapping(gesturename): db.removeMapping(getCurrentProfile(),gesturename)
def editMapping(oldGesture,newGesture,newCommand):
    if newGesture:
        db.updateGesture(oldGesture,newGesture)
    if newCommand:
        db.updateCommand(oldGesture,newCommand)
def editCommand(oldName,name,description,script):
    try:
        db.updateMulti("commands",("name","description","script"),("'%s'"% name,"'%s'"%
                    description,"'%s'"% script),"name = '%s'"% oldName)
    except IntegrityError:
        print "Sorry, you can't edit that. Either you are trying to rename it to a macro that\
already exists, or you are trying to edit a macro used by someone else."
def createGesture(name,description,representation):
    try:
        db.insertGesture(name,description,representation)
    except IntegrityError:
        print "Sorry, there already exists a gesture with that name."
def createCommand():
    usedNumbers = [r[0][len('Untitled macro '):] for r in db.query("SELECT name FROM commands WHERE name LIKE 'Untitled macro %'")]
    usedNumbers = filter(lambda x: x.isdigit(),usedNumbers)
    usedNumbers = [int(n) for n in usedNumbers]
    for i in range(1,len(usedNumbers)+2):
        if not i in usedNumbers:
            db.insert("commands",("Untitled macro "+str(i),"",""))
            return
def removeGesture(name):
    if name == "(No gesture)":
        print "Sorry, that gesture is special. Get your filthy hand off of it!"
    else:
        db.removeGesture(name)
