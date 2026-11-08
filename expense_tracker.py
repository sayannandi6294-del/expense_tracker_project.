import csv
import sqlite3
from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DB_FILE = Path(__file__).with_name("expenses.db")

CATEGORIES = [
    "Food", "Travel", "Education", "Shopping",
    "Bills", "Entertainment", "Health", "Other"
]


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Expense Tracker")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)

        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.create_database()

        self.setup_style()
        self.build_ui()
        self.set_default_values()
        self.refresh_all()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_database(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)
        self.conn.commit()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Card.TFrame", relief="solid", borderwidth=1)
        style.configure("CardTitle.TLabel", font=("Segoe UI", 10))
        style.configure("CardValue.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="Daily Expense Tracker",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Record, analyse and monitor your daily expenditure",
            style="Subtitle.TLabel"
        ).pack(anchor="w")

        # Summary cards
        cards = ttk.Frame(outer)
        cards.pack(fill="x", pady=(0, 15))

        self.total_var = tk.StringVar(value="₹0.00")
        self.month_var = tk.StringVar(value="₹0.00")
        self.highest_var = tk.StringVar(value="₹0.00")
        self.count_var = tk.StringVar(value="0")

        self.make_card(cards, "Total Expenditure", self.total_var, 0)
        self.make_card(cards, "Current Month", self.month_var, 1)
        self.make_card(cards, "Highest Expense", self.highest_var, 2)
        self.make_card(cards, "Transactions", self.count_var, 3)

        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)

        self.add_tab = ttk.Frame(notebook, padding=15)
        self.history_tab = ttk.Frame(notebook, padding=15)
        self.analysis_tab = ttk.Frame(notebook, padding=15)
        self.report_tab = ttk.Frame(notebook, padding=15)

        notebook.add(self.add_tab, text="  Add Expense  ")
        notebook.add(self.history_tab, text="  Expense History  ")
        notebook.add(self.analysis_tab, text="  Analysis  ")
        notebook.add(self.report_tab, text="  Monthly Report  ")

        self.build_add_tab()
        self.build_history_tab()
        self.build_analysis_tab()
        self.build_report_tab()

    def make_card(self, parent, title, variable, column):
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.grid(row=0, column=column, sticky="nsew", padx=5)
        parent.columnconfigure(column, weight=1)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=variable,
                  style="CardValue.TLabel").pack(anchor="w", pady=(4, 0))

    def build_add_tab(self):
        form = ttk.LabelFrame(self.add_tab, text="Enter Expense", padding=18)
        form.pack(fill="x")

        self.date_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(
            row=0, column=0, sticky="w", padx=8, pady=8)
        date_entry = ttk.Entry(form, textvariable=self.date_var, width=25)
        date_entry.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 12))

        ttk.Label(form, text="Description").grid(
            row=0, column=1, sticky="w", padx=8, pady=8)
        ttk.Entry(form, textvariable=self.description_var).grid(
            row=1, column=1, sticky="ew", padx=8, pady=(0, 12))

        ttk.Label(form, text="Category").grid(
            row=0, column=2, sticky="w", padx=8, pady=8)
        self.category_combo = ttk.Combobox(
            form, textvariable=self.category_var,
            values=CATEGORIES, state="readonly"
        )
        self.category_combo.grid(
            row=1, column=2, sticky="ew", padx=8, pady=(0, 12))

        ttk.Label(form, text="Amount (₹)").grid(
            row=0, column=3, sticky="w", padx=8, pady=8)
        amount_entry = ttk.Entry(form, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=3, sticky="ew", padx=8, pady=(0, 12))

        for i in range(4):
            form.columnconfigure(i, weight=1)

        buttons = ttk.Frame(self.add_tab)
        buttons.pack(fill="x", pady=15)
        ttk.Button(buttons, text="Add Expense",
                   command=self.add_expense,
                   style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(buttons, text="Clear",
                   command=self.clear_form).pack(side="left", padx=5)

        help_text = (
            "Tip: Use a clear description such as “Lunch”, “Bus fare”, "
            "“Python book”, or “Groceries”."
        )
        ttk.Label(self.add_tab, text=help_text).pack(anchor="w", pady=10)

    def build_history_tab(self):
        controls = ttk.Frame(self.history_tab)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="Month (YYYY-MM):").pack(side="left")
        self.history_month_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.history_month_var,
                  width=12).pack(side="left", padx=7)

        ttk.Button(controls, text="Filter",
                   command=self.refresh_history).pack(side="left", padx=4)
        ttk.Button(controls, text="Show All",
                   command=self.show_all_history).pack(side="left", padx=4)
        ttk.Button(controls, text="Delete Selected",
                   command=self.delete_selected).pack(side="right", padx=4)
        ttk.Button(controls, text="Export CSV",
                   command=self.export_csv).pack(side="right", padx=4)

        tree_frame = ttk.Frame(self.history_tab)
        tree_frame.pack(fill="both", expand=True)

        columns = ("id", "date", "description", "category", "amount")
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                 show="headings", selectmode="extended")

        headings = {
            "id": "ID",
            "date": "Date",
            "description": "Description",
            "category": "Category",
            "amount": "Amount (₹)"
        }
        widths = {"id": 60, "date": 120, "description": 300,
                  "category": 150, "amount": 130}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col],
                             anchor="e" if col == "amount" else "w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_analysis_tab(self):
        top = ttk.Frame(self.analysis_tab)
        top.pack(fill="x", pady=(0, 10))

        ttk.Label(top, text="Analyse Month (YYYY-MM):").pack(side="left")
        self.analysis_month_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.analysis_month_var,
                  width=12).pack(side="left", padx=7)
        ttk.Button(top, text="Analyse",
                   command=self.refresh_analysis).pack(side="left")

        body = ttk.Frame(self.analysis_tab)
        body.pack(fill="both", expand=True)

        left = ttk.LabelFrame(body, text="Category-wise Expenditure",
                              padding=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 7))

        self.category_tree = ttk.Treeview(
            left, columns=("category", "amount", "percent"),
            show="headings"
        )
        self.category_tree.heading("category", text="Category")
        self.category_tree.heading("amount", text="Amount (₹)")
        self.category_tree.heading("percent", text="Share")
        self.category_tree.column("category", width=180)
        self.category_tree.column("amount", width=130, anchor="e")
        self.category_tree.column("percent", width=100, anchor="e")
        self.category_tree.pack(fill="both", expand=True)

        right = ttk.LabelFrame(body, text="Highest Expenditure",
                               padding=15)
        right.pack(side="right", fill="both", expand=True, padx=(7, 0))

        self.highest_detail = tk.StringVar(
            value="No expense recorded for this month."
        )
        ttk.Label(
            right, textvariable=self.highest_detail,
            font=("Segoe UI", 12), justify="left",
            wraplength=330
        ).pack(anchor="nw", fill="x")

        ttk.Separator(right).pack(fill="x", pady=18)

        self.analysis_total = tk.StringVar(value="Total: ₹0.00")
        ttk.Label(
            right, textvariable=self.analysis_total,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

    def build_report_tab(self):
        controls = ttk.Frame(self.report_tab)
        controls.pack(fill="x", pady=(0, 12))

        ttk.Label(controls, text="Report Month (YYYY-MM):").pack(side="left")
        self.report_month_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.report_month_var,
                  width=12).pack(side="left", padx=7)

        ttk.Button(controls, text="Generate Report",
                   command=self.generate_report).pack(side="left", padx=4)
        ttk.Button(controls, text="Save Report",
                   command=self.save_report).pack(side="left", padx=4)

        self.report_text = tk.Text(
            self.report_tab, wrap="word", font=("Consolas", 10),
            padx=12, pady=12
        )
        self.report_text.pack(fill="both", expand=True)

    def set_default_values(self):
        today = date.today()
        month = today.strftime("%Y-%m")
        self.date_var.set(today.isoformat())
        self.category_var.set(CATEGORIES[0])
        self.history_month_var.set(month)
        self.analysis_month_var.set(month)
        self.report_month_var.set(month)

    def validate_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_expense(self):
        expense_date = self.date_var.get().strip()
        description = self.description_var.get().strip()
        category = self.category_var.get().strip()
        amount_text = self.amount_var.get().strip()

        if not self.validate_date(expense_date):
            messagebox.showerror(
                "Invalid Date",
                "Enter the date in YYYY-MM-DD format."
            )
            return

        if not description:
            messagebox.showerror("Missing Description",
                                 "Please enter a description.")
            return

        if category not in CATEGORIES:
            messagebox.showerror("Invalid Category",
                                 "Please select a valid category.")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Amount must be a positive number."
            )
            return

        self.conn.execute(
            "INSERT INTO expenses (expense_date, description, category, amount) "
            "VALUES (?, ?, ?, ?)",
            (expense_date, description, category, amount)
        )
        self.conn.commit()

        messagebox.showinfo("Expense Added",
                            f"₹{amount:.2f} added successfully.")
        self.clear_form()
        self.refresh_all()

    def clear_form(self):
        self.date_var.set(date.today().isoformat())
        self.description_var.set("")
        self.category_var.set(CATEGORIES[0])
        self.amount_var.set("")

    def fetch_expenses(self, month=None):
        if month:
            return self.conn.execute(
                "SELECT * FROM expenses WHERE expense_date LIKE ? "
                "ORDER BY expense_date DESC, id DESC",
                (month + "-%",)
            ).fetchall()

        return self.conn.execute(
            "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()

    def refresh_history(self):
        month = self.history_month_var.get().strip()
        if not self.valid_month(month):
            messagebox.showerror("Invalid Month",
                                 "Enter month as YYYY-MM.")
            return
        self.populate_history(self.fetch_expenses(month))

    def show_all_history(self):
        self.populate_history(self.fetch_expenses())

    def populate_history(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert(
                "", "end",
                values=(
                    row["id"], row["expense_date"],
                    row["description"], row["category"],
                    f"{row['amount']:.2f}"
                )
            )

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection",
                                   "Select at least one expense.")
            return

        ids = [self.tree.item(item, "values")[0] for item in selected]
        answer = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(ids)} selected expense(s)?"
        )
        if not answer:
            return

        self.conn.executemany(
            "DELETE FROM expenses WHERE id = ?",
            [(expense_id,) for expense_id in ids]
        )
        self.conn.commit()
        self.refresh_all()

    def export_csv(self):
        rows = self.fetch_expenses(self.history_month_var.get().strip()
                                   if self.valid_month(
                                       self.history_month_var.get().strip()
                                   ) else None)
        if not rows:
            messagebox.showinfo("Export CSV", "There are no expenses to export.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Expense CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not filename:
            return

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Description", "Category",
                             "Amount"])
            for row in rows:
                writer.writerow([
                    row["id"], row["expense_date"], row["description"],
                    row["category"], f"{row['amount']:.2f}"
                ])

        messagebox.showinfo("Export Complete",
                            f"CSV saved to:\n{filename}")

    def refresh_analysis(self):
        month = self.analysis_month_var.get().strip()
        if not self.valid_month(month):
            messagebox.showerror("Invalid Month",
                                 "Enter month as YYYY-MM.")
            return

        rows = self.fetch_expenses(month)
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        totals = {}
        grand_total = 0.0

        for row in rows:
            totals[row["category"]] = totals.get(row["category"], 0) + row["amount"]
            grand_total += row["amount"]

        for category, amount in sorted(
            totals.items(), key=lambda item: item[1], reverse=True
        ):
            percent = (amount / grand_total * 100) if grand_total else 0
            self.category_tree.insert(
                "", "end",
                values=(category, f"{amount:.2f}", f"{percent:.1f}%")
            )

        if rows:
            highest = max(rows, key=lambda row: row["amount"])
            self.highest_detail.set(
                f"Description: {highest['description']}\n"
                f"Category: {highest['category']}\n"
                f"Date: {highest['expense_date']}\n"
                f"Amount: ₹{highest['amount']:.2f}"
            )
        else:
            self.highest_detail.set("No expense recorded for this month.")

        self.analysis_total.set(f"Total: ₹{grand_total:.2f}")

    def generate_report(self):
        month = self.report_month_var.get().strip()
        if not self.valid_month(month):
            messagebox.showerror("Invalid Month",
                                 "Enter month as YYYY-MM.")
            return

        rows = self.fetch_expenses(month)
        total = sum(row["amount"] for row in rows)

        category_totals = {}
        for row in rows:
            category_totals[row["category"]] = (
                category_totals.get(row["category"], 0) + row["amount"]
            )

        self.report_text.delete("1.0", "end")
        self.report_text.insert("end", "=" * 58 + "\n")
        self.report_text.insert("end", f"           MONTHLY EXPENSE REPORT - {month}\n")
        self.report_text.insert("end", "=" * 58 + "\n\n")

        self.report_text.insert("end", f"Total expenditure : ₹{total:,.2f}\n")
        self.report_text.insert("end", f"Transactions      : {len(rows)}\n")

        if rows:
            highest = max(rows, key=lambda row: row["amount"])
            average = total / len(rows)
            self.report_text.insert(
                "end", f"Average expense   : ₹{average:,.2f}\n"
            )
            self.report_text.insert(
                "end",
                f"Highest expense   : ₹{highest['amount']:,.2f} "
                f"({highest['description']})\n"
            )
        else:
            self.report_text.insert("end", "Average expense   : ₹0.00\n")
            self.report_text.insert("end", "Highest expense   : ₹0.00\n")

        self.report_text.insert("end", "\nCATEGORY-WISE EXPENDITURE\n")
        self.report_text.insert("end", "-" * 58 + "\n")

        if category_totals:
            for category, amount in sorted(
                category_totals.items(), key=lambda item: item[1], reverse=True
            ):
                share = (amount / total * 100) if total else 0
                self.report_text.insert(
                    "end",
                    f"{category:<18} ₹{amount:>12,.2f}   {share:>5.1f}%\n"
                )
        else:
            self.report_text.insert("end", "No expenses recorded.\n")

        self.report_text.insert("end", "\nEXPENSE DETAILS\n")
        self.report_text.insert("end", "-" * 58 + "\n")

        for row in sorted(rows, key=lambda r: r["expense_date"]):
            self.report_text.insert(
                "end",
                f"{row['expense_date']} | {row['category']:<15} | "
                f"₹{row['amount']:>10,.2f} | {row['description']}\n"
            )

        self.report_text.insert("end", "\n" + "=" * 58 + "\n")
        self.report_text.insert("end", "End of report\n")

    def save_report(self):
        if not self.report_text.get("1.0", "end").strip():
            self.generate_report()

        content = self.report_text.get("1.0", "end").strip()
        if not content:
            return

        filename = filedialog.asksaveasfilename(
            title="Save Monthly Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not filename:
            return

        Path(filename).write_text(content, encoding="utf-8")
        messagebox.showinfo("Report Saved", f"Report saved to:\n{filename}")

    def valid_month(self, value):
        try:
            datetime.strptime(value, "%Y-%m")
            return True
        except ValueError:
            return False

    def refresh_summary(self):
        total = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()[0]

        month = date.today().strftime("%Y-%m")
        month_total = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses "
            "WHERE expense_date LIKE ?",
            (month + "-%",)
        ).fetchone()[0]

        highest = self.conn.execute(
            "SELECT COALESCE(MAX(amount), 0) FROM expenses"
        ).fetchone()[0]

        count = self.conn.execute(
            "SELECT COUNT(*) FROM expenses"
        ).fetchone()[0]

        self.total_var.set(f"₹{total:,.2f}")
        self.month_var.set(f"₹{month_total:,.2f}")
        self.highest_var.set(f"₹{highest:,.2f}")
        self.count_var.set(str(count))

    def refresh_all(self):
        self.refresh_summary()
        self.refresh_history()
        self.refresh_analysis()
        self.generate_report()

    def close_app(self):
        self.conn.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
