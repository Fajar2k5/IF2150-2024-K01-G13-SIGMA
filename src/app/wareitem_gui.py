"""
GUIT FOR WAREHOUSE ITEM MANAGEMENT
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import item


class WarehouseGUI:
    """
    Main GUI untuk warehouse item management
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse item Management")
        self.root.geometry("800x600")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and setup widgets
        self.setup_warehouseitem_list()
        self.setup_buttons()

    def setup_warehouseitem_list(self):
        """
        Melakukan setup untuk warehouse list
        """
        # Warehouse Item list with scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.grid(row=0, column=0, columnspan=4, sticky=(
            tk.W, tk.E, tk.N, tk.S))

        self.warehouse_tree = ttk.Treeview(list_frame, columns=(
            "ID", "Name", "Quantity", "Volume", "Used"),
            show="headings")

        # Define columns
        self.warehouse_tree.heading("ID", text="ID")
        self.warehouse_tree.heading("Name", text="Name")
        self.warehouse_tree.heading("Quantity", text="Quantity")
        self.warehouse_tree.heading("Volume", text="Volume")
        self.warehouse_tree.heading("Used", text="Used Space")

        # Column widths
        self.warehouse_tree.column("ID", width=50)
        self.warehouse_tree.column("Name", width=150)
        self.warehouse_tree.column("Quantity", width=150)
        self.warehouse_tree.column("Volume", width=100)
        self.warehouse_tree.column("Used", width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.warehouse_tree.yview)
        self.warehouse_tree.configure(yscrollcommand=scrollbar.set)

        self.warehouse_tree.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def setup_buttons(self):
        """
        Melakukan setup untuk tombol-tombol CRUD
        """
        # CRUD Buttons
        ttk.Button(self.main_frame, text="Add Item"
                   ).grid(
                    row=1, column=0, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Edit Item"
                   ).grid(
                    row=1, column=1, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Delete Item"
                   ).grid(
                    row=1, column=2, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Refresh"
                   ).grid(
                    row=1, column=3, pady=10, padx=5)        


def main():
    """
    Fungsi main untuk menjalankan aplikasi GUI
    """
    root = tk.Tk()
    WarehouseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()