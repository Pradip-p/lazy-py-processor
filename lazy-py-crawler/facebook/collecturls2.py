import threading
import mysql.connector
import time
from queue import Queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="hostname",
  user="username",
  password="password",
  database="database_name"
)

# Create a cursor to interact with the database
mycursor = mydb.cursor()

# Create a queue to store the URLs
url_queue = Queue()

# Add the initial URL to the queue
url_queue.put("https://www.amazon.com/")

# Define a function to be used by the threads
def process_url():
    while not url_queue.empty():
        url = url_queue.get()
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=http://webshare.io")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='a-link-normal']")))
        links = driver.find_elements_by_xpath("//a[@class='-link-normal']")
for link in links:
new_url = link.get_attribute("href")
if "https://www.amazon.com" in new_url and "product" in new_url:
product_name = driver.find_element_by_xpath("//span[@id='productTitle']").text
breadcrumbs = []
breadcrumb_elements = driver.find_elements_by_xpath("//span[@class='a-size-base a-color-tertiary']")
for breadcrumb in breadcrumb_elements:
breadcrumb_text = breadcrumb.text
mycursor.execute("SELECT id FROM breadcrumbs WHERE breadcrumb = %s", (breadcrumb_text,))
result = mycursor.fetchone()
if result is None:
mycursor.execute("INSERT INTO breadcrumbs (breadcrumb) VALUES (%s)", (breadcrumb_text,))
mydb.commit()
breadcrumb_id = mycursor.lastrowid
else:
breadcrumb_id = result[0]
breadcrumbs.append(breadcrumb_id)
mycursor.execute("SELECT id FROM products WHERE url = %s", (new_url,))
result = mycursor.fetchone()
if result is None:
mycursor.execute("INSERT INTO products (url, name) VALUES (%s, %s)", (new_url, product_name))
mydb.commit()
product_id = mycursor.lastrowid
else:
product_id = result[0]
for breadcrumb_id in breadcrumbs:
mycursor.execute("INSERT INTO product_breadcrumbs (product_id, breadcrumb_id) VALUES (%s, %s)", (product_id, breadcrumb_id))
mydb.commit()
url_queue.put(new_url)
driver.close()
url_queue.task_done()

#Create and start the threads
for i in range(20):
t = threading.Thread(target=process_url)
t.daemon = True
t.start()

#Wait for all the URLs to be processed
url_queue.join()


