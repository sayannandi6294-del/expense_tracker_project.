# 💰 Daily Expense Tracker – Python Project

A complete desktop application built using Python and Tkinter for recording, managing, tracking, and analysing daily expenses.

## 🚀 Features

- Add daily expenses
- Select expense categories:
  - Food
  - Travel
  - Education
  - Shopping
  - Bills
  - Entertainment
  - Health
  - Other
- Calculate total expenditure
- Calculate category-wise expenditure
- Display highest expenditure
- Generate monthly expense reports
- View complete expense history
- Filter expenses by month
- Delete selected expenses
- Export expense records to CSV
- Save monthly reports as TXT files
- SQLite database for permanent local storage
- Interactive dashboard displaying:
  - Total expenditure
  - Current-month expenditure
  - Highest expense
  - Total transaction count

## 🛠️ Technologies Used

- Python 3.9+
- Tkinter (GUI)
- SQLite3 (Database)
- CSV (Data Export)
- File Handling

## 📋 Requirements

- Python 3.9 or newer
- Tkinter
- SQLite3

**No third-party Python packages are required.**

## ▶️ How to Run

1. Download or clone the project repository.
2. Extract the project folder.
3. Open the project folder in VS Code.
4. Open the terminal.
5. Run the following command:

```bash
python expense_tracker.py
```

The application automatically creates an `expenses.db` database file in the project folder.

## 📖 How to Use

### 1. Add Expense

Enter the following information:

- Date in YYYY-MM-DD format
- Expense description
- Expense category
- Amount in rupees

Click the **Add Expense** button to save the record.

### 2. Expense History

- View all recorded expenses.
- Filter records by month.
- Click Show All to display all records.
- Select records and click Delete Selected.
- Click Export CSV to export expense records.

### 3. Expense Analysis

Enter a month in YYYY-MM format and click Analyse.

The application displays:

- Category-wise expenditure
- Percentage share of each category
- Highest expense
- Total monthly expenditure

### 4. Monthly Report

Enter a month and click Generate Report.

The monthly report includes:

- Total expenditure
- Number of transactions
- Average expense
- Highest expense
- Category-wise expenditure
- Percentage distribution
- Detailed expense list

Click **Save Report** to save the report as a TXT file.

## 📸 Screenshots

This section showcases the graphical user interface (GUI) and important features of the Daily Expense Tracker application.

### 1. Main Dashboard

Displays total expenditure, current-month expenditure, highest expense and total transaction count.

![Main Dashboard]<img width="1917" height="1042" alt="Screenshot 2026-11-01 224858" src="https://github.com/user-attachments/assets/9cd3feb2-6e6f-4493-afb4-82bec90d5eb4" />

### 2.Select Expense Categories

Allows users to select from the following expense categories while adding a new expense.

![Select Expense Categories]<img width="1917" height="1037" alt="Screenshot 2026-11-01 224940" src="https://github.com/user-attachments/assets/03d31aef-0651-4204-bdf3-2376ad7a6742" />

### 3. Add Expense

Allows users to enter expense details, including date, description, category and amount.

![Add Expense]<img width="1917" height="1037" alt="Screenshot 2026-11-01 225158" src="https://github.com/user-attachments/assets/37950693-8d28-4bad-ad48-8902ad8d898f" />

### 4. Expense History

Displays recorded expenses with options to filter and delete selected records.

![Expense History]<img width="1917" height="1038" alt="Screenshot 2026-11-01 225402" src="https://github.com/user-attachments/assets/436ae838-be1b-44af-a506-b57fa93fefb7" />

### 5. Expense Analysis

Displays category-wise expenditure, percentage distribution and highest expenditure.

![Expense Analysis]<img width="1915" height="1037" alt="Screenshot 2026-11-01 225511" src="https://github.com/user-attachments/assets/eaa96ab2-1174-42a2-be3d-0c1a91c73e71" />

### 6. Monthly Report

Displays monthly financial summaries and detailed expense records.

![Monthly Report]<img width="1917" height="1008" alt="Screenshot 2026-11-01 225545" src="https://github.com/user-attachments/assets/22b180a5-067c-432b-a9ad-25004c98b1d0" />

## 📁 Project Structure

```text
Daily_Expense_Tracker/
│
├── expense_tracker.py
├── README.md
│
├── screenshots/
│   ├── dashboard.png
│   ├── add_expense.png
│   ├── expense_history.png
│   ├── analysis.png
│   ├── monthly_report.png
│   └── export_csv.png
│
└── expenses.db
```

**Note:** The `expenses.db` file is automatically created when the application runs for the first time.

## 🗄️ Database Design

**Database:** SQLite

**Table:** expenses

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary Key |
| expense_date | TEXT | Date of expense |
| description | TEXT | Expense description |
| category | TEXT | Expense category |
| amount | REAL | Expense amount |

## 🧠 Concepts Demonstrated

This project demonstrates practical implementation of:

- Python Functions and Classes
- Object-Oriented Programming (OOP)
- Tkinter GUI Development
- SQLite Database Connectivity
- CRUD Operations
- Input Validation
- SQL Aggregate Functions
- Category-wise Data Analysis
- File Handling
- CSV Export
- Monthly Report Generation
- Exception Handling

## 🔮 Future Improvements

- Pie and Bar Charts using Matplotlib
- User Login and Registration
- Monthly Budget Limits and Alerts
- Search Expenses by Description
- PDF Report Generation
- Excel Export
- Database Backup and Restore
- Recurring Expenses
- Income vs Expenditure Analysis

## 🎯 Project Objective

The main objective of this project is to develop a simple and user-friendly desktop application that helps users manage their daily expenses, monitor spending habits, analyse monthly expenditure and maintain financial records efficiently.

## 👨‍💻 Developer

**Developed using Python**

**Project Name:** Daily Expense Tracker

**Category:** Python Desktop Application

**Domain:** Personal Finance Management

---

⭐ If you find this project useful, consider giving it a star on GitHub!

