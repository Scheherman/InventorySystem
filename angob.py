import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the SQLite database file
db_file = os.path.join(script_dir, "inventory.db")

# Centralized function to create or connect to the database
def connect_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return conn, cursor

# Check if the database file exists, create it if not
if not os.path.exists(db_file):
    conn, cursor = connect_database()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        ID INTEGER PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Price REAL NOT NULL,
                        Quantity INTEGER NOT NULL,
                        Units TEXT NOT NULL,
                        Descriptions TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    print("Database created successfully at:", db_file)
else:
    print("Database already exists at:", db_file)

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x700+0+0")
        self.title("Inventory Management System")
        self.resizable(False, False)
        
        # Title label
        lbl_title = tk.Label(self, bd=15, relief=tk.RIDGE, text="INVENTORY MANAGEMENT SYSTEM", fg="blue", bg="linen", font=("times new roman", 20, "bold"))
        lbl_title.pack(side=tk.TOP, fill=tk.X)
        
        # Treeview widget
        tree_frame = tk.Frame(self, bd=15, relief=tk.RIDGE, width=700, height=500)
        tree_frame.place(x=0, y=65)
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Quantity", "Units", "Descriptions"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Units", text="Units")
        self.tree.heading("Descriptions", text="Descriptions")
        # Center align all columns
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Create the database and populate Treeview
        self.create_database()
        self.update_treeview()

        # Main functions
        self.create_buttons()
        self.create_menubar()

    # Function to create or connect to the database
    def create_database(self):
        self.conn, self.cursor = connect_database()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        ID INTEGER PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Price REAL NOT NULL,
                        Quantity INTEGER NOT NULL,
                        Units TEXT NOT NULL,
                        Descriptions TEXT NOT NULL)''')
        self.conn.commit()

    # Update the Treeview function
    def update_treeview(self):
        # Clear existing data
        self.tree.delete(*self.tree.get_children())

        # Retrieve data from the SQLite database and insert it into the Treeview
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    # Button widgets below Treeview    
    def create_buttons(self):
        # Button frame for buttons
        button_frame = tk.Frame(self, bd=15, relief=tk.RIDGE, width=700, height=70)
        button_frame.place(x=0, y=335)
        
        # Add a new product
        btn_add = tk.Button(button_frame, command=self.add_product_window, text="Add", fg="white", bg="green", font=("times new roman", 15, "bold"), width=17, height=1, padx=4, pady=6)
        btn_add.grid(row=0, column=0)
        
        # Remove a product
        btn_remove = tk.Button(button_frame, command=self.remove_selected_item, text="Remove", bg="red", fg="white", font=("times new roman", 15, "bold"), width=17, height=1, padx=4, pady=6)
        btn_remove.grid(row=0, column=1)
        
        # View all products
        btn_view = tk.Button(button_frame, command=self.view_product_window, text="View", fg="white", bg="green", font=("times new roman", 15, "bold"), width=18, height=1, padx=4, pady=6)
        btn_view.grid(row=0, column=2)
        
        # Update an existing product
        btn_update = tk.Button(button_frame, command=self.update_product_window, text="Update", bg="green", fg="white", font=("times new roman", 15, "bold"), width=16, height=1, padx=4, pady=6)
        btn_update.grid(row=0, column=3)
        
        # Exit the application
        btn_exit = tk.Button(button_frame, command=self.exit_confirmation, text="Exit", bg="red", fg="white", font=("times new roman", 15, "bold"), width=14, height=1, padx=4, pady=6)
        btn_exit.grid(row=0, column=4)

        # Exit window (x)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)

    # Functions for the buttons

    # Add product window function
    def add_product_window(self):
        def add_product():
            # Retrieve data from entry fields
            name = name_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()
            units = units_entry.get()
            descriptions = descriptions_entry.get()
            
            # Validate name (letters and spaces only)
            if not name.replace(" ", "").isalpha():
                messagebox.showerror("Invalid Input", "Name should contain only letters or spaces.")
                return
            
            # Validate price and quantity (numbers only)
            try:
                price = float(price)
                quantity = int(quantity.replace(",", ""))  # Remove commas before converting to integer
            except ValueError:
                messagebox.showerror("Invalid Input", "Price and Quantity should contain only numbers.")
                return
            
            # Insert data into the database
            self.cursor.execute("INSERT INTO products (Name, Price, Quantity, Units, Descriptions) VALUES (?, ?, ?, ?, ?)", (name, price, quantity, units, descriptions))
            self.conn.commit()
            
            # Refresh the Treeview to display the newly added product
            self.update_treeview()
            add_window.destroy()
        
        # Open a new window for adding a product
        add_window = tk.Toplevel(self)
        add_window.geometry("300x300")
        add_window.title("Add Product")
        add_window.resizable(False, False)
        add_window.configure(bd=20, relief=tk.RIDGE)
        
        # Label and entry for Name
        name_label = tk.Label(add_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        
        # Label and entry for Price
        price_label = tk.Label(add_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()
        
        # Label and entry for Quantity
        quantity_label = tk.Label(add_window, text="Quantity:")
        quantity_label.pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()
        
        
        units_label = tk.Label(add_window, text="Units:")
        units_label.pack()
        units_entry = tk.Entry(add_window)
        units_entry.pack() 
        
        # Label and entry for Descriptions
        descriptions_label = tk.Label(add_window, text="Descriptions:")
        descriptions_label.pack()
        descriptions_entry = tk.Entry(add_window)
        descriptions_entry.pack()
        
        
        # Button to add product
        add_button = tk.Button(add_window, text="Add", command=add_product, bg="green", fg="white", width=10)
        add_button.pack()

    # View product window function    
    def view_product_window(self):
        def search_products(keyword):
            def go_back():
                result_window.destroy()
                view_window.deiconify()

            result_window = tk.Toplevel(view_window)
            result_window.title("Search Results")
            result_window.geometry("840x100")
            result_window.resizable(False, False)

            tree = ttk.Treeview(result_window, columns=("ID", "Name", "Price", "Quantity", "Units", "Descriptions"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Price", text="Price")
            tree.heading("Quantity", text="Quantity")
            tree.heading("Units", text="Units")
            tree.heading("Descriptions", text="Descriptions")
            
            for col in tree["columns"]:
                tree.column(col, anchor="center")

            conn, cursor = connect_database()

            # Perform search based on the keyword
            cursor.execute("SELECT * FROM products WHERE ID=? OR Name LIKE ? OR Price=? OR Quantity=? OR Units=? Or Descriptions LIKE ?", (keyword, f'%{keyword}%', keyword, keyword, keyword, f'%{keyword}%'))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("No Results", "No products found matching the search criteria.")
            else:
                for row in rows:
                    tree.insert("", "end", values=row)

            tree.pack(expand=True, fill="both", padx=5, pady=5)

            back_button = tk.Button(result_window, text="Back", command=go_back, bg="gray", fg="white", width=10)
            back_button.pack(pady=5)

            cursor.close()
            conn.close()

        view_window = tk.Toplevel(self)
        view_window.geometry("400x150")
        view_window.title("View Product")
        view_window.resizable(False, False)
        view_window.configure(bd=20, relief=tk.RIDGE)

        # Label and entry for search
        search_label = tk.Label(view_window, text="Enter search keyword:")
        search_label.pack()
        search_entry = tk.Entry(view_window)
        search_entry.pack()

        # Button to view products
        view_button = tk.Button(view_window, text="Search", command=lambda: search_products(search_entry.get()), bg="green", fg="white", width=10)
        view_button.pack()

    # Remove product function
    def remove_selected_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return

        confirm = messagebox.askyesno("Confirm Removal", "Are you sure you want to remove the selected item?")
        if confirm:
            for item in selected_item:
                item_id = self.tree.item(item, "values")[0]
                self.cursor.execute("DELETE FROM products WHERE ID=?", (item_id,))
            self.conn.commit()
            self.update_treeview()
            messagebox.showinfo("Item Removed", "Selected item(s) removed successfully.")

    # Update product window function
    def update_product_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to update.")
            return

        item_id = self.tree.item(selected_item[0], "values")[0]

        def update_product():
            name = name_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()
            units = units_entry.get()
            descriptions = descriptions_entry.get()
            
            if not name.replace(" ", "").isalpha():
                messagebox.showerror("Invalid Input", "Name should contain only letters or spaces.")
                return
            try:
                price = float(price)
                quantity = int(quantity.replace(",", ""))
            except ValueError:
                messagebox.showerror("Invalid Input", "Price and Quantity should contain only numbers.")
                return

            self.cursor.execute("UPDATE products SET Name=?, Price=?, Quantity=?, Units=?, Descriptions=? WHERE ID=?", (name, price, quantity, units, descriptions, item_id))
            self.conn.commit()
            self.update_treeview()
            update_window.destroy()

        update_window = tk.Toplevel(self)
        update_window.geometry("300x300")
        update_window.title("Update Product")
        update_window.resizable(False, False)
        update_window.configure(bd=20, relief=tk.RIDGE)

        name_label = tk.Label(update_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        price_label = tk.Label(update_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(update_window)
        price_entry.pack()

        quantity_label = tk.Label(update_window, text="Quantity:")
        quantity_label.pack()
        quantity_entry = tk.Entry(update_window)
        quantity_entry.pack()

        units_label = tk.Label(update_window, text="Units:")
        units_label.pack()
        units_entry = tk.Entry(update_window)
        units_entry.pack()
        
        descriptions_label = tk.Label(update_window, text="Descriptions:")
        descriptions_label.pack()
        descriptions_entry = tk.Entry(update_window)
        descriptions_entry.pack()
        


        update_button = tk.Button(update_window, text="Update", command=update_product, bg="green", fg="white", width=10)
        update_button.pack()

        self.cursor.execute("SELECT * FROM products WHERE ID=?", (item_id,))
        product = self.cursor.fetchone()
        name_entry.insert(0, product[1])
        price_entry.insert(0, product[2])
        quantity_entry.insert(0, product[3])
        units_entry.insert(0, product[4])
        descriptions_entry.insert(0, product[5])

    # Confirm exit function
    def exit_confirmation(self):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
        if confirm:
            self.conn.close()
            self.destroy()

    # Export data function
    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.cursor.execute("SELECT * FROM products")
            rows = self.cursor.fetchall()

            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Price", "Quantity", "Units", "Descriptions"])
                writer.writerows(rows)

            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

    # Menu bar function
    def create_menubar(self):
        menubar = tk.Menu(self)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Export", command=self.export_data)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_confirmation)
        menubar.add_cascade(label="File", menu=filemenu)
        
        self.config(menu=menubar)

if __name__ == "__main__":
    app = Gui()
    app.mainloop()
