import sqlite3
import pandas as pd

# Task 5
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """SELECT li.line_item_id, li.quantity, p.product_id, p.product_name, p.price FROM line_items AS li JOIN products AS p ON p.product_id = li.product_id"""
    df = pd.read_sql_query(sql_statement, conn)
    print(df.head())
    
    df["total"] = df["quantity"] * df["price"]
    print(df.head())
    
    grouped_df = df.groupby("product_id").agg({
		"line_item_id" : "count",
		"total" : "sum",
		"product_name" : "first"
	})
    print(grouped_df.head())
    
    sorted_df = grouped_df.sort_values(by = "product_name")
    print(sorted_df.head())
    
    df.to_csv("order_summary.csv", index = False)