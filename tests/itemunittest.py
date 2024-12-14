import unittest
import sqlite3

# Menggunakan database in-memory untuk pengujian dengan koneksi global
db_connection = sqlite3.connect(':memory:')

def setup_database():
    """Setup database schema."""
    c = db_connection.cursor()
    # Menghapus tabel 'items' jika ada 
    c.execute("DROP TABLE IF EXISTS items")
    c.execute("""CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                volume INTEGER NOT NULL
            )""")
    db_connection.commit()

def delete_item(item_id):
    c = db_connection.cursor()
    try:
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        if not c.fetchone():
            return False, f"Item with id '{item_id}' does not exist."

        c.execute("DELETE FROM items WHERE id = ?", (item_id,))
        db_connection.commit()
        return True, f"Item with ID '{item_id}' deleted successfully."
    except sqlite3.Error as e:
        return False, str(e)

def update_item(item_id, name=None, description=None, volume=None):
    c = db_connection.cursor()
    try:
        c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        if not c.fetchone():
            return False, f"Item with id '{item_id}' does not exist."

        if name:
            c.execute("SELECT id FROM items WHERE name = ? AND id != ?", (name, item_id))
            if c.fetchone():
                return False, f"Item with the name '{name}' already exists."

        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if description:
            updates.append("description = ?")
            params.append(description)
        if volume is not None:
            if volume <= 0:
                return False, "Volume must be a positive number."
            updates.append("volume = ?")
            params.append(volume)

        if not updates:
            return False, "No fields to update."

        query = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
        params.append(item_id)

        c.execute(query, tuple(params))
        db_connection.commit()
        return True, f"Item with ID '{item_id}' updated successfully."
    except sqlite3.Error as e:
        return False, str(e)

def add_item(name, description, volume):
    c = db_connection.cursor()
    try:
        c.execute("SELECT id FROM items WHERE name = ?", (name,))
        if c.fetchone():
            return False, f"Item with name '{name}' already exists."

        if volume <= 0:
            return False, "Volume must be a positive number."

        c.execute("INSERT INTO items (name, description, volume) VALUES (?, ?, ?)", (name, description, volume))
        db_connection.commit()
        return True, f"Item '{name}' added successfully."
    except sqlite3.Error as e:
        return False, str(e)

class TestItemOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database()
        add_item("Item1", "Description1", 10)
        add_item("Item2", "Description2", 20)
        
    def test_update_with_existing_name(self):
        add_item("Item1", "Description1", 10)
        success, message = update_item(2, name="Item1")
        self.assertFalse(success)
        self.assertEqual(message, "Item with the name 'Item1' already exists.")
        
    def test_update_with_invalid_volume(self):
        success, message = update_item(2, volume=-10)
        self.assertFalse(success)
        self.assertEqual(message, "Volume must be a positive number.")

    def test_update_with_no_changes(self):
        success, message = update_item(2)
        self.assertFalse(success)
        self.assertEqual(message, "No fields to update.")

    def test_delete_existing_item(self):
        success, message = delete_item(1)
        self.assertTrue(success)
        self.assertEqual(message, "Item with ID '1' deleted successfully.")

    def test_delete_nonexistent_item(self):
        success, message = delete_item(999)
        self.assertFalse(success)
        self.assertEqual(message, "Item with id '999' does not exist.")

    def test_update_existing_item(self):
        success, message = update_item(2, name="NewItem2", description="Updated Description", volume=25)
        self.assertTrue(success)
        self.assertEqual(message, "Item with ID '2' updated successfully.")

    def test_update_nonexistent_item(self):
        success, message = update_item(999, name="Nonexistent", description="None", volume=5)
        self.assertFalse(success)
        self.assertEqual(message, "Item with id '999' does not exist.")


    def test_add_item_success(self):
        success, message = add_item("NewItem", "New Description", 15)
        self.assertTrue(success)
        self.assertEqual(message, "Item 'NewItem' added successfully.")

    def test_add_item_existing_name(self):
        success, message = add_item("Item1", "Duplicate Name", 5)
        self.assertFalse(success)
        self.assertEqual(message, "Item with name 'Item1' already exists.")

    def test_add_item_invalid_volume(self):
        success, message = add_item("InvalidVolumeItem", "Description", -5)
        self.assertFalse(success)
        self.assertEqual(message, "Volume must be a positive number.")

if __name__ == "__main__":
    unittest.main()
