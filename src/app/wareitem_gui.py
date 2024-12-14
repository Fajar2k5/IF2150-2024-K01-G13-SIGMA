"""
GUIT FOR WAREHOUSE ITEM MANAGEMENT
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import warehouseitem
import warehouse
import item


class WarehouseItemGUI:
    """
    Main GUI for warehouse item management
    """
    def __init__(self, root):
        self.root = root

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
        self.setup_warehouseitem_list()
        self.setup_buttons()
        self.refresh_warehouseitem_list()

    def setup_warehouseitem_list(self):
        """
        Setup for warehouse item list
        """
        # Warehouse item list with scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.grid(row=0, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.warehouseitem_tree = ttk.Treeview(list_frame, columns=("ID", "Warehouse", "Item", "Quantity", "Occupied"), show="headings")

        # Define columns
        self.warehouseitem_tree.heading("ID", text="ID")
        self.warehouseitem_tree.heading("Warehouse", text="Warehouse (ID)")
        self.warehouseitem_tree.heading("Item", text="Item (ID)")
        self.warehouseitem_tree.heading("Quantity", text="Quantity")
        self.warehouseitem_tree.heading("Occupied", text="Occupied (%)")

        # Column widths
        self.warehouseitem_tree.column("ID", width=50)
        self.warehouseitem_tree.column("Warehouse", width=200)
        self.warehouseitem_tree.column("Item", width=200)
        self.warehouseitem_tree.column("Quantity", width=100)
        self.warehouseitem_tree.column("Occupied", width=100)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.warehouseitem_tree.yview)
        self.warehouseitem_tree.configure(yscrollcommand=scrollbar.set)

        self.warehouseitem_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    def refresh_warehouseitem_list(self):
        """
        Fetch warehouse item data from database and display in treeview
        """
        # Clear existing items
        for items in self.warehouseitem_tree.get_children():
            self.warehouseitem_tree.delete(items)

        # Connect to database and fetch warehouse items
        conn = sqlite3.connect(warehouseitem.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT wi.id, w.name || ' (' || wi.warehouse_id || ')',
                   i.name || ' (' || wi.item_id || ')', wi.quantity,
                   (wi.quantity * i.volume * 100.0 / w.capacity) AS occupied
            FROM warehouseitem wi
            JOIN Warehouse w ON wi.warehouse_id = w.id
            JOIN items i ON wi.item_id = i.id
        """)
        warehouseitems = cursor.fetchall()
        conn.close()

        # Insert warehouse item data
        for w in warehouseitems:
            self.warehouseitem_tree.insert("", tk.END, values=w)

    def setup_buttons(self):
        """
        Setup for CRUD buttons
        """
        button_font = ('Microsoft YaHei UI Light', 10)
        button_width = 150
        button_height = 40
        button_radius = 10

        # Use tk.Frame instead of ttk.Frame
        button_frame = tk.Frame(self.main_frame, bg='#F0F0F0')
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)

        # CRUD Buttons with consistent styling
        buttons = [
            ("Add Item", self.show_add_dialog),
            ("Edit Qty", self.show_edit_dialog),
            ("Delete Item", self.delete_item),
            ("Refresh", self.refresh_warehouseitem_list),
            ("Move Item", self.show_move_dialog)  # Added Move Item button
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

    def show_move_dialog(self):
        """
        Show dialog to move warehouse item
        """
        selected = self.warehouseitem_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a warehouse item to move")
            return

        items = self.warehouseitem_tree.item(selected[0])
        values = items['values']

        dialog = MoveItemDialog(self.root, "Move Warehouse Item", (values[1][-2]), values[2][-2], values[3])
        if dialog.result:
            source_warehouse_id, target_warehouse_id, item_id, quantity = dialog.result
            warehouseitem.transfer_items(int(source_warehouse_id), int(target_warehouse_id), int(item_id), int(quantity))
            self.refresh_warehouseitem_list()

    def show_add_dialog(self):
        """
        Show dialog to add new warehouse item
        """
        dialog = WarehouseItemDialog(self.root, "Add Warehouse Item")
        if dialog.result:
            warehouse_id, item_id, quantity = dialog.result
            warehouseitem.add_item_to_warehouse(int(warehouse_id), int(item_id), int(quantity))
            self.refresh_warehouseitem_list()

    def show_edit_dialog(self):
        """
        Show dialog to edit warehouse item
        """
        selected = self.warehouseitem_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a warehouse item to edit")
            return

        items = self.warehouseitem_tree.item(selected[0])
        values = items['values']

        dialog = WarehouseItemDialog(self.root, "Edit Warehouse Item", values[1][-2], values[2][-2], values[3])
        if dialog.result:
            warehouse_id, item_id, quantity = dialog.result
            warehouseitem.update_item_quantity(warehouse_id, item_id, quantity)
            self.refresh_warehouseitem_list()

    def delete_item(self):
        """
        Delete selected warehouse item
        """
        selected = self.warehouseitem_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a warehouse item to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this warehouse item?"):
            items = self.warehouseitem_tree.item(selected[0])
            warehouse_id, item_id = items['values'][1][-2], items['values'][2][-2]
            warehouseitem.remove_item_from_warehouse(int(warehouse_id), int(item_id))
            self.refresh_warehouseitem_list()



class MoveItemDialog:
    """
    Dialog to move warehouse item
    """
    def __init__(self, parent, title, warehouse_id="", item_id="", quantity=""):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Form fields
        ttk.Label(self.dialog, text="Source Warehouse ID:").grid(row=0, column=0, pady=5, padx=5)
        self.source_warehouse_id_label = ttk.Label(self.dialog, text=warehouse_id, anchor="w")
        self.source_warehouse_id_label.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(self.dialog, text="Target Warehouse ID:").grid(row=1, column=0, pady=5, padx=5)
        self.target_warehouse_id_entry = ttk.Entry(self.dialog, width=40)
        self.target_warehouse_id_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.dialog, text="Item ID:").grid(row=2, column=0, pady=5, padx=5)
        self.item_id_label = ttk.Label(self.dialog, text=item_id, anchor="w")
        self.item_id_label.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(self.dialog, text="Quantity:").grid(row=3, column=0, pady=5, padx=5)
        self.quantity_entry = ttk.Entry(self.dialog, width=40)
        self.quantity_entry.insert(0, quantity)
        self.quantity_entry.grid(row=3, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Move", command=self.move).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=1, padx=5)

        # Center the dialog
        self.dialog.wait_window()

    def move(self):
        """
        Validate and move warehouse item data
        """
        source_warehouse_id = self.source_warehouse_id_label.cget("text").strip()
        target_warehouse_id = self.target_warehouse_id_entry.get().strip()
        item_id = self.item_id_label.cget("text").strip()
        quantity = self.quantity_entry.get().strip()

        if not all([source_warehouse_id, target_warehouse_id, item_id, quantity]):
            messagebox.showwarning("Validation Error", "All fields are required")
            return

        try:
            source_warehouse_id = int(source_warehouse_id)
            target_warehouse_id = int(target_warehouse_id)
            item_id = int(item_id)
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Quantity must be a positive integer")
            return

        self.result = (source_warehouse_id, target_warehouse_id, item_id, quantity)
        self.dialog.destroy()
        
    
class WarehouseItemDialog:
    """
    Dialog to add or edit warehouse item
    """
    def __init__(self, parent, title, warehouse_id="", item_id="", quantity=""):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Form fields
        ttk.Label(self.dialog, text="Warehouse ID:").grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(self.dialog, text=warehouse_id, anchor="w").grid(row=0, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(self.dialog, text="Item ID:").grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(self.dialog, text=item_id, anchor="w").grid(row=1, column=1, pady=5, padx=5, sticky="w")

        ttk.Label(self.dialog, text="Quantity:").grid(row=2, column=0, pady=5, padx=5)
        self.quantity_entry = ttk.Entry(self.dialog, width=40)
        self.quantity_entry.insert(0, quantity)
        self.quantity_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Save", command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=1, padx=5)

        # Center the dialog
        self.dialog.wait_window()

    def save(self):
        """
        Validate and save warehouse item data
        """
        warehouse_id = self.warehouse_id_entry.get().strip()
        item_id = self.item_id_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if not all([warehouse_id, item_id, quantity]):
            messagebox.showwarning("Validation Error", "All fields are required")
            return

        try:
            warehouse_id = int(warehouse_id)
            item_id = int(item_id)
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Validation Error", "Quantity must be a positive integer")
            return

        self.result = (warehouse_id, item_id, quantity)
        self.dialog.destroy()


class RoundedButton(tk.Canvas):
    """
    Custom button widget with rounded corners
    """
    def __init__(self, parent, text, command, width=150, height=40, corner_radius=10, padding=0, color="#6666FF", text_color="white", hover_color="#7777FF", font=None):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget("bg"))

        self.command = command
        self.color = color
        self.hover_color = hover_color

        # Create rounded rectangle
        self.rect = self.round_rectangle(padding, padding, width-padding*2, height-padding*2, corner_radius, fill=color, outline="")

        # Add text
        self.text = self.create_text(width/2, height/2, text=text, fill=text_color, font=font)

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
    Main function to run the GUI application
    """
    root = tk.Tk()
    WarehouseItemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
