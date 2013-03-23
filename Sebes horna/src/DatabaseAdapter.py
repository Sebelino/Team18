# Module

import shutil
import sqlite3
import os

database = '../resources/profiles.db'
files = './files'

def leaf(path):
    return path.split('/')[-1]

def parent(path):
    return '/'.join(path.split('/')[:-1])

def try_making_directory(path):
    try:
        os.makedirs(path)
    except:
        pass
#        print("Directory already exists: %s"% path)

#def try_removing_dir(path):
#    try:
#        os.rmdir(path)
#    except WindowsError:
#        print("Directory is not empty: %s"% path)

def printTable(table):
    print('\n'.join(str(x) for x in table))

def prompt_book(c):
    print("Books:")
    c.execute("SELECT DISTINCT book FROM solutions")
    books = [x[0] for x in c.fetchall()]
    number_to_book_dict = dict(zip(range(1,len(books)+1),books))
    for n in number_to_book_dict:
        print("%d. %s"% (n,number_to_book_dict[n]))
    option = int(raw_input("Command?:"))
    found_book = number_to_book_dict[option]
    return found_book

def prompt_sections(book):
    print("Sections:")

def unindex(c,(book,section,name),path):
    c.execute("INSERT INTO unindexed VALUES(?,?,?,?)",(book,section,name,path))
    c.execute("SELECT id FROM solutions WHERE book = ? AND section = ? AND name = ?",(book,section,name))
    id = c.fetchone()[0]
    try:
        shutil.move("./files/%s.tex"% id,path)
    except IOError:
        print("Could not unindex: ./files/%s.tex -> %s"% (id,path))

def index(c,id,path):
    c.execute('DELETE FROM unindexed WHERE path = ?',(path,))
    try:
        shutil.move(path,"./files/%s.tex"% id)
    except IOError:
        print("Could not index: %s -> ./files/%s.tex"% (path,id))

def index_all(c):
    c.execute('SELECT id,path FROM unindexed NATURAL JOIN solutions')
    ids_paths = c.fetchall()
    if not ids_paths:
        print("All files seem to be indexed.")
    for (id,path) in ids_paths:
        index(c,id,path)
        #try_removing_dir(parent(path))

def unindex_section(c):
    book = raw_input("Enter book:")
    section = raw_input("Enter section:")
    c.execute("SELECT name FROM solutions WHERE book = ? AND section = ?",(book,section))
    names = [x[0] for x in c.fetchall()]
    if not names:
        print("Section not found: %s/%s"% (book,section))
        return
    dir_path = "./%s"% section
    try_making_directory(dir_path)
    for name in names:
        unindex(c,(book,section,name),"%s/%s.tex"% (dir_path,name))

def unindex_book(c):
    book = prompt_book(c)
    c.execute("SELECT section,name FROM solutions WHERE book = ?",(book,))
    try_making_directory("./%s"% book)
    sections_names = c.fetchall()
    for (section,name) in sections_names:
        dir_path = "./%s/%s"% (book,section)
        try_making_directory(dir_path)
        unindex(c,(book,section,name),"%s/%s.tex"% (dir_path,name))

def unindex_all(c):
    print("Under construction.")

conn = sqlite3.connect(database)
c = conn.cursor()

print("Sebastian Olsson's Indexer")
print("1. Index all")
print("2. Unindex section")
print("3. Unindex book")
#print("4. Unindex all")

options = {1 : index_all,
           2 : unindex_section,
           3 : unindex_book,
           4 : unindex_all
}

option = int(raw_input("Command?:"))

options[option](c)

conn.commit()
conn.close()
