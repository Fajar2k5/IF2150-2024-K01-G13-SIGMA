"""
ITEM MODULE
"""
import sqlite3
import os


# Define the database path relative to this script's location
# src directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "item.db")


def create_item_table():
    """
    Membuat tabel item di database
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE items (
                id integer primary key autoincrement,
                name text,
                description text,
                volume integer
                )""")

    conn.commit()
    conn.close()


def get_item_name(item_id):
    """
    Mengambil nama item berdasarkan id
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT name FROM items WHERE id = ?", (item_id,))
    name = c.fetchone()

    if name is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    conn.close()
    return name


def get_item_id(name):
    """
    Mengambil id item berdasarkan nama
    """
    conn = sqlite3.connect(DATABASE_PATH)

    c = conn.cursor()

    c.execute("SELECT id FROM items WHERE name = ?", (name,))
    item_id = c.fetchone()
    if item_id is None:
        print(f"Item with name '{name}' does not exists.")
        conn.close()
        return
    conn.close()
    return item_id


def get_item_description(item_id):
    """
    Mengambil deskripsi item berdasarkan nama
    """
    conn = sqlite3.connect(DATABASE_PATH)

    c = conn.cursor()

    c.execute("SELECT description FROM items WHERE id = ?", (item_id,))
    description = c.fetchone()
    if description is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    conn.close()
    return description


def set_item_name(item_id, new_name):
    """
    Mengganti nama item berdasarkan id
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if c.fetchone() is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    c.execute("UPDATE items SET name = ? WHERE id = ?", (new_name, item_id))

    conn.commit()
    conn.close()


def set_item_description(item_id, new_description):
    """
    Mengganti description item berdasarkan nama
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if c.fetchone() is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    c.execute("UPDATE items SET description = ? WHERE id = ?",
              (new_description, item_id))

    conn.commit()
    conn.close()


def get_item_volume(item_id):
    """
    Mengambil volume item berdasarkan id
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT volume FROM items WHERE id = ?", (item_id,))
    volume = c.fetchone()

    if volume is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    conn.close()
    return volume


def set_item_volume(item_id, new_volume):
    """
    Mengganti volume item berdasarkan id
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    if c.fetchone() is None:
        print(f"Item with id '{item_id}' does not exists.")
        conn.close()
        return
    c.execute("UPDATE items SET volume = ? WHERE id = ?",
              (new_volume, item_id))

    conn.commit()
    conn.close()
    
def add_item(name, description, volume):
    if volume <= 0:
        print("the input should be positive")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    try:
        # kasus nama item tidak boleh sama, jika sama maka ada info
        c.execute("SELECT id FROM items WHERE name = ?", (name,))
        if c.fetchone():
            print(f"Item with name '{name}' already exists.")
            return

        # nambahin item secara regular
        c.execute("INSERT INTO items (name, description, volume) VALUES (?, ?, ?)",
                  (name, description, volume))
        conn.commit()
        print(f"Item '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding item: {e}")
    finally:
        conn.close()


def update_item(item_id, name=None, description=None, volume=None):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    try:
        # checking kalau ada item
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        if not c.fetchone():
            print(f"Item with id '{item_id}' does not exist.")
            return

        # update query
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if description:
            updates.append("description = ?")
            params.append(description)
        if volume:
            if volume <= 0:
                print("Volume must be a positive number.")
                return
            updates.append("volume = ?")
            params.append(volume)

        if not updates:
            print("No fields to update.")
            return

        query = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
        params.append(item_id)

        c.execute(query, tuple(params))
        conn.commit()
        print(f"Item with ID '{item_id}' updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating item: {e}")
    finally:
        conn.close()


def read_item(item_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = c.fetchone()
        if item:
            print(f"Item Details: ID={item[0]}, Name={item[1]}, "
                  f"Description={item[2]}, Volume={item[3]}")
        else:
            print(f"Item with id '{item_id}' does not exist.")
    except sqlite3.Error as e:
        print(f"Error reading item: {e}")
    finally:
        conn.close()


def delete_item(item_id):
    """
    Menghapus item berdasarkan ID
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    try:
        # check kalau item ada
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        if not c.fetchone():
            print(f"Item with id '{item_id}' does not exist.")
            return

        # hapus item secara reguler
        c.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        print(f"Item with ID '{item_id}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting item: {e}")
    finally:
        conn.close()


# def main():
#     print(get_quantity('apple'))
#     print(get_item_id('apple'))
#     print(get_name(1))
#     print(get_quantity('avocado'))
#     print(get_item_id('avocado'))
#     print(get_name(2))

# if __name__ == "__main__":
#     main()
