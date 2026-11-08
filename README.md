# Daily Expense Tracker – Python Project

A complete desktop application for recording and analysing daily expenses.

## Features

- Add daily expenses
- Select categories:
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
- Generate a simple monthly report
- View expense history
- Filter expenses by month
- Delete selected expenses
- Export expenses to CSV
- Save monthly reports as TXT
- SQLite database for permanent local storage
- Dashboard showing total expenditure, current-month expenditure, highest expense and transaction count

## Requirements

- Python 3.9 or newer
- Tkinter (normally included with standard Python on Windows)
- No third-party Python packages are required.

## How to run

1. Extract the project folder.
2. Open Command Prompt / PowerShell in the project folder.
3. Run:

```text
python expense_tracker.py
```

The application automatically creates `expenses.db` in the same folder.

## How to use

### 1. Add Expense
Enter:
- Date in `YYYY-MM-DD`
- Description
- Category
- Amount in rupees

Click **Add Expense**.

### 2. Expense History
Use the month field to filter records, or click **Show All**.

Select one or more records and click **Delete Selected** to remove them.

Click **Export CSV** to save the selected month's data as a spreadsheet-compatible CSV file.

### 3. Analysis
Enter a month such as `2026-09` and click **Analyse**.

The application displays:
- Category-wise expenditure
- Percentage share of each category
- Highest expense of that month
- Total monthly expenditure

### 4. Monthly Report
Enter a month and click **Generate Report**.

The report contains:
- Total expenditure
- Number of transactions
- Average expense
- Highest expense
- Category-wise expenditure and percentage
- Detailed expense list

Click **Save Report** to save it as a `.txt` file.

## Project structure

```text
expense_tracker_project/
│
├── expense_tracker.py
└── README.md
```

After first run, this is also created automatically:

```text
expenses.db
```

## Database design

Table: `expenses`

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| expense_date | TEXT | Date of expense |
| description | TEXT | Expense description |
| category | TEXT | Expense category |
| amount | REAL | Expense amount |

## Concepts demonstrated

This project is suitable for a Python/college mini-project because it demonstrates:

- Python functions and classes
- Object-oriented programming
- Tkinter GUI
- SQLite database connectivity
- CRUD operations
- Input validation
- SQL aggregation (`SUM`, `MAX`, `COUNT`)
- Category-wise analysis
- File handling
- CSV export
- Report generation
- Exception handling

## Possible future improvements

- Pie/bar charts using Matplotlib
- User login
- Budget limits and alerts
- Search by description
- PDF reports
- Excel export
- Backup/restore
- Recurring expenses
- Income vs expenditure analysis
