import shutil
import sqlite3
import os
import sys

def leaf(path):
    return path.split('/')[-1]

def parent(path):
    return '/'.join(path.split('/')[:-1])

def printTable_depr(table):
    print('\n'.join(str(x) for x in table))

def tableToString(table):
    max_char_lengths = [max(map(lambda x:len(str(x)),c)) for c in zip(*table)]
    padding = 2
    tableString = "Gestures\n"
    tableString += "-------"
    for row in table:
        tableString += "\n"
        for pair in zip(row,max_char_lengths):
            tableString += str(pair[0])
            for _ in range(pair[1]-len(str(pair[0]))+padding):
                tableString += " "
    return tableString

# Inserts the row into the table.
def insert(tablename,args):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    questionmarks = "?"
    for _ in range(1,len(args)):
        questionmarks += ",?"
    c.execute("INSERT INTO %s VALUES (%s)"% (tablename,questionmarks),args)
    conn.commit()
    conn.close()
    return 'Insertion successful.'

# Alters the table.
def update(tablename,attribute,newValue,condition):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    c.execute("UPDATE %s SET %s=%s WHERE %s"% (tablename,attribute,newValue,condition))
    conn.commit()
    conn.close()
    return 'Update successful.'

# Alters the table.
def updateMulti(tablename,attributes,newValues,condition):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    queryString = "UPDATE %s SET "% tablename
    for (a,v) in zip(attributes,newValues):
        queryString += "%s = %s, "% (a,v)
    queryString = queryString[0:-2]
    queryString += " WHERE %s"% condition
    print queryString
    c.execute(queryString)
    conn.commit()
    conn.close()
    return 'Update successful.'

# Deletes the rows satisfying the condition.
def delete(tablename,condition):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    c.execute("DELETE FROM %s WHERE %s"% (tablename,condition))
    conn.commit()
    conn.close()
    return 'Deletion successful.'

# Executes the query and returns the results, if any.
def query(query):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result

database = '../resources/profiles.db'

def getCommand(gesturename):
    return query("SELECT commands.name,commands.description,commands.script FROM\
        profiles,commands WHERE profiles.commandname = commands.name AND\
        gesturename = '%s' AND profiles.name='Sebbes profil'"% gesturename)[0]

def getScript(gesturename):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys=ON")
    c = conn.cursor()
    result = select(c,"profiles.commandname = commands.name AND gesturename = '%s' AND profiles.name='Sebbes profil'"% gesturename,"script","profiles,commands")
    conn.commit()
    conn.close()
    print result
    print gesturename
    return result[0][0]

def getMappings(): return query("SELECT gesturename,commandname FROM profiles WHERE\
        name=(SELECT name FROM activeprofile)")

def getProfiles():
    return query("SELECT name FROM profiles")

def createProfile(profilename):
    try:
        insertMapping(profilename,"(No gesture)","(No macro)")
    except sqlite3.IntegrityError as err:
        print 'Sorry, a profile with the name "%s" already exists.'% profilename

def removeProfile(profilename):
    try:
        if int(len(set([r[0] for r in query("SELECT name FROM profiles")]))) <= 1:
            raise sqlite3.IntegrityError
        delete("profiles","name = '%s'"% profilename)
    except sqlite3.IntegrityError as err:
        print "Sorry, there has to be at least one profile available."

def renameProfile(old,new):
    try:
        if query("SELECT name from profiles WHERE name = '%s'"% new):
            raise sqlite3.IntegrityError
        update("profiles","name","'%s'"% new,"name = '%s'"% old)
    except sqlite3.IntegrityError as err:
        print 'Sorry, a profile with the name "%s" already exists.'% new

def removeMacro(macroname):
    try:
        delete("commands","name = '%s'"% macroname)
    except sqlite3.IntegrityError as err:
        print 'Sorry, some other profile uses that macro.'

def insertMapping(profile,gesture,command):
    try:
        print "INSERTING MAPPING %s: %s->%s"% (profile,gesture,command)
        insert("profiles",(profile,gesture,command))
    except sqlite3.IntegrityError as err:
        print "Sorry, your insertion violates the functional dependency"
        print "profile,gesture -> macro."

def removeMapping(profile,gesture):
    try:
        if int(len(set([r[0] for r in query("SELECT gesturename FROM profiles,activeprofile WHERE profiles.name = activeprofile.name")]))) <= 1:
            raise sqlite3.IntegrityError
        delete("profiles","name = '%s' AND gesturename = '%s'"% (profile,gesture))
    except sqlite3.IntegrityError as err:
        print "Sorry, there has to be at least one mapping available."

def insertGesture(gesture,description,representation):
    insert("gestures",(gesture,description,representation))

def removeGesture(name): delete("gestures","name = '%s'"% name)

def getCurrentProfile(): return query("SELECT name FROM activeprofile")
def setCurrentProfile(name): update("activeprofile","name","'%s'"% name,"1=1")

def updateGesture(name,newname):
    try:
        update("profiles","gesturename","'%s'"% newname,"gesturename = '%s' AND profiles.name = (SELECT name from activeprofile)"% name)
    except sqlite3.IntegrityError as err:
        print "Sorry, your update violates the functional dependency"
        print "profile,gesture -> macro."
def updateCommand(name,newname):
    update("profiles","commandname","'%s'"% newname,"gesturename = '%s' AND profiles.name = (SELECT name from activeprofile)"% name)
