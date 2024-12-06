"""
warehouse.py

This module provides functionalities for managing warehouse operations,
including inventory tracking, order processing, and reporting.
"""

# import tkinter as tk
import os
import sqlite3


# Define the database path relative to this script's location
# src directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "warehouse.db")


def initialize_warehouse_tables():
    """
    Fungsi ini akan membuat tabel-tabel yang diperlukan,
    untuk menyimpan data Warehouse (jika belum ada)
    """
    # Ensure the database directory exists
    os.makedirs(DATABASE_DIR, exist_ok=True)

    # Connect to SQLite database (or create one if it doesn't exist)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create Warehouse table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Warehouse (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        capacity REAL NOT NULL,
        used_capacity REAL DEFAULT 0.0
    );
    """)

    # Create Item table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image TEXT,
        volume REAL NOT NULL
    );
    """)

    # Create WarehouseItem table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WarehouseItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (warehouse_id) REFERENCES Warehouse (id),
        FOREIGN KEY (item_id) REFERENCES Item (id),
        UNIQUE (warehouse_id, item_id)
    );
    """)

    conn.commit()
    print("Tables created successfully.")
    conn.close()


def print_all_warehouse():
    """
    Fungsi ini akan menampilkan semua data Warehouse
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Warehouse")
    warehouses = cursor.fetchall()

    for warehouse in warehouses:
        print(warehouse)

    conn.close()


def total_volume_used(warehouse_id: int):
    """
    Fungsi ini menghitung total volume yang digunakan di gudang
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT used_capacity FROM Warehouse WHERE id = ?",
                   (warehouse_id,))
    used_capacity = cursor.fetchone()

    if used_capacity:
        print(f"Total volume used in Warehouse {warehouse_id}: "
              f"{used_capacity[0]}")
    else:
        print(f"Warehouse with ID {warehouse_id} does not exist.")

    conn.close()


def add_warehouse(name: str, description: str, capacity: float):
    """
    Fungsi ini akan menambahkan data Warehouse baru
    """
    if capacity <= 0:
        print("Capacity must be a positive number.")
        return

    # Connect to the database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Check if the warehouse name already exists
        cursor.execute("SELECT id FROM Warehouse WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"A warehouse with the name '{name}' already exists.")
            return

        # Insert the new warehouse data
        cursor.execute("""
        INSERT INTO Warehouse (name, description, capacity)
        VALUES (?, ?, ?);
        """, (name, description, capacity))
        conn.commit()
        print(f"Warehouse '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding warehouse: {e}")
    finally:
        conn.close()


def edit_warehouse(warehouse_id: int, name: str = None,
                   description: str = None, capacity: float = None):
    """
    Fungsi ini digunakan untuk mengedit data Warehouse yang sudah ada
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Check if the warehouse exists
        cursor.execute("SELECT * FROM Warehouse WHERE id = ?", (warehouse_id,))
        if not cursor.fetchone():
            print(f"Warehouse with ID {warehouse_id} does not exist.")
            return

        # Build the UPDATE query dynamically
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if description:
            updates.append("description = ?")
            params.append(description)
        if capacity:
            if capacity <= 0:
                print("Capacity must be a positive number.")
                return
            updates.append("capacity = ?")
            params.append(capacity)

        if not updates:
            print("No fields to update.")
            return

        query = f"UPDATE Warehouse SET {', '.join(updates)} WHERE id = ?"
        params.append(warehouse_id)

        # Execute the query
        cursor.execute(query, tuple(params))
        conn.commit()
        print(f"Warehouse with ID {warehouse_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating warehouse: {e}")
    finally:
        conn.close()


def delete_warehouse(warehouse_id: int):
    """
    Fungsi untuk menghapus warehouse berdasarkan ID nya
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        # Check if the warehouse exists
        cursor.execute("SELECT * FROM Warehouse WHERE id = ?", (warehouse_id,))
        if not cursor.fetchone():
            print(f"Warehouse with ID {warehouse_id} does not exist.")
            return

        # Delete associated records in WarehouseItem
        cursor.execute("DELETE FROM WarehouseItem WHERE warehouse_id = ?",
                       (warehouse_id,))
        # Delete the warehouse
        cursor.execute("DELETE FROM Warehouse WHERE id = ?", (warehouse_id,))
        conn.commit()
        print(f"Warehouse with ID {warehouse_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting warehouse: {e}")
    finally:
        conn.close()
