import unittest
import sqlite3

# Menggunakan database in-memory untuk pengujian dengan koneksi global
db_connection = sqlite3.connect(':memory:')

def setup_database():
    """Setup database schema."""
    c = db_connection.cursor()
    # Menghapus tabel 'items' jika ada 
    c.execute("DROP TABLE IF EXISTS Warehouse")
    c.execute("""CREATE TABLE IF NOT EXISTS Warehouse (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                capacity REAL NOT NULL,
                used_capacity REAL DEFAULT 0.0
            )""")
    db_connection.commit()

def add_warehouse(name, description, capacity):
    c = db_connection.cursor()
    try:
        c.execute("SELECT id FROM Warehouse WHERE name = ?", (name,))
        if c.fetchone():
            return False, f"Warehouse with name '{name}' already exists."

        if capacity <= 0:
            return False, "Capacity must be a positive number."

        c.execute("INSERT INTO Warehouse (name, description, capacity) VALUES (?, ?, ?)", (name, description, capacity))
        db_connection.commit()
        return True, f"Warehouse '{name}' added successfully."
    except sqlite3.Error as e:
        return False, str(e)

def delete_warehouse(warehouse_id):
    c = db_connection.cursor()
    try:
        c.execute("SELECT * FROM Warehouse WHERE id = ?", (warehouse_id,))
        if not c.fetchone():
            return False, f"Warehouse with id '{warehouse_id}' does not exist."

        c.execute("DELETE FROM Warehouse WHERE id = ?", (warehouse_id,))
        db_connection.commit()
        return True, f"Warehouse with ID '{warehouse_id}' deleted successfully."
    except sqlite3.Error as e:
        return False, str(e)

def edit_warehouse(warehouse_id, name=None, description=None, capacity=None):
    c = db_connection.cursor()
    try:
        c.execute("SELECT * FROM Warehouse WHERE id = ?", (warehouse_id,))
        if not c.fetchone():
            return False, f"Warehouse with id '{warehouse_id}' does not exist."

        if name:
            c.execute("SELECT id FROM Warehouse WHERE name = ? AND id != ?", (name, warehouse_id))
            if c.fetchone():
                return False, f"Warehouse with the name '{name}' already exists."

        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if description:
            updates.append("description = ?")
            params.append(description)
        if capacity is not None:
            if capacity <= 0:
                return False, "Capacity must be a positive number."
            updates.append("capacity = ?")
            params.append(capacity)

        if not updates:
            return False, "No fields to update."

        query = f"UPDATE Warehouse SET {', '.join(updates)} WHERE id = ?"
        params.append(warehouse_id)

        c.execute(query, tuple(params))
        db_connection.commit()
        return True, f"Warehouse with ID '{warehouse_id}' updated successfully."
    except sqlite3.Error as e:
        return False, str(e)

# Unit test untuk fungsi add_warehouse
class TestAddWarehouse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database()

    def test_add_warehouse_success(self):
        success, message = add_warehouse("NewWarehouse", "New Description", 100.0)
        self.assertTrue(success)
        self.assertEqual(message, "Warehouse 'NewWarehouse' added successfully.")

    def test_add_warehouse_existing_name(self):
        add_warehouse("ExistingWarehouse", "Description", 50.0)
        success, message = add_warehouse("ExistingWarehouse", "Duplicate", 30.0)
        self.assertFalse(success)
        self.assertEqual(message, "Warehouse with name 'ExistingWarehouse' already exists.")

    def test_add_warehouse_invalid_capacity(self):
        success, message = add_warehouse("InvalidCapacity", "Description", -10.0)
        self.assertFalse(success)
        self.assertEqual(message, "Capacity must be a positive number.")

# Unit test untuk fungsi delete_warehouse
class TestDeleteWarehouse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database()
        add_warehouse("WarehouseToDelete", "Description", 200.0)

    def test_delete_existing_warehouse(self):
        success, message = delete_warehouse(1)
        self.assertTrue(success)
        self.assertEqual(message, "Warehouse with ID '1' deleted successfully.")

    def test_delete_nonexistent_warehouse(self):
        success, message = delete_warehouse(999)
        self.assertFalse(success)
        self.assertEqual(message, "Warehouse with id '999' does not exist.")

# Unit test untuk fungsi edit_warehouse
class TestEditWarehouse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database()
        add_warehouse("WarehouseToEdit", "Old Description", 150.0)

    def test_edit_existing_warehouse(self):
        success, message = edit_warehouse(1, name="UpdatedWarehouse", description="Updated Description", capacity=300.0)
        self.assertTrue(success)
        self.assertEqual(message, "Warehouse with ID '1' updated successfully.")

    def test_edit_nonexistent_warehouse(self):
        success, message = edit_warehouse(999, name="Nonexistent")
        self.assertFalse(success)
        self.assertEqual(message, "Warehouse with id '999' does not exist.")

    def test_edit_with_existing_name(self):
        add_warehouse("AnotherWarehouse", "Description", 200.0)
        success, message = edit_warehouse(1, name="AnotherWarehouse")
        self.assertFalse(success)
        self.assertEqual(message, "Warehouse with the name 'AnotherWarehouse' already exists.")

    def test_edit_with_invalid_capacity(self):
        success, message = edit_warehouse(1, capacity=-50.0)
        self.assertFalse(success)
        self.assertEqual(message, "Capacity must be a positive number.")

    def test_edit_with_no_changes(self):
        success, message = edit_warehouse(1)
        self.assertFalse(success)
        self.assertEqual(message, "No fields to update.")

if __name__ == "__main__":
    unittest.main()
