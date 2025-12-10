# Task 3

import csv

with open("../csv/employees.csv", "r") as employees:
    reader = csv.reader(employees)
    rows = []
    for row in reader:
        rows.append(row)
    employees_list = [f"{row[1]} {row[2]}" for row in rows[1::]]
    employees_with_e = [name for name in employees_list if "e" in name]