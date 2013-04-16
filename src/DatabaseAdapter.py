import shutil
import sqlite3
import os
import sys

database = '../resources/profiles.db'

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
def select(c,condition):
    if len(condition) == 0:
        c.execute("SELECT * FROM gestures")
    else:
        c.execute("SELECT * FROM gestures WHERE %s"% condition[0])
    return tableToString(c.fetchall())

if len(sys.argv) <= 1:
    print("Please apply some parameters.")
    sys.exit()

conn = sqlite3.connect(database)
c = conn.cursor()

options = {
    '-i' : insert,
    '-d' : delete,
    '-s' : select
}

option = sys.argv[1]

result = options[option](c,sys.argv[2:])
print(result)

conn.commit()
conn.close()
