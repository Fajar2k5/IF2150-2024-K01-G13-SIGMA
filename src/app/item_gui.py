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
        button_font = ('Microsoft YaHei UI Light', 10)
        button_width = 120
        button_height = 40
        button_radius = 10

        # Use tk.Frame instead of ttk.Frame
        button_frame = tk.Frame(self.main_frame, bg='#F0F0F0')
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)

        # CRUD Buttons with consistent styling
        buttons = [
            ("Add Item", self.show_add_dialog),
            ("Edit Item", self.show_edit_dialog),
            ("Delete Item", self.delete_item),
            ("Refresh", self.refresh_item_list),
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
        Menampilkan semua data item yang dipilih dalam jendela pop-up
        """
        selected = self.item_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select an item to expand")
            return

        items = self.item_tree.item(selected[0])
        values = items['values']

        # Create pop-up window
        expand_dialog = tk.Toplevel(self.root)
        expand_dialog.title("Expand Item")
        expand_dialog.geometry("400x300")

        # Display item details
        ttk.Label(expand_dialog, text="ID:").grid(row=0, column=0, pady=5, padx=5)
        ttk.Label(expand_dialog, text=values[0], anchor=tk.W).grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(expand_dialog, text="Name:").grid(row=1, column=0, pady=5, padx=5)
        ttk.Label(expand_dialog, text=values[1], anchor=tk.W).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(expand_dialog, text="Description:").grid(row=2, column=0, pady=5, padx=5)

        # Scrollable description
        desc_frame = ttk.Frame(expand_dialog)
        desc_frame.grid(row=2, column=1, pady=5, padx=5)
        desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=10, width=30)
        desc_text.insert(tk.END, values[2])
        desc_text.config(state=tk.DISABLED)
        desc_text.grid(row=0, column=0)

        desc_scrollbar = ttk.Scrollbar(desc_frame, orient=tk.VERTICAL, command=desc_text.yview)
        desc_text.config(yscrollcommand=desc_scrollbar.set)
        desc_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        ttk.Label(expand_dialog, text="Volume:").grid(row=3, column=0, pady=5, padx=5)
        ttk.Label(expand_dialog, text=values[3], anchor=tk.W).grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

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
            success, message = item.update_item(values[0], name, desc, float(volume))
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_warehouse_list()
            else:
                messagebox.showerror("Edit Item", message)
            
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
    ItemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
