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
    tableString =  "Gestures\n"
    tableString += "--------"
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
