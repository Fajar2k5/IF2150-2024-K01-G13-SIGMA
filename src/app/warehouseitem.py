"""
MODULE WAREHOUSEITEM
"""
import sqlite3
import os

# Define the database path relative to this script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
# DATABASE_PATH = os.path.join(DATABASE_DIR, "warehouse.db")
# ITEM_PATH = os.path.join(DATABASE_DIR, "item.db")
# DATABASE_PATH = os.path.join(DATABASE_DIR, "warehouseitem.db")
DATABASE_PATH = os.path.join(DATABASE_DIR, "database.db")


def initialize_warehouseitem_table():
    """
    Membuat tabel WarehouseItem di database
    """
    # First, make sure we can access both source tables
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master
                        WHERE type='table' AND name='items'""")
    if not cursor.fetchone():
        print("Items table not found in item database")
        conn.close()
        return

    cursor.execute("""SELECT name FROM sqlite_master
                        WHERE type='table' AND name='Warehouse'""")
    if not cursor.fetchone():
        print("Warehouse table not found in warehouse database")
        conn.close()
        return

    cursor.execute("""CREATE TABLE IF NOT EXISTS warehouseitem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                warehouse_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                UNIQUE (warehouse_id, item_id)
                )""")

    conn.commit()
    conn.close()


def get_item_details(item_id):
    """Helper function to get item details from item database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT volume FROM items WHERE id = ?", (item_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def update_warehouse_capacity(warehouse_id, volume_change):
    """Helper function to update warehouse capacity"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Get current warehouse data
    cursor.execute("""SELECT capacity, used_capacity
                          FROM Warehouse WHERE id = ?""", (warehouse_id,))
    warehouse_data = cursor.fetchone()

    if warehouse_data is None:
        conn.close()
        return False, "Warehouse not found"

    capacity, used_capacity = warehouse_data
    new_used_capacity = used_capacity + volume_change

    if new_used_capacity > capacity:
        conn.close()
        return False, "Warehouse capacity exceeded"

    if new_used_capacity < 0:
        conn.close()
        return False, "Invalid volume change"

    # Update warehouse capacity
    cursor.execute("""UPDATE Warehouse
                          SET used_capacity = ?
                          WHERE id = ?""", (new_used_capacity, warehouse_id))
    conn.commit()
    conn.close()
    return True, None


def add_item_to_warehouse(warehouse_id, item_id, quantity):
    """
    Menambahkan item ke dalam warehouse jika
    Warehouse.used_capacity + quantity x item_volume <= Warehouse.capacity
    """
    if quantity <= 0:
        print("Quantity must be positive when adding items")
        return

    # Check if item exists and get its volume
    item_volume = get_item_details(item_id)
    if item_volume is None:
        print(f"Item with id {item_id} not found.")
        return

    # Update warehouse capacity
    success, error = update_warehouse_capacity(
        warehouse_id, quantity * item_volume)
    if not success:
        print(error)
        return

    # Add the item to warehouseitem
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO warehouseitem (
                           warehouse_id, item_id, quantity)
                         VALUES (?, ?, ?)""",
                       (warehouse_id, item_id, quantity))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error adding item to warehouse: {e}")
        conn.rollback()
    finally:
        conn.close()


def update_item_quantity(warehouse_id, item_id, new_quantity):
    """
    Update the quantity of an item in a warehouse,
    adjusting the warehouse capacity accordingly.
    If new_quantity is 0, the item will be removed from the warehouse.
    """
    if new_quantity < 0:
        print("Quantity cannot be negative")
        return

    # If new quantity is 0, remove the item completely
    if new_quantity == 0:
        remove_item_from_warehouse(warehouse_id, item_id)
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Get current quantity
    cursor.execute("""SELECT quantity FROM warehouseitem
                     WHERE warehouse_id = ? AND item_id = ?""",
                   (warehouse_id, item_id))
    result = cursor.fetchone()

    if result is None:
        print(f"Item {item_id} not found in warehouse {warehouse_id}")
        conn.close()
        return

    current_quantity = result[0]

    # Calculate volume change
    item_volume = get_item_details(item_id)
    if item_volume is None:
        print(f"Item with id {item_id} not found.")
        conn.close()
        return

    volume_change = (new_quantity - current_quantity) * item_volume

    # Update warehouse capacity
    success, error = update_warehouse_capacity(warehouse_id, volume_change)
    if not success:
        print(error)
        conn.close()
        return

    # Update item quantity
    cursor.execute("""UPDATE warehouseitem
                     SET quantity = ?
                     WHERE warehouse_id = ? AND item_id = ?""",
                   (new_quantity, warehouse_id, item_id))
    conn.commit()
    conn.close()


