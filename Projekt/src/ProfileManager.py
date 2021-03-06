# -*- coding: utf-8 -*-
import Command
import Gesture as OwnGesture
import Profile
from kivy.gesture import Gesture, GestureDatabase
import DatabaseAdapter as db
from sqlite3 import IntegrityError

error = None

def getCurrentProfile():
    return db.query("SELECT name FROM activeprofile")[0][0]

def setCurrentProfile(name):
    db.update("activeprofile","name","'%s'"% name,"1=1")

def getGestures(): return db.query("SELECT * FROM gestures ORDER BY LOWER(name)")

def getDefaultGestures(): return [r[0] for r in db.query("SELECT name FROM defaultgestures ORDER BY LOWER(name)")]

def getCommands(): return db.query("SELECT * FROM commands ORDER BY LOWER(name)")

def getCustomGestures():
    return filter(lambda r: r[0] not in getDefaultGestures(),getGestures())

def getCurrentGestures():
    gestures = db.query("SELECT gestures.name,gestures.description,gestures.representation\
            FROM gestures,profiles,activeprofile WHERE profiles.name =\
            activeprofile.name AND gestures.name = gesturename ORDER BY LOWER(gesturename)")
    return gestures

def getCustomCommands():
    return filter(lambda r: r[0] != u'(No macro)',getCommands())

def getCurrentCommands():
    commands = db.query("SELECT commands.name,commands.description,commands.script\
            FROM commands,profiles,activeprofile WHERE profiles.name =\
            activeprofile.name AND commands.name = commandname ORDER BY LOWER(commandname)")
    return commands

gdb = GestureDatabase()

kivygestures = dict()
for [name,description,representation] in getCurrentGestures():
    if len(representation) < 20:    # Fulhack för att känna igen multitouch.
        continue
    kivygestures.update({representation:name})
    gest = gdb.str_to_gesture(representation.encode("ascii"))
    gdb.add_gesture(gest)

def getCommand(gesture):
    if gesture.multitouch:
        return getMultitouchedCommand(gesture)
    g = gdb.str_to_gesture(gesture.toString())
    identifiedGesture = None
    current_max = 0.7 # Minimum score
    for gi in [gdb.str_to_gesture(st) for st in kivygestures.keys()]:
        if(g.get_score(gi) > current_max):
            current_max = g.get_score(gi)
            identifiedGesture = gi

    nop = Command.Command("No operation","Does nothing","nop")
    if identifiedGesture != None:
        strang = gdb.gesture_to_str(identifiedGesture)
        gesturename = kivygestures[strang]
        table = db.query("SELECT\
                commands.name,commands.description,commands.script FROM\
                profiles,commands WHERE profiles.commandname = commands.name AND\
                gesturename = '%s' AND profiles.name='%s'"% (gesturename,getCurrentProfile()))
        if not table:
            return nop
        (name,description,script) = table[0]
        return Command.Command(name,description,script)
    print("That gesture was not recognized.")
    return nop

def getMultitouchedCommand(gesture):
    table = db.query("SELECT name,description,script FROM commands WHERE name IN\
            (SELECT commandname FROM profiles,activeprofile WHERE profiles.name = activeprofile.name AND\
             gesturename=(SELECT name FROM gestures WHERE representation='%s'))"% gesture.stringRepresentation)
    if table:
        return Command.Command(table[0][0],table[0][1],table[0][2])
    return Command.Command("No operation","Does nothing.","nop")

def getMappings():
    return db.query("SELECT gesturename,commandname FROM profiles WHERE\
        name=(SELECT name FROM activeprofile) ORDER BY LOWER(gesturename)")

def getProfiles():
    profiles = list(set([x[0] for x in db.query("SELECT name from profiles")]))
    profiles.sort()
    return profiles
def createProfile(profilename):
    global error
    try:
        db.insert('profiles',(profilename,'(No gesture)','(No macro)'))
        setCurrentProfile(profilename)
    except IntegrityError as err:
        error = 'A profile with the name "%s" already exists.'% profilename

def removeProfile(profilename):
    global error
    profilename = profilename.strip()
    try:
        if not profilename:
            error = 'The name cannot consist of whitespace only.'
            return
        if int(len(set([r[0] for r in db.query("SELECT name FROM profiles")]))) <= 1:
            error = "There has to be at least one profile available."
            return
        db.delete("profiles","name = '%s'"% profilename)
        anyOtherProfile = list(getProfiles())[0]
        setCurrentProfile(anyOtherProfile)
    except IntegrityError as err:
        error = 'A database integrity error was encountered: %s'% err

