import sqlite3
from contextlib import closing
from datetime import date

# Task 1
def main():
    with closing(sqlite3.connect("../db/lesson.db")) as conn:
        print("Database successfully opened")
        conn.execute("PRAGMA foreign_keys = 1")

        # Task 1 Part 2
        total_order_price = find_total_order_price(conn, 5)
        print(total_order_price)
        
        # Task 2 Part 2
        customer_avg = customer_order_avg(conn)
        print(customer_avg)
        
        # Task 3 Part 2
        order_id = create_new_order(conn, "Perez and Sons", "Miranda Harris", 5, 10)
        order = find_order(conn, order_id)
        print(order)
        
        # Task 4 Part 2
        temp = find_employee_order_count(conn)
        print(temp)

    print("Database has been closed")

# Task 1 Part 1
def find_total_order_price(conn, limit):
    cursor = conn.cursor()
    query = f"SELECT o.order_id, sum(p.price * li.quantity) FROM orders AS o JOIN line_items AS li ON o.order_id = li.order_id JOIN products AS p ON p.product_id = li.product_id GROUP BY o.order_id ORDER BY o.order_id LIMIT {limit}"
    cursor.execute(query)
    try:
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
        
    return data

# Task 2 Part 1
def customer_order_avg(conn):
    cursor = conn.cursor()
    query = "SELECT c.customer_name, avg(total_price) FROM customers AS c LEFT JOIN (SELECT o.customer_id AS customer_id_b, sum(p.price * li.quantity) AS total_price FROM orders AS o JOIN line_items AS li ON o.order_id = li.order_id JOIN products AS p ON p.product_id = li.product_id GROUP BY o.order_id) AS order_avg_query ON c.customer_id = customer_id_b GROUP BY customer_id"
    
    cursor.execute(query)
    try:
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
        
    return data

# Task 3 Part 1 
def find_cust_id(conn, cust_name):
    cursor = conn.cursor()
    query = "SELECT customer_id FROM customers WHERE customer_name = ?"
    cursor.execute(query, (cust_name,))
    try:
        data = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
    if data:
        return data[0]
    else:
        print("No customer record found.  Please create a new record")
        
def find_employee_id(conn, employee_name):
    cursor = conn.cursor()
    first_name, last_name = employee_name.split(" ")
    query = "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?"
    cursor.execute(query, (first_name, last_name))
    try:
        data = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
    if data:
        return data[0]
    else:
        print("No employee record found.  Please double check name")
        
def find_cheapest_products(conn, limit):
    cursor = conn.cursor()
    query = f"SELECT product_id FROM products ORDER BY price ASC LIMIT {limit}"
    cursor.execute(query)
    try:
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
    if len(data) == limit:
        data = [row[0] for row in data]
        return data
    else:
        print(f"There were not {limit} products to select")

# def find_newest_order_id(cursor, cust_id, employee_id):
#     query = "SELECT order_id FROM orders WHERE customer id = ?, employee_id = ? GROUP BY date DESC"
#     cursor.execute(query, (cust_id, employee_id))
#     try:
#         data = cursor.fetchone()
#     except sqlite3.Error as e:
#         print(f"A SQLite3 error has occured: {e}")
#     if data:
#         return data[0]
#     else:
#         print("No order record found.  Please double check customer id and employee id")
        
def create_new_order(conn, cust_name, employee_name, limit, quantity):
    cursor = conn.cursor()
    cust_id = find_cust_id(cursor, cust_name)
    employee_id = find_employee_id(cursor, employee_name)
    product_id_list = find_cheapest_products(cursor, limit)
    current_date = date.today().isoformat()
    
    try:
        with conn:
            statement_orders = "INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?) RETURNING order_id"
            cursor.execute(statement_orders, [cust_id, employee_id, current_date])
            
            order_id = cursor.fetchall()[0]
            # Can also use to ensure only returning last row instead of a list of order_ids
            # order_id = cursor.lastrowid
            statement_line_items = "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)"
            for product_id in product_id_list:
                cursor.execute(statement_line_items, [order_id, product_id, quantity])
        return order_id
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")
        

def find_order(conn, order_id):
    cursor = conn.cursor()
    query = f"SELECT li.line_item_id, li.quantity, p.product_name FROM line_items AS li JOIN products AS p ON li.product_id = p.product_id WHERE li.order_id = ?"
    cursor.execute(query, (order_id,))
    try:
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")

    return data

# Task 4 Part 1
def find_employee_order_count(conn):
    cursor = conn.cursor()
    query = "SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.employee_id) AS order_count FROM employees AS e JOIN orders AS o ON e.employee_id = o.employee_id GROUP BY o.employee_id HAVING order_count > 5"
    cursor.execute(query)
    try:
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"A SQLite3 error has occured: {e}")

    return data
    
if __name__ == "__main__":
    main()