def remove_item_from_warehouse(warehouse_id, item_id):
    """
    Remove an item completely from a warehouse
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Get current quantity
    cursor.execute("""SELECT quantity FROM warehouseitem
                     WHERE warehouse_id = ? AND item_id = ?""",
                   (warehouse_id, item_id))
    result = cursor.fetchone()

    if result is None:
        print(f"Item {item_id} not found in warehouse {warehouse_id}")
        conn.close()
        return

    current_quantity = result[0]

    # Calculate volume to free up
    item_volume = get_item_details(item_id)
    if item_volume is None:
        print(f"Item with id {item_id} not found.")
        conn.close()
        return

    # Update warehouse capacity (negative because we're removing)
    success, error = update_warehouse_capacity(
        warehouse_id, -current_quantity * item_volume)
    if not success:
        print(error)
        conn.close()
        return

    # Remove the item
    cursor.execute("""DELETE FROM warehouseitem
                     WHERE warehouse_id = ? AND item_id = ?""",
                   (warehouse_id, item_id))
    conn.commit()
    conn.close()


def transfer_items(from_warehouse_id, to_warehouse_id, item_id, quantity):
    """
    Transfer items from one warehouse to another
    """
    if quantity <= 0:
        print("Transfer quantity must be positive")
        return

    # Check if source warehouse has enough items
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""SELECT quantity FROM warehouseitem
                     WHERE warehouse_id = ? AND item_id = ?""",
                   (from_warehouse_id, item_id))
    result = cursor.fetchone()

    if result is None:
        print(f"Item {item_id} not found in source warehouse "
              f"{from_warehouse_id}")
        conn.close()
        return

    source_quantity = result[0]

    if source_quantity < quantity:
        print("Insufficient quantity in source warehouse. "
              f"Available: {source_quantity}")
        conn.close()
        return

    # Get item volume
    item_volume = get_item_details(item_id)
    if item_volume is None:
        print(f"Item with id {item_id} not found.")
        conn.close()
        return

    # Calculate volume changes
    transfer_volume = quantity * item_volume

    # Update destination warehouse capacity
    success, error = update_warehouse_capacity(
        to_warehouse_id, transfer_volume)
    if not success:
        print(f"Error with destination warehouse: {error}")
        conn.close()
        return

    # Update source warehouse capacity
    success, error = update_warehouse_capacity(
        from_warehouse_id, -transfer_volume)
    if not success:
        # Rollback destination warehouse change
        update_warehouse_capacity(to_warehouse_id, -transfer_volume)
        print(f"Error with source warehouse: {error}")
        conn.close()
        return

    try:
        # If transferring all items, potentially remove from source
        if quantity == source_quantity:
            cursor.execute("""DELETE FROM warehouseitem
                            WHERE warehouse_id = ? AND item_id = ?""",
                           (from_warehouse_id, item_id))
        else:
            # Reduce quantity in source warehouse
            cursor.execute("""UPDATE warehouseitem
                            SET quantity = quantity - ?
                            WHERE warehouse_id = ? AND item_id = ?""",
                           (quantity, from_warehouse_id, item_id))

        # Add or update quantity in destination warehouse
        cursor.execute("""INSERT INTO warehouseitem (
                       warehouse_id, item_id, quantity)
                         VALUES (?, ?, ?)
                         ON CONFLICT(warehouse_id, item_id)
                         DO UPDATE SET quantity = quantity + ?""",
                       (to_warehouse_id, item_id, quantity, quantity))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error during transfer: {e}")
        conn.rollback()
    finally:
        conn.close()
