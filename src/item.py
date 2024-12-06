import sqlite3

def createTable ():
    conn = sqlite3.connect('items.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE items (
                name text, 
                id integer,
                quantity integer
                )""")

    conn.commit()

    conn.close()

