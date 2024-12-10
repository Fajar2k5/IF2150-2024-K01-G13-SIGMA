"""
GUIT FOR ITEM MANAGEMENT
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import item

class ItemGUI:
    """
    Main GUI untuk item management
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Item Management")
        self.root.geometry("800x600")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and setup widgets
        self.setup_item_list()
        self.setup_buttons()
        self.refresh_item_list()

    def setup_item_list(self):
        """
        Melakukan setup untuk item list
        """
        # item list with scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.grid(row=0, column=0, columnspan=4, sticky=(
            tk.W, tk.E, tk.N, tk.S))

        self.item_tree = ttk.Treeview(list_frame, columns=(
            "ID", "Name", "Description", "Volume"),
            show="headings")

        # Define columns
        self.item_tree.heading("ID", text="ID")
        self.item_tree.heading("Name", text="Name")
        self.item_tree.heading("Description", text="Description")
        self.item_tree.heading("Volume", text="Volume")

        # Column widths
        self.item_tree.column("ID", width=50)
        self.item_tree.column("Name", width=150)
        self.item_tree.column("Description", width=250)
        self.item_tree.column("Volume", width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)

        self.item_tree.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def setup_buttons(self):
        """
        Melakukan setup untuk tombol-tombol CRUD
        """
        # CRUD Buttons
        ttk.Button(self.main_frame, text="Add Item",
                   command=self.show_add_dialog).grid(
                    row=1, column=0, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Edit Item",
                   command=self.show_edit_dialog).grid(
                    row=1, column=1, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Delete Item",
                   command=self.delete_item).grid(
                    row=1, column=2, pady=10, padx=5)
        ttk.Button(self.main_frame, text="Refresh",
                   command=self.refresh_item_list).grid(
                    row=1, column=3, pady=10, padx=5)

    def refresh_item_list(self):
        """
        Mengambil data item dari database dan menampilkan di treeview
        """
        # Clear existing items
        for z in self.item_tree.get_children():
            self.item_tree.delete(z)

        # Connect to database and fetch items
        conn = sqlite3.connect(item.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        conn.close()

        # Insert item data
        for w in items:
            self.item_tree.insert("", tk.END, values=w)

    def show_add_dialog(self):
        """
        Melakukan show dialog untuk menambahkan item baru
        """
        dialog = ItemDialog(self.root, "Add item")
        if dialog.result:
            name, desc, volume = dialog.result
            item.add_item(name, desc, float(volume))
            self.refresh_item_list()

    def show_edit_dialog(self):
        """
        Melakukan show dialog untuk mengedit item
        """
        selected = self.item_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select an item to edit")
            return

        items = self.item_tree.item(selected[0])
        values = items['values']

        dialog = ItemDialog(self.root, "Edit item",
                                 values[1], values[2], values[3])
        if dialog.result:
            name, desc, volume = dialog.result
            item.update_item(values[0], name, desc, float(volume))
            self.refresh_item_list()

    def delete_item(self):
        """
        Menghapus item yang dipilih
        """
        selected = self.item_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select an item to delete")
            return

        if messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this item?"):
            items = self.item_tree.item(selected[0])
            item_id = items['values'][0]
            item.delete_item(item_id)
            self.refresh_item_list()


class ItemDialog:
    """
    Dialog untuk menambahkan atau mengedit item
    """
    def __init__(self, parent, title, name="", desc="", volume=""):
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

        ttk.Label(self.dialog, text="Volume:").grid(
            row=2, column=0, pady=5, padx=5)
        self.volume_entry = ttk.Entry(self.dialog, width=40)
        self.volume_entry.insert(0, volume)
        self.volume_entry.grid(row=2, column=1, pady=5, padx=5)

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
        Validasi dan simpan data item
        """
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        volume = self.volume_entry.get().strip()

        if not all([name, desc, volume]):
            messagebox.showwarning("Validation Error",
                                   "All fields are required")
            return

        try:
            volume = float(volume)
            if volume <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error",
                                   "Volume must be a positive number")
            return

        self.result = (name, desc, volume)
        self.dialog.destroy()


def main():
    """
    Fungsi main untuk menjalankan aplikasi GUI
    """
    root = tk.Tk()
    ItemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
