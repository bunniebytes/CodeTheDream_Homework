import os, csv, custom_module, traceback
from datetime import datetime

# Task 2
def read_employees():
    employees_dict = {}
    rows = []
    try:
        with open("../csv/employees.csv", "r") as employees_csv:
            reader = csv.reader(employees_csv)
            for row in reader:
                if employees_dict.get("fields"):
                    rows.append(row)
                else:
                    employees_dict["fields"] = row
            employees_dict["rows"] = rows
        return employees_dict           
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

employees = read_employees()

# Task 3
def column_index(string):
    return employees["fields"].index(string)

employee_id_column = column_index("employee_id")

# Task 4
def first_name(row_number):
    idx = column_index("first_name")
    # index of the employee = row_number - 1
    employee = employees["rows"][row_number]
    first_name = employee[idx]
    return first_name

# Task 5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

# Task 7
def sort_by_last_name():
    employees["rows"].sort(key = lambda item : item[column_index("last_name")])
    return employees["rows"]
    
sort_by_last_name()
print(employees)

# Task 8
def employee_dict(row):
    employee_dict = {}
    
    # for x in employees["fields"][1:]:
    #     employee_dict[x] = row[column_index(x)]
    
    # Used zip as requested by hw
    employee_dict = dict(zip(employees["fields"][1:], row[1:]))
    return employee_dict

# Task 9
def all_employees_dict():
    employees_dict = {}
    for row in employees["rows"]:
        employees_dict[row[0]] = employee_dict(row)
    return employees_dict
    
# Task 10
def get_this_value():
    try:
        return os.getenv("THISVALUE")
    except KeyError:
        print("THISVALUE is not set")

# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

# Task 12
def read_minutes():
    def minutes_dict(file):
        minutes_dict = {} 
        with open(file, "r") as minutes:
            reader = csv.reader(minutes)
            rows = []
            for row in reader:
                if minutes_dict.get("fields"):
                    rows.append(tuple(row))
                else:
                    minutes_dict["fields"] = row
            minutes_dict["rows"] = rows
        return minutes_dict
    dict1 = minutes_dict("../csv/minutes1.csv")
    dict2 = minutes_dict("../csv/minutes2.csv")
    return dict1, dict2

minutes1, minutes2 = read_minutes()

# Task 13
def create_minutes_set():
    def create_set(rows):
        return set(rows)
    set1 = create_set(minutes1["rows"])
    set2 = create_set(minutes2["rows"])
    combined_set = set1.union(set2)
    return combined_set

minutes_set = create_minutes_set()

# Task 14
def create_minutes_list():
    minutes_list = [list(item) for item in minutes_set]
    minutes_list_map = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    return minutes_list_map

minutes_list = create_minutes_list()

# Task 15
def write_sorted_list():
    sorted_minutes_list = sorted(minutes_list, key = lambda x : x[1])
    sorted_minutes_list_map = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), sorted_minutes_list))
    with open ("./minutes.csv", "w", newline = "") as minutes:
        writer = csv.writer(minutes)
        writer.writerow(minutes1["fields"])
        writer.writerows(sorted_minutes_list_map)
    return sorted_minutes_list_map

write_sorted_list()