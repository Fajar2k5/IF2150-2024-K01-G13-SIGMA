"""
GUIT FOR WAREHOUSE MANAGEMENT
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import warehouse


class WarehouseGUI:
    """
    Main GUI untuk warehouse management
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Management")
        self.root.geometry("800x600")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and setup widgets
        self.setup_warehouse_list()
        self.setup_buttons()
        self.refresh_warehouse_list()

    def setup_warehouse_list(self):
        """
        Melakukan setup untuk warehouse list
        """
        # Warehouse list with scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.grid(row=0, column=0, columnspan=4, sticky=(
            tk.W, tk.E, tk.N, tk.S))

        self.warehouse_tree = ttk.Treeview(list_frame, columns=(
            "ID", "Name", "Description", "Capacity", "Used"),
            show="headings")

        # Define columns
        self.warehouse_tree.heading("ID", text="ID")
        self.warehouse_tree.heading("Name", text="Name")
        self.warehouse_tree.heading("Description", text="Description")
        self.warehouse_tree.heading("Capacity", text="Capacity")
        self.warehouse_tree.heading("Used", text="Used Capacity")

        # Column widths
        self.warehouse_tree.column("ID", width=50)
        self.warehouse_tree.column("Name", width=150)
        self.warehouse_tree.column("Description", width=250)
        self.warehouse_tree.column("Capacity", width=100)
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
        ttk.Button(self.main_frame, text="Add Warehouse",
                   command=self.show_add_dialog).grid(
                    row=1, column=0, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Edit Warehouse",
                   command=self.show_edit_dialog).grid(
                    row=1, column=1, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Delete Warehouse",
                   command=self.delete_warehouse).grid(
                    row=1, column=2, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Refresh",
                   command=self.refresh_warehouse_list).grid(
                    row=1, column=3, pady=10, padx=5)

    def refresh_warehouse_list(self):
        """
        Mengambil data warehouse dari database dan menampilkan di treeview
        """
        # Clear existing items
        for item in self.warehouse_tree.get_children():
            self.warehouse_tree.delete(item)

        # Connect to database and fetch warehouses
        conn = sqlite3.connect(warehouse.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Warehouse")
        warehouses = cursor.fetchall()
        conn.close()

        # Insert warehouse data
        for w in warehouses:
            self.warehouse_tree.insert("", tk.END, values=w)

    def show_add_dialog(self):
        """
        Melakukan show dialog untuk menambahkan warehouse baru
        """
        dialog = WarehouseDialog(self.root, "Add Warehouse")
        if dialog.result:
            name, desc, capacity = dialog.result
            warehouse.add_warehouse(name, desc, float(capacity))
            self.refresh_warehouse_list()

    def show_edit_dialog(self):
        """
        Melakukan show dialog untuk mengedit warehouse
        """
        selected = self.warehouse_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a warehouse to edit")
            return

        item = self.warehouse_tree.item(selected[0])
        values = item['values']

        dialog = WarehouseDialog(self.root, "Edit Warehouse",
                                 values[1], values[2], values[3])
        if dialog.result:
            name, desc, capacity = dialog.result
            warehouse.edit_warehouse(values[0], name, desc, float(capacity))
            self.refresh_warehouse_list()

    def delete_warehouse(self):
        """
        Menghapus warehouse yang dipilih
        """
        selected = self.warehouse_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a warehouse to delete")
            return

        if messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this warehouse?"):
            item = self.warehouse_tree.item(selected[0])
            warehouse_id = item['values'][0]
            warehouse.delete_warehouse(warehouse_id)
            self.refresh_warehouse_list()


class WarehouseDialog:
    """
    Dialog untuk menambahkan atau mengedit warehouse
    """
    def __init__(self, parent, title, name="", desc="", capacity=""):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Form fields
        ttk.Label(self.dialog, text="Name:").grid(
            row=0, column=0, pady=5, padx=5)
        self.name_entry = ttk.Entry(self.dialog, width=40)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.dialog, text="Description:").grid(
            row=1, column=0, pady=5, padx=5)
        self.desc_entry = ttk.Entry(self.dialog, width=40)
        self.desc_entry.insert(0, desc)
        self.desc_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.dialog, text="Capacity:").grid(
            row=2, column=0, pady=5, padx=5)
        self.capacity_entry = ttk.Entry(self.dialog, width=40)
        self.capacity_entry.insert(0, capacity)
        self.capacity_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Save", command=self.save).grid(
            row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).grid(
            row=0, column=1, padx=5)

        # Center the dialog
        self.dialog.wait_window()

    def save(self):
        """
        Validasi dan simpan data warehouse
        """
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        capacity = self.capacity_entry.get().strip()

        if not all([name, desc, capacity]):
            messagebox.showwarning("Validation Error",
                                   "All fields are required")
            return

        try:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error",
                                   "Capacity must be a positive number")
            return

        self.result = (name, desc, capacity)
        self.dialog.destroy()


def main():
    """
    Fungsi main untuk menjalankan aplikasi GUI
    """
    root = tk.Tk()
    WarehouseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
