import pandas as pd
import json

# Task 1 - Part 1
data = {
    "Name" : ['Alice', 'Bob', 'Charlie'],
    "Age" : [25, 30, 35],
    "City": ['New York', 'Los Angeles', 'Chicago'],
}

task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

# Task 1 - Part 2
task1_with_salary = task1_data_frame.copy()
task1_with_salary["Salary"] = [70000, 80000, 90000]
print(task1_with_salary)

# Task 1 - Part 3
task1_older = task1_with_salary.copy()
task1_older["Age"] += 1
print(task1_older)

# Task 1 - Part 4
task1_older.to_csv("employees.csv", index = False)

#################

# Task 2 - Part 1
task2_employees = pd.read_csv("employees.csv")
print(task2_employees)

# Task 2 - Part 2
data = {
	"Name" : ["Eve", "Frank"],
	"Age" : [28, 40],
 	"City" : ["Miami", "Seattle"],
	"Salary" : [60000, 95000]
}

with open("additional_employees.json", "w") as json_file:
    json.dump(data, json_file)
    
json_employees = pd.read_json("additional_employees.json")
print(json_employees)

# Task 2 - Part 3
more_employees = pd.concat([task2_employees, json_employees], ignore_index = True)
print(more_employees)

#################

# Task 3 - Part 1
first_three = more_employees.head(3)
print(first_three)

# Task 3 - Part 2
last_two = more_employees.tail(2)
print(last_two)

# Task 3 - Part 3
employee_shape = more_employees.shape
print(employee_shape)

# Task 3 - Part 4
print(more_employees.info())

#################

# Task 4 - Part 1
dirty_data = pd.read_csv("dirty_data.csv")
print(dirty_data)

clean_data = dirty_data.copy()

# Task 4 - Part 2
clean_data.drop_duplicates(inplace = True)
print(clean_data)

# Task 4 - Part 3
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors = "coerce")
print(clean_data)

# Task 4 - Part 4
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors = "coerce")
print(clean_data)

# Task 4 - Part 5 (Can be combined into one liners)
age_mean = clean_data["Age"].mean()
salary_median = clean_data["Salary"].median()
clean_data["Age"] = clean_data["Age"].fillna(age_mean).astype(int)
clean_data["Salary"] = clean_data["Salary"].fillna(salary_median).astype(int)
print(clean_data)

# Task 4 - Part 6
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], format = "mixed", errors = "coerce")
print(clean_data)

# Task 4 - Part 7
clean_data["Name"] = clean_data["Name"].str.strip().str.upper()
clean_data["Department"] = clean_data["Department"].str.strip().str.upper()
print(clean_data)