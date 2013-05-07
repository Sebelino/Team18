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
    c = conn.cursor()
    questionmarks = "?"
    print "UPDATE %s SET %s=%s WHERE %s"% (tablename,attribute,newValue,condition)
    c.execute("UPDATE %s SET %s=%s WHERE %s"% (tablename,attribute,newValue,condition))
    conn.commit()
    conn.close()
    return 'Update successful.'

# Deletes the rows satisfying the condition.
def delete(tablename,condition):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM %s WHERE %s"% (tablename,condition))
    conn.commit()
    conn.close()
    return 'Deletion successful.'

# Returns the rows satisfying the condition.
def select(c,condition,columns,table):
    if len(condition) == 0:
        c.execute("SELECT %s FROM %s"% (columns,table))
    else:
        print("SELECT %s FROM %s WHERE %s"% (columns,table,condition))
        c.execute("SELECT %s FROM %s WHERE %s"% (columns,table,condition))
    return c.fetchall()

# Executes the query and returns the results, if any.
def query(query):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result

database = '../resources/profiles.db'

def getGestures():
    return query("SELECT * FROM gestures")

def getProfileGestures(profilename):
    return query("SELECT gesturename,description,representation FROM gestures,profiles WHERE\
        gestures.name = gesturename AND profiles.name = '%s'"% profilename)

def getCommands():
    return query("SELECT * FROM commands")

def getCommand(gesturename):
    return query("SELECT commands.name,commands.description,commands.script FROM\
        profiles,commands WHERE profiles.commandname = commands.name AND\
        gesturename = '%s' AND profiles.name='Sebbes profil'"% gesturename)[0]

def getScript(gesturename):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = select(c,"profiles.commandname = commands.name AND gesturename = '%s' AND profiles.name='Sebbes profil'"% gesturename,"script","profiles,commands")
    conn.commit()
    conn.close()
    print result
    print gesturename
    return result[0][0]

def getMappings():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = select(c,"","gesturename,commandname","profiles")
    conn.commit()
    conn.close()
    return result

def getProfiles():
    return query("SELECT name FROM profiles")

def createProfile(profilename):
    (somegesture,somecommand) = query("SELECT gesturename,commandname FROM profiles")[0]
    insert("profiles",(profilename,somegesture,somecommand))

def removeProfile(profilename):
    delete("profiles","name = '%s'"% profilename)

def renameProfile(old,new):
    update("profiles","name","'%s'"% new,"name = '%s'"% old)

