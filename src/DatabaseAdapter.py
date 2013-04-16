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
def insert(c,args):
    row = [args[0],args[1]]
    c.execute("INSERT INTO gestures VALUES (?,?)",row)
    return 'Insertion successful.'

# Deletes the rows satisfying the condition.
def delete(c,condition):
    c.execute("DELETE FROM gestures WHERE %s"% condition[0])
    return 'Deletion successful.'

# Returns the rows satisfying the condition.
def select(c,condition,columns,table):
    if len(condition) == 0:
        c.execute("SELECT %s FROM %s"% (columns,table))
    else:
        c.execute("SELECT %s FROM %s WHERE %s"% (columns,table,condition[0]))
    return c.fetchall()

database = '../resources/profiles.db'

def getGestures():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = select(c,"","*","gestures")
    conn.commit()
    conn.close()
    return result

def getScript(gesturename):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = select(c,"profiles.commandname = commands.name AND gesturename = %s AND profile.name='Sebbes profil'"% gesturename,"script","profiles,commands")
    conn.commit()
    conn.close()
    return result[0][0]

def getMappings():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    result = select(c,"","gesturename,commandname","profiles")
    conn.commit()
    conn.close()
    return result