def renameProfile(old,new):
    global error
    new = new.strip()
    try:
        if db.query("SELECT name from profiles WHERE name = '%s'"% new):
            error = 'A profile with the name "%s" already exists.'% new
            return
        if not new:
            error = 'The name cannot consist of whitespace only.'
            return
        db.update("profiles","name","'%s'"% new,"name = '%s'"% old)
        setCurrentProfile(new)
    except IntegrityError as err:
        error = 'A database integrity error was encountered: %s'% err
        
def removeMacro(macroname):
    global error
    try:
        table = db.query("SELECT name,commandname FROM profiles WHERE commandname = '%s'"% macroname)
        if table:
            error = 'Profile "%s" is using that macro.'% table[0][0]
            return
        db.delete("commands","name = '%s'"% macroname)
    except IntegrityError as err:
        error = 'A database integrity error was encountered: %s'% err

def createMapping():
    global error
    availableGestures = [r[0] for r in db.query("SELECT name from gestures WHERE name NOT IN\
            (SELECT profiles.gesturename FROM profiles,activeprofile WHERE profiles.name =\
             activeprofile.name)")]
    if not availableGestures:
        error = "All available gestures are already mapped in this profile."
        return
    db.insert("profiles",(getCurrentProfile(),availableGestures[0],'(No macro)'))

def removeMapping(gesture):
    global error
    profile = getCurrentProfile()
    try:
        if int(len(set([r[0] for r in db.query("SELECT gesturename FROM profiles,activeprofile\
                            WHERE profiles.name = activeprofile.name")]))) <= 1:
            error = "There has to be at least one mapping available."
            return
        db.delete("profiles","name = '%s' AND gesturename = '%s'"% (profile,gesture))
    except IntegrityError:
        error = 'A database integrity error was encountered: %s'% err
        
def editMapping(oldGesture,newGesture,newCommand):
    global error
    if newGesture:
        try:
            db.update("profiles","gesturename","'%s'"% newGesture,
                    "gesturename = '%s' AND profiles.name = (SELECT name from activeprofile)"%
                    oldGesture)
        except IntegrityError as err:
            error = "That name is already used by some mapping."
    if newCommand:
        db.update("profiles","commandname","'%s'"% newCommand,
                "gesturename = '%s' AND profiles.name = (SELECT name from activeprofile)"%
                oldGesture)

def editCommand(oldName,name,description,script):
    global error
    name = name.strip()
    try:
        if not name:
            error = 'The name cannot consist of whitespace only.'
            return
        if oldName != name and db.query("SELECT name FROM commands WHERE name = '%s'"% name):
            error = 'A macro with that name already exists.'
            return
        table = db.query("SELECT profiles.name,commandname FROM profiles,activeprofile WHERE\
                commandname = '%s' AND profiles.name <> activeprofile.name"% oldName)
        if table:
            error = 'Profile "%s" is using that macro.'% table[0][0]
            return
        db.updateMulti("commands",("name","description","script"),("'%s'"% name,"'%s'"%
                    description,"'%s'"% script),"name = '%s'"% oldName)
    except IntegrityError as err:
        error = 'A database integrity error was encountered: %s'% err

def createGesture(name,description,representation):
    global error
    try:
        if not representation:
            error = 'You need to draw a gesture.'
            return
        db.insert("gestures",(name,description,representation))
    except IntegrityError:
        error = "There already exists a gesture with that name."

def createCommand():
    global error
    usedNumbers = [r[0][len('Untitled macro '):] for r in db.query("SELECT name FROM commands WHERE name LIKE 'Untitled macro %'")]
    usedNumbers = filter(lambda x: x.isdigit(),usedNumbers)
    usedNumbers = [int(n) for n in usedNumbers]
    for i in range(1,len(usedNumbers)+2):
        if not i in usedNumbers:
            db.insert("commands",("Untitled macro "+str(i),"",""))
            return

def removeGesture(name):
    global error
    try:
        table = db.query("SELECT name,gesturename FROM profiles WHERE gesturename = '%s'"% name)
        if table:
            error = 'Profile "%s" is using that gesture.'% table[0][0]
            return
        db.delete("gestures","name = '%s'"% name)
    except IntegrityError as err:
        error = 'A database integrity error was encountered: %s'% err

def popError():
    global error
    temp = error
    error = None
    return temp

