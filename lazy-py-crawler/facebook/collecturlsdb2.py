import mysql.connector

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host="hostname",
  user="username",
  password="password"
)

# Create a cursor to interact with the server
mycursor = mydb.cursor()

# Create the database
mycursor.execute("CREATE DATABASE database_name")

# Connect to the newly created database
mydb = mysql.connector.connect(
  host="hostname",
  user="username",
  password="password",
  database="database_name"
)

# Create a cursor to interact with the database
mycursor = mydb.cursor()

# Create the products table
mycursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), name VARCHAR(255))")

# Create the breadcrumbs table
mycursor.execute("CREATE TABLE breadcrumbs (id INT AUTO_INCREMENT PRIMARY KEY, breadcrumb VARCHAR(255))")

# Create the product_breadcrumbs table
mycursor.execute("CREATE TABLE product_breadcrumbs (product_id INT, breadcrumb_id INT, FOREIGN KEY (product_id) REFERENCES products(id), FOREIGN KEY (breadcrumb_id) REFERENCES breadcrumbs(id))")
