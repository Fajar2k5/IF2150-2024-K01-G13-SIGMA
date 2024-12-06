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

def getName(id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    c.execute("SELECT name FROM items WHERE id = ?", (id,))
    name = c.fetchone()

    if name is None:
        print(f"Item with id '{id}' does not exists.")
        conn.close()
        return
    
    conn.close()
    return name

def getItemID(name):
    conn = sqlite3.connect('items.db')

    c = conn.cursor()

    c.execute("SELECT id FROM items WHERE name = ?", (name,))
    id = c.fetchone()
    if id is None:
        print(f"Item with name '{name}' does not exists.")
        conn.close()
        return
    
    conn.close()
    return id

def getQuantity(name):
    conn = sqlite3.connect('items.db')

    c = conn.cursor()

    c.execute("SELECT quantity FROM items WHERE name = ?", (name,))
    quantity = c.fetchone()
    if quantity is None:
        print(f"Item with name '{name}' does not exists.")
        conn.close()
        return
    
    conn.close()
    return quantity

def setName(id, new_name):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id = ?", (id,))
    if c.fetchone() is None:
        print(f"Item with id '{id}' does not exists.")
        conn.close()
        return
    
    c.execute("UPDATE items SET name = ? WHERE id = ?", (new_name, id))

    conn.commit()
    conn.close()

def setItemID(name, new_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE name = ?", (name,))
    if c.fetchone() is None:
        print(f"Item with name '{name}' does not exists.")
        conn.close()
        return
    
    c.execute("UPDATE items SET id = ? WHERE name = ?", (new_id, name))

    conn.commit()
    conn.close()

def setQuantity(name, new_quantity):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE name = ?", (name,))
    if c.fetchone() is None:
        print(f"Item with name '{name}' does not exists.")
        conn.close()
        return
    
    c.execute("UPDATE items SET quantity = ? WHERE name = ?", (new_quantity, name))

    conn.commit()
    conn.close()

def main():
    
    print(getQuantity('apple'))
    print(getItemID('apple'))
    print(getName(1))
    
    print(getQuantity('avocado'))
    print(getItemID('avocado'))
    print(getName(2))
    

if __name__ == "__main__":
    main()