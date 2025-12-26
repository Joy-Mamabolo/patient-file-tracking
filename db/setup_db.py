import os
import sqlite3

script_path = os.path.abspath(__file__)
base_dir = os.path.dirname(script_path)

db_path = os.path.join(base_dir,"..","data","patient_file_tracking.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Department table
cursor.execute('DROP TABLE IF EXISTS departments')
cursor.execute('''
    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE
    )
''')

# Status table
cursor.execute('DROP TABLE IF EXISTS statuses')
cursor.execute('''
    CREATE TABLE statuses (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT NOT NULL UNIQUE
    )
''')

# PatientFile table
cursor.execute('DROP TABLE IF EXISTS patient_files')
cursor.execute('''
    CREATE TABLE patient_files (
        file_no INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        dob DATE NOT NULL,
        status_id INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES statuses(status_id)
    )
''')

# Staff table
cursor.execute('DROP TABLE IF EXISTS staff')
cursor.execute('''
    CREATE TABLE staff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        permissions TEXT CHECK (permissions IN ('Super-user', 'Standard User','Special User')) NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
    )
''')

#Insert mock data into departments table
departments = ['Records', 'Radiology', 'Cardiology', 'Maternity']
for dept in departments:
    cursor.execute('INSERT INTO departments (department_name) VALUES (?)', (dept,))

#Insert data into statuses table
statuses = ['Checked In', 'Checked Out', 'Admitted']
for status in statuses:
    cursor.execute('INSERT INTO statuses (status_name) VALUES (?)', (status,))

#Insert mock data into staff table
staff_members = [
    ('John Smith', 'Records', 'Super-user'),
    ('Jane Doe', 'Radiology', 'Standard User'),
    ('Bob Johnson', 'Records', 'Special User'),
    ('Alice Williams', 'Maternity', 'Standard User'),
    ('Charlie Brown', 'Cardiology', 'Standard User')
]
for name, department_name, permissions in staff_members:
    cursor.execute('''
        INSERT INTO staff (name, department_id, permissions)
        SELECT ?, departments.department_id, ?
        FROM departments
        WHERE departments.department_name = ?
    ''', (name, permissions, department_name))

#Insert mock data into patient_files table
patient_files = [
    ('Emily Davis', '1985-04-12', 'Checked In'),
    ('Michael Wilson', '1990-09-23', 'Checked Out'),
    ('Sarah Miller', '1978-11-05', 'Admitted'),
    ('David Anderson', '1965-02-17', 'Checked In'),
    ('Laura Thomas', '2000-07-30', 'Checked Out')
]
for patient_name, dob, status_name in patient_files:
    cursor.execute('''
        INSERT INTO patient_files (patient_name, dob, status_id)
        SELECT ?, ?, statuses.status_id
        FROM statuses
        WHERE statuses.status_name = ?
    ''', (patient_name, dob, status_name))

conn.commit()
conn.close()
print("Database setup with mock data complete.")
