import sqlite3

conn = sqlite3.connect("database/sample.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER,
    join_date TEXT
)
""")

cur.execute("DELETE FROM employees")

cur.executemany("""
INSERT INTO employees (name, department, salary, join_date)
VALUES (?, ?, ?, ?)
""", [
    ("Ali", "IT", 50000, "2022-01-10"),
    ("Sara", "HR", 60000, "2021-06-15"),
    ("John", "Finance", 75000, "2020-09-01"),
    ("Ayesha", "IT", 90000, "2023-03-20")
])

conn.commit()
conn.close()

print("Database ready!")