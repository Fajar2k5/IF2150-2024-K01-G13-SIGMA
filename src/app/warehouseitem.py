"""
MODULE WAREHOUSEITEM
"""
import sqlite3
import os


# Define the database path relative to this script's location
# src directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
WAREHOUSE_PATH = os.path.join(DATABASE_DIR, "warehouse.db")
ITEM_PATH = os.path.join(DATABASE_DIR, "item.db")
WAREITEM_PATH = os.path.join(DATABASE_DIR, "warehouseitem.db")


def initialize_warehouseitem_table():
    """
    Membuat tabel WarehouseItem di database
    """
    # Connect to main database
    conn = sqlite3.connect(WAREITEM_PATH)
    cursor = conn.cursor()

    # Enable foreign key
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Attach the other database
    cursor.execute(f"ATTACH DATABASE '{ITEM_PATH}' AS item_db")
    cursor.execute(f"ATTACH DATABASE '{WAREHOUSE_PATH}' AS ware_db")

    cursor.execute("""CREATE TABLE IF NOT EXISTS warehouseitem (
                id integer primary key autoincrement,
                warehouse_id integer,
                item_id integer,
                quantity integer,
                foreign key (warehouse_id) references Warehouse(id),
                foreign key (item_id) references items(id),
                unique (warehouse_id, item_id)
                )""")

    conn.commit()
    conn.close()


def add_item_to_warehouse(warehouse_id, item_id, quantity):
    """
    Menambahkan item ke dalam warehouse jika
    Warehouse.used_capacity + quantity x item_volume <= Warehouse.capacity
    """
    conn = sqlite3.connect(WAREITEM_PATH)
    cursor = conn.cursor()

    # Enable foreign key
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(f"ATTACH DATABASE '{ITEM_PATH}' AS item_db")
    cursor.execute(f"ATTACH DATABASE '{WAREHOUSE_PATH}' AS ware_db")

    # Get the item volume
    cursor.execute("SELECT volume FROM item_db.items WHERE id = ?", (item_id,))
    item_volume = cursor.fetchone()[0]

    # Get the warehouse capacity and used capacity
    cursor.execute("""SELECT capacity, used_capacity
                   FROM ware_db.Warehouse WHERE id = ?""", (warehouse_id,))
    capacity, used_capacity = cursor.fetchone()

    # Calculate the new used capacity
    new_used_capacity = used_capacity + quantity * item_volume

    # Check if the new used capacity exceeds the warehouse capacity
    if new_used_capacity > capacity:
        print("Warehouse capacity exceeded.")
        return

    # Set the new used capacity
    cursor.execute("""UPDATE ware_db.Warehouse
                   SET used_capacity = ?
                   WHERE id = ?""", (new_used_capacity, warehouse_id))

    # Add the item to the warehouse
    cursor.execute("""INSERT INTO warehouseitem (
                   warehouse_id, item_id, quantity) VALUES (?, ?, ?)""",
                   (warehouse_id, item_id, quantity))

    conn.commit()
    conn.close()
