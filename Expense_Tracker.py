import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import datetime
import os

# DB Setup
def setup_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY, source TEXT, amount REAL, date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, category TEXT, amount REAL, receipt TEXT, date TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS budget (id INTEGER PRIMARY KEY, monthly_limit REAL)""")
    conn.commit()
    conn.close()

setup_db()

# Add Income
def add_income():
    source = income_source_entry.get()
    amount = income_amount_entry.get()
    date = datetime.date.today().strftime("%Y-%m-%d")

    if source and amount:
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO income (source, amount, date) VALUES (?, ?, ?)", (source, amount, date))
        conn.commit()
        conn.close()
        update_income_table()
        update_summary()
        income_source_entry.delete(0, tk.END)
        income_amount_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Income Added")
    else:
        messagebox.showerror("Error", "All fields required")

# Add Expense
def add_expense():
    category = expense_category_entry.get()
    amount = expense_amount_entry.get()
    receipt = receipt_path.get()
    date = datetime.date.today().strftime("%Y-%m-%d")

    if category and amount:
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (category, amount, receipt, date) VALUES (?, ?, ?, ?)", (category, amount, receipt, date))
        conn.commit()
        conn.close()
        update_expense_table()
        update_summary()
        expense_category_entry.delete(0, tk.END)
        expense_amount_entry.delete(0, tk.END)
        receipt_path.set("No file selected")
        messagebox.showinfo("Success", "Expense Added")
    else:
        messagebox.showerror("Error", "All fields required")

# Set Budget
def set_budget():
    budget = budget_entry.get()
    if budget:
        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM budget")
        cur.execute("INSERT INTO budget (monthly_limit) VALUES (?)", (budget,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Budget", "Monthly Budget Set")
        update_summary()

# Upload Receipt
def upload_receipt():
    file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file:
        receipt_path.set(file)

# Update Income Treeview
def update_income_table():
    for item in income_tree.get_children():
        income_tree.delete(item)
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT source, amount, date FROM income")
    for row in cur.fetchall():
        income_tree.insert('', tk.END, values=row)
    conn.close()

# Update Expense Treeview
def update_expense_table():
    for item in expense_tree.get_children():
        expense_tree.delete(item)
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT category, amount, date FROM expenses")
    for row in cur.fetchall():
        expense_tree.insert('', tk.END, values=row)
    conn.close()

# Summary
def update_summary():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM income")
    income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(amount) FROM expenses")
    expense = cur.fetchone()[0] or 0

    cur.execute("SELECT monthly_limit FROM budget")
    row = cur.fetchone()
    budget = row[0] if row else 0

    income_label.config(text=f"₹{income:.2f}")
    expense_label.config(text=f"₹{expense:.2f}")
    balance_label.config(text=f"₹{income - expense:.2f}")
    budget_label.config(text=f"₹{budget:.2f}")
    conn.close()

# GUI Setup
root = tk.Tk()
root.title("ExpenseEase - Professional Expense Tracker")
root.geometry("850x600")
root.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
style.configure("Treeview", rowheight=25, font=('Arial', 10))

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Income Frame
income_frame = ttk.Frame(notebook)
expense_frame = ttk.Frame(notebook)
budget_frame = ttk.Frame(notebook)

notebook.add(income_frame, text="Income")
notebook.add(expense_frame, text="Expenses")
notebook.add(budget_frame, text="Budget & Summary")

# INCOME TAB
tk.Label(income_frame, text="Source:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
tk.Label(income_frame, text="Amount:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)

income_source_entry = tk.Entry(income_frame, width=30)
income_amount_entry = tk.Entry(income_frame, width=30)
income_source_entry.grid(row=0, column=1, pady=5)
income_amount_entry.grid(row=1, column=1, pady=5)

tk.Button(income_frame, text="Add Income", command=add_income, bg="#4caf50", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)

income_tree = ttk.Treeview(income_frame, columns=("Source", "Amount", "Date"), show="headings")
income_tree.heading("Source", text="Source")
income_tree.heading("Amount", text="Amount")
income_tree.heading("Date", text="Date")
income_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# EXPENSE TAB
tk.Label(expense_frame, text="Category:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
tk.Label(expense_frame, text="Amount:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5)
tk.Label(expense_frame, text="Receipt:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5)

expense_category_entry = tk.Entry(expense_frame, width=30)
expense_amount_entry = tk.Entry(expense_frame, width=30)
receipt_path = tk.StringVar()
receipt_label = tk.Label(expense_frame, textvariable=receipt_path, font=("Arial", 9), fg="gray")
receipt_path.set("No file selected")

expense_category_entry.grid(row=0, column=1, pady=5)
expense_amount_entry.grid(row=1, column=1, pady=5)
receipt_label.grid(row=2, column=1, pady=5)

tk.Button(expense_frame, text="Upload Receipt", command=upload_receipt, bg="#2196f3", fg="white", width=20).grid(row=3, column=1, pady=5)
tk.Button(expense_frame, text="Add Expense", command=add_expense, bg="#f44336", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=10)

expense_tree = ttk.Treeview(expense_frame, columns=("Category", "Amount", "Date"), show="headings")
expense_tree.heading("Category", text="Category")
expense_tree.heading("Amount", text="Amount")
expense_tree.heading("Date", text="Date")
expense_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# BUDGET & SUMMARY
tk.Label(budget_frame, text="Monthly Budget:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
budget_entry = tk.Entry(budget_frame, width=30)
budget_entry.grid(row=0, column=1, pady=5)
tk.Button(budget_frame, text="Set Budget", command=set_budget, bg="#9c27b0", fg="white", width=20).grid(row=1, column=0, columnspan=2, pady=10)

tk.Label(budget_frame, text="Total Income:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
tk.Label(budget_frame, text="Total Expense:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
tk.Label(budget_frame, text="Balance:", font=("Arial", 11)).grid(row=4, column=0, padx=10, pady=5, sticky='e')
tk.Label(budget_frame, text="Budget Limit:", font=("Arial", 11)).grid(row=5, column=0, padx=10, pady=5, sticky='e')

income_label = tk.Label(budget_frame, text="₹0.00", font=("Arial", 11))
expense_label = tk.Label(budget_frame, text="₹0.00", font=("Arial", 11))
balance_label = tk.Label(budget_frame, text="₹0.00", font=("Arial", 11))
budget_label = tk.Label(budget_frame, text="₹0.00", font=("Arial", 11))

income_label.grid(row=2, column=1, sticky="w")
expense_label.grid(row=3, column=1, sticky="w")
balance_label.grid(row=4, column=1, sticky="w")
budget_label.grid(row=5, column=1, sticky="w")

# Initialize data
update_income_table()
update_expense_table()
update_summary()

root.mainloop()
