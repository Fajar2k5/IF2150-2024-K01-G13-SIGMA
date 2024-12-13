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

        # Set default font for all widgets
        default_font = ('Microsoft YaHei UI Light', 10)
        self.root.option_add('*Font', default_font)

        # Apply font to specific widget types
        style = ttk.Style()
        style.configure('Treeview', font=default_font)
        style.configure('Treeview.Heading', font=default_font)

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
        button_font = ('Microsoft YaHei UI Light', 10)
        button_width = 120
        button_height = 40
        button_radius = 10

        # Use tk.Frame instead of ttk.Frame
        button_frame = tk.Frame(self.main_frame, bg='#F0F0F0')
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)

        # CRUD Buttons with consistent styling
        buttons = [
            ("Add Warehouse", self.show_add_dialog),
            ("Edit Warehouse", self.show_edit_dialog),
            ("Delete Warehouse", self.delete_warehouse),
            ("Refresh", self.refresh_warehouse_list),
            ("Expand", self.show_expand_dialog)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = RoundedButton(
                button_frame,
                text=text,
                command=command,
                width=button_width,
                height=button_height,
                corner_radius=button_radius,
                color='#6666FF',
                hover_color='#7777FF',
                font=button_font
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

    def show_expand_dialog(self):
        """
        Menampilkan semua data warehouse yang dipilih dalam jendela pop-up
        """
        selected = self.warehouse_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a warehouse to expand")
            return

        item = self.warehouse_tree.item(selected[0])
        values = item['values']

        expand_dialog = tk.Toplevel(self.root)
        expand_dialog.title("Warehouse Details")
        expand_dialog.geometry("400x300")

        ttk.Label(expand_dialog, text="ID:").grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Label(expand_dialog, text=values[0]).grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(expand_dialog, text="Name:").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Label(expand_dialog, text=values[1]).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(expand_dialog, text="Description:").grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        desc_text = tk.Text(expand_dialog, wrap=tk.WORD, height=5, width=40)
        desc_text.insert(tk.END, values[2])
        desc_text.config(state=tk.DISABLED)
        desc_text.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        desc_scrollbar = ttk.Scrollbar(expand_dialog, orient=tk.VERTICAL, command=desc_text.yview)
        desc_text.config(yscrollcommand=desc_scrollbar.set)
        desc_scrollbar.grid(row=2, column=2, pady=5, padx=5, sticky=(tk.N, tk.S))

        ttk.Label(expand_dialog, text="Capacity:").grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Label(expand_dialog, text=values[3]).grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(expand_dialog, text="Used Capacity:").grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
        ttk.Label(expand_dialog, text=values[4]).grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Button(expand_dialog, text="Close", command=expand_dialog.destroy).grid(row=5, column=0, columnspan=2, pady=10)

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
        cursor.execute("SELECT id, name, description, capacity, used_capacity FROM Warehouse")
        warehouses = cursor.fetchall()
        conn.close()

        # Insert warehouse data with percentage used capacity
        for w in warehouses:
            ware_id, name, description, capacity, used_capacity = w
            used_percentage = (used_capacity / capacity) * 100 if capacity > 0 else 0
            self.warehouse_tree.insert("", tk.END, values=(ware_id, name, description, capacity, f"{used_capacity} ({used_percentage:.2f}%)"))

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


class RoundedButton(tk.Canvas):
    """
    Custom button widget with rounded corners
    """
    def __init__(self, parent, text, command, width=150, height=40,
                 corner_radius=10, padding=0, color="#6666FF",
                 text_color="white",
                 hover_color="#7777FF", font=None):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=parent.cget("bg"))

        self.command = command
        self.color = color
        self.hover_color = hover_color

        # Create rounded rectangle
        self.rect = self.round_rectangle(padding, padding,
                                         width-padding*2, height-padding*2,
                                         corner_radius, fill=color, outline="")

        # Add text
        self.text = self.create_text(width/2, height/2, text=text,
                                     fill=text_color, font=font)

        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """
        Create a rounded rectangle
        """
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, e):
        """
        Change color on mouse enter
        """
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, e):
        """
        Change color back on mouse leave
        """
        self.itemconfig(self.rect, fill=self.color)

    def on_click(self, e):
        """
        Execute command on button click
        """
        if self.command:
            self.command()


def main():
    """
    Fungsi main untuk menjalankan aplikasi GUI
    """
    root = tk.Tk()
    WarehouseGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
