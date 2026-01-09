import sqlite3

# Task 1
def main():
	with sqlite3.connect("../db/magazines.db") as conn:
		print("Database created and connected successfully")
		conn.execute("PRAGMA foreign_keys = 1")
		cursor = conn.cursor()
	# except sqlite3.Error as e:
	#     print(f"An error has occured: {e}")

	# Task 2
		publishers_table = """CREATE TABLE IF NOT EXISTS publishers (
			publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
			publisher TEXT UNIQUE
			)"""
		magazines_table = """CREATE TABLE IF NOT EXISTS magazines (
			magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
			magazine TEXT UNIQUE,
			publisher_id INTEGER,
			CONSTRAINT publisher_fk
				FOREIGN KEY (publisher_id)
				REFERENCES publishers (publisher_id)
			)"""
		subscribers_table = """CREATE TABLE IF NOT EXISTS subscribers (
			subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			address TEXT NOT NULL,
			UNIQUE (name, address)
			)"""
		subscription_table = """CREATE TABLE IF NOT EXISTS subscription (
			subscriber_id INT NOT NULL,
			magazine_id INT NOT NULL,
			expiration_date TEXT NOT NULL,
			PRIMARY KEY (subscriber_id, magazine_id),
			CONSTRAINT magazine_fk
				FOREIGN KEY (magazine_id)
				REFERENCES magazines(magazine_id)
			CONSTRAINT subscriber_fk
				FOREIGN KEY (subscriber_id)
				REFERENCES subscribers(subscriber_id)
			)"""
			
		cursor.execute(publishers_table)
		cursor.execute(magazines_table)
		cursor.execute(subscribers_table)
		cursor.execute(subscription_table)
	
	# Task 3
		publisher_list = ["Condé Nast", "Hearst Corporation", "National Geographic Society"]
		magazine_dictionary = {"Vogue" : "Condé Nast",
						"The New Yorker" : "Condé Nast",
						"Cosmopolitan" : "Hearst Corporation",
						"National Geographic": "National Geographic Society"}
		subscriber_dictionary = {"Snoopy" : "1720 Pine Street",
						   "Homer Simpson" : "742 Evergreen Terrace",
						   "Miffy" : "Agnietenstraat 2 3512 XB Utrecht, Netherlands",
						   "Elmo" : "123 Sesame Street"}
		subscription_dictionary = {("Snoopy", "1720 Pine Street") : [("Vogue", 	"January 1, 2027")],
							 ("Miffy", "Agnietenstraat 2 3512 XB Utrecht, Netherlands") : [("National Geographic", "Lifetime"), ("The New Yorker", "February 14, 2027")],
							 ("Elmo", "123 Sesame Street") : [("The New Yorker", "December 25, 2026")],
							 ("Homer Simpson", "742 Evergreen Terrace"): [("Cosmopolitan", "09/01/2027")]}
  
		for publisher in publisher_list:
			insert_publishers(cursor, publisher)
		for magazine, publisher in magazine_dictionary.items():
			insert_magazines(cursor, magazine, publisher)
		for subscriber, address in subscriber_dictionary.items():
			insert_subscribers(cursor, subscriber, address)
		for subscriber, magazines in subscription_dictionary.items():
			name = subscriber[0]
			address = subscriber[1]
			for magazine in magazines:
				magazine_name = magazine[0]
				expiration_date = magazine[1]
				insert_subscription(cursor, name, address, magazine_name, expiration_date)
	# Task 4
		subscription_data = fetch_table(cursor, "*", "subscription")
		print("This is the table of the subscriber ids and magazine ids with the expiration date")
		print(subscription_data)
		
		magazine_data = fetch_table(cursor, "magazine", "magazines")
		magazines_sorted = sorted([data[0] for data in magazine_data])
		print("This is a list of all the available magazines sorted in alphabetical order")
		print(magazines_sorted)

		specified_publisher = "Condé Nast"
		primary_key = find_key(cursor, "publishers", "publisher_id", "publisher", specified_publisher)
		if primary_key:
			temp = join_table(cursor, "magazines", "publishers", "publisher_id", "magazine", primary_key[0])
			magazine_with_publisher = [data[0] for data in temp]
			print(f"This is a list of magazines with the publisher {specified_publisher}")
			print(magazine_with_publisher)
		else:
			print(f"There is no publisher called {primary_key[1]}")
	
		conn.commit()

	print("Database has been closed")

def insert_publishers(cursor, publisher):
	query = """INSERT INTO publishers (publisher) VALUES (?) ON CONFLICT (publisher) DO NOTHING"""
	cursor.execute(query, (publisher,))
 
def insert_magazines(cursor, magazine, publisher):
	cursor.execute("SELECT publisher_id FROM publishers WHERE publisher = ?", (publisher,))
	result = cursor.fetchone()
	if result:
		pub_id = result[0]
		query = """INSERT INTO magazines(publisher_id, magazine) VALUES (?, ?) ON CONFLICT (magazine) DO NOTHING"""
		try:
			cursor.execute(query, (pub_id, magazine))
		except sqlite3.Error as e:
			print(f"A SQLite error occured: {e}")
	else:
		print(f"Could not find or create publisher: {publisher}")
	
def insert_subscribers(cursor, name, address):
	query = """INSERT INTO subscribers (name, address) VALUES (?, ?) ON CONFLICT (name, address) DO NOTHING"""
	cursor.execute(query, (name, address))
	
def insert_subscription(cursor, name, address, magazine, expiration_date):
	cursor.execute("SELECT subscriber_id from subscribers WHERE name = ? AND address = ?", (name, address))
	sub_id_result = cursor.fetchone()
	cursor.execute("SELECT magazine_id from magazines WHERE magazine = ?", (magazine,))
	mag_id_result = cursor.fetchone()
	if sub_id_result and mag_id_result:
		sub_id = sub_id_result[0]
		mag_id = mag_id_result[0]
		query = """INSERT INTO subscription (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?) ON CONFLICT (subscriber_id, magazine_id) DO NOTHING"""
		try:
			cursor.execute(query, (sub_id, mag_id, expiration_date))
		except sqlite3.Error as e:
			print(f"A SQLite error occured: {e}")
	elif sub_id_result is None:
			print(f"There is no one in the database named {name} and {address}")
	elif mag_id_result is None:
			print(f"There is no magazine called {magazine}")

def fetch_table(cursor, columns, table):
	query = f"SELECT {columns} FROM {table}"
	cursor.execute(query)
	try:
		data = cursor.fetchall()
	except sqlite3.Error as e:
		print(f"A SQLite error occured: {e}")
	return data

def find_key(cursor, table, column_pk, column_name, name):
	query = f"SELECT {column_pk} FROM {table} WHERE {column_name} = ?"
	cursor.execute(query, (name,))
	try:
		data = cursor.fetchone()
	except sqlite3.Error as e:
		print(f"A SQLite error occured: {e}")
	return data
 
def join_table(cursor, table_1, table_2, common_column, column_name, primary_key):
	query = f"SELECT {column_name} FROM {table_1} AS t1 JOIN {table_2} AS t2 ON t1.{common_column} = t2.{common_column} WHERE t1.{common_column} = ?"
	cursor.execute(query, (primary_key,))
	table = cursor.fetchall()
	return table

if __name__ == "__main__":
	main()