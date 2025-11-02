import tkinter as tk
from tkinter import ttk, messagebox
import db

class CanteenApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f8f5f2")
        self.cart = []
        self.total = 0

        # --- Header ---
        header = tk.Label(self.root, text="☕ Modern Café Billing System ☕",
                          font=("Georgia", 26, "bold"), bg="#4e342e", fg="white", pady=15)
        header.pack(fill="x")

        # --- Search Bar ---
        search_frame = tk.Frame(self.root, bg="#f8f5f2")
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="🔍 Search:", font=("Georgia", 14, "bold"),
                 bg="#f8f5f2", fg="#4e342e").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 13), width=30).pack(side="left")
        tk.Button(search_frame, text="Search", bg="#8b4513", fg="white",
                  font=("Arial", 12, "bold"), command=self.search_item).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", bg="#a0522d", fg="white",
                  font=("Arial", 12, "bold"), command=self.show_all_items).pack(side="left", padx=5)

        # --- Main Frame ---
        main_frame = tk.Frame(self.root, bg="#f8f5f2")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # ✅ Adjusted column weights: Menu wider, Bill and Cart equal
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=2)

        # --- Menu Section ---
        menu_frame = tk.Frame(main_frame, bg="#f8f5f2")
        menu_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(menu_frame, text="📋 Menu", font=("Georgia", 20, "bold"),
                 bg="#f8f5f2", fg="#4e342e").pack(pady=10)

        self.canvas = tk.Canvas(menu_frame, bg="#f8f5f2", highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f5f2")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load items
        self.menu_items = db.get_menu()
        self.quantity_vars = {}
        self.display_menu_items(self.menu_items)

        # --- Bill Section (Middle column) ---
        bill_frame = tk.Frame(main_frame, bg="#fff8f0", bd=2, relief="groove")
        bill_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        tk.Label(bill_frame, text="🧾 Bill", font=("Georgia", 18, "bold"),
                 bg="#fff8f0", fg="#4e342e").pack(pady=10)
        self.bill_label = tk.Label(bill_frame, text="", font=("Consolas", 12),
                                   bg="#fdf6f0", fg="black", justify="left",
                                   bd=1, relief="solid", padx=15, pady=10)
        self.bill_label.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Cart Section (Right column) ---
        cart_frame = tk.Frame(main_frame, bg="#fff8f0", bd=2, relief="groove")
        cart_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        tk.Label(cart_frame, text="🛒 Your Cart", font=("Georgia", 18, "bold"),
                 bg="#fff8f0", fg="#4e342e").pack(pady=10)
        self.cart_listbox = tk.Listbox(cart_frame, font=("Consolas", 13), width=40, height=20,
                                       bg="white", fg="#3e2723", relief="flat")
        self.cart_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        self.cart_total_label = tk.Label(cart_frame, text="Total: ₹0", font=("Georgia", 14, "bold"),
                                         bg="#fff8f0", fg="#4e342e")
        self.cart_total_label.pack(pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(cart_frame, bg="#fff8f0")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add to Cart", bg="#a0522d", fg="white",
                  font=("Arial", 13, "bold"), command=self.add_to_cart).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Generate Bill", bg="#6b8e23", fg="white",
                  font=("Arial", 13, "bold"), command=self.generate_bill).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="📊 View Sales Report", bg="#4e342e", fg="white",
                  font=("Arial", 13, "bold"), command=self.view_sales_report).grid(row=1, column=0, columnspan=2, pady=5)

    def display_menu_items(self, items):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.quantity_vars.clear()
        for item_id, name, price, category in items:
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill="x", padx=10, pady=5)
            tk.Label(frame, text=f"{name} ({category})", font=("Georgia", 14, "bold"),
                     bg="white", anchor="w", width=25).grid(row=0, column=0, padx=10, sticky="w")
            tk.Label(frame, text=f"₹{price}", font=("Arial", 12), bg="white").grid(row=0, column=1, padx=10)
            qty = tk.IntVar()
            ttk.Entry(frame, textvariable=qty, width=5).grid(row=0, column=2, padx=10)
            self.quantity_vars[item_id] = qty

    def add_to_cart(self):
        self.cart.clear()
        self.cart_listbox.delete(0, tk.END)
        self.total = 0
        for item_id, qty_var in self.quantity_vars.items():
            qty = qty_var.get()
            if qty > 0:
                item = next(x for x in self.menu_items if x[0] == item_id)
                total_item = item[2] * qty
                self.cart.append((item[1], qty, item[2], total_item))
                self.total += total_item
                self.cart_listbox.insert(tk.END, f"{item[1]:<20} x{qty:<2} ₹{total_item}")
        self.cart_total_label.config(text=f"Total: ₹{self.total}")
        if not self.cart:
            messagebox.showwarning("Empty", "No items selected!")

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "Add items to cart first!")
            return
        db.save_bill(self.total)
        bill = "──────────── BILL ────────────\n"
        for name, qty, price, subtotal in self.cart:
            bill += f"{name:<20} x{qty:<2} ₹{subtotal}\n"
        bill += f"\nTOTAL: ₹{self.total}\n──────────────────────────────"
        self.bill_label.config(text=bill)
        messagebox.showinfo("Saved", "Bill saved successfully!")

    def search_item(self):
        term = self.search_var.get().strip()
        self.menu_items = db.get_menu(term) if term else db.get_menu()
        self.display_menu_items(self.menu_items)

    def show_all_items(self):
        self.menu_items = db.get_menu()
        self.display_menu_items(self.menu_items)

    def view_sales_report(self):
        win = tk.Toplevel(self.root)
        win.title("📊 Sales Report")
        win.geometry("700x500")
        win.config(bg="white")

        tk.Label(win, text="📊 Sales Report", font=("Georgia", 22, "bold"),
                 fg="#4e342e", bg="white").pack(pady=10)

        cols = ("Bill ID", "Total Amount", "Date & Time")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=15)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=200)
        tree.pack(padx=15, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        for bill_id, amount, date in db.get_all_bills():
            tree.insert("", "end", values=(bill_id, f"₹{amount}", date))

        total_sales = db.get_total_sales()
        tk.Label(win, text=f"💰 Total Sales: ₹{total_sales}",
                 font=("Georgia", 16, "bold"), bg="white", fg="#4e342e").pack(pady=10)
