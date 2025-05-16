# ExpenseEase - Professional Expense Tracker 🧾💰

**ExpenseEase** is a Tkinter-based desktop application built in Python for managing income, expenses, and budgets professionally. It is lightweight, easy to use, and helps users stay financially aware by tracking their monthly financial activities.

---

## 🚀 Features

### 📌 Income Management
- Add income entries with source, amount, and date.
- Update existing income records directly.
- Delete income entries as needed.
- Visualize all income entries in a table format.

### 📌 Expense Management
- Add expense entries with category, amount, and optional receipt image.
- Upload receipt images for documentation.
- Update or delete individual expense records.
- Real-time display of all expense entries.

### 📌 Budget Management
- Set a monthly budget limit.
- Delete/reset the budget as needed.
- Budget warning alert if expenses exceed the set limit.

### 📊 Summary Dashboard
- View total income, total expense, remaining balance, and monthly budget.
- Real-time auto-refresh of financial summaries.

### ⚠️ Smart Alerts
- Automatic popup alert when your expenses exceed your set monthly budget.

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** for GUI
- **SQLite** for local database storage

---

## 📂 Project Structure

```
ExpenseEase/
│
├── expenses.db           # SQLite database (auto-created)
├── main.py               # Main Python application
└── README.md             # This file
```

---

## 🧑‍💻 How to Run

1. Make sure Python 3 is installed.
2. Save the code in a file named `main.py`.
3. Run the application:

```bash
python main.py
```

The SQLite database (`expenses.db`) will be created automatically on first run.

---


## 💡 Future Enhancements

- Export data to Excel or PDF.
- Charts for visual insights (Pie/Bar Graphs).
- Dark mode toggle.
- Multi-user support.
- Cloud sync.
