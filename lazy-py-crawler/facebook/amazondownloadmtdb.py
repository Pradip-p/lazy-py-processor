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

# Create a cursor to interact with the new database
mycursor = mydb.cursor()

# Create the products table
mycursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), product_description LONGTEXT, product_info LONGTEXT, about_this_product LONGTEXT, product_rating FLOAT, product_rating_by_feature LONGTEXT, customer_questions_answers LONGTEXT, good_reviews LONGTEXT, bad_reviews LONGTEXT, done BOOLEAN)")
