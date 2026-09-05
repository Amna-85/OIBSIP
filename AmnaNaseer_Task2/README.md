# Advanced BMI Tracker & Visualizer

A modular desktop application built with Python, Tkinter, SQLite, and Matplotlib. It calculates Body Mass Index (BMI), provides color-coded category feedback, supports multi-user tracking, and visualizes historical health trends over time.

---

## Features

- Tkinter GUI Interface: Modern desktop user interface with flat card styling and custom TTK component themes.
- Color-Coded Visual Feedback: Immediate visual feedback with standard BMI categories:
- Blue: Underweight (< 18.5)
- Green: Normal Weight (18.5 – 24.9)
- Orange: Overweight (25.0 – 29.9)
- Red: Obese (≥ 30.0)
- Defensive Input Validation: Error handling that flags non-numeric strings, blank entries, zero values, negative numbers, and unrealistic human ranges.
- Multi-User Support: Create, switch, and manage distinct historical tracking records across multiple named user profiles.
- Data Persistence: Relational data storage using an embedded SQLite database (`bmi_tracker.db`).
- Trend Visualization: Integrated Matplotlib line plot displaying historical progress over time alongside reference threshold lines.

---

## Technologies Used

- **Language:** Python 3.8+
- **GUI Framework:** `tkinter` / `tkinter.ttk`
- **Data Persistence:** `sqlite3`
- **Data Visualization:** `matplotlib`

---

## Project Structure

```text
AmnaNaseer_Task2/
│
├── .gitignore       # Excludes local databases, IDE settings, and bytecode
├── README.md        # Project documentation and setup guide
├── app.py           # Presentation Layer (Tkinter GUI & Matplotlib canvas)
├── bmi_logic.py     # Business Logic Layer (BMI calculations & input validation)
└── database.py      # Data Access Layer (SQLite CRUD queries & table init)
├── app.py           # Presentation Layer (Tkinter GUI & Matplotlib canvas)
├── bmi_logic.py     # Business Logic Layer (BMI calculations & input validation)
└── database.py      # Data Access Layer (SQLite CRUD queries & table init)
