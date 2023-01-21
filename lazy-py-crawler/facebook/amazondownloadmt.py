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

# Select the URLs from the database
mycursor.execute("SELECT url FROM products WHERE done = 0")
urls = mycursor.fetchall()

# Create a queue to store the URLs
url_queue = Queue()

# Add the URLs to the queue
for url in urls:
    url_queue.put(url)

# Define a function to be used by the threads
def process_url():
    while not url_queue.empty():
        url = url_queue.get()
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=http://webshare.io")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url[0])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='product-image']")))
        product_images = driver.find_elements_by_xpath("//img[@class='product-image']")
        for image in product_images:
            img_src = image.get_attribute("src")
            img_data = requests.get(img_src).content
            with open(f'product-images/{img_src.split("/")[-1]}', 'wb') as handler:
                handler.write(img_data)
        product_videos = driver.find_elements_by_xpath("//video[@class='product-video']")
        for video in product_videos:
            video_src = video.get_attribute("src")
            video_data = requests.get(video_src).content
            with open(f'product-videos/{video_src.split("/")[-1]}', 'wb') as handler:
                handler.write(video_data)
        customer_images = driver.find_elements_by_xpath("//img[@class='customer-image']")
        for image in customer_images:
            img_src = image.get_attribute("src")
            img_data = requests.get(img_src).content
            with open(f'customer-images/{img_src.split("/")[-1]}', 'wb') as handler:
                handler.write(img_data)
        customer_videos = driver.find_elements_by_xpath("//video[@class='customer-video']")
        for video in customer_videos:
            video_src = video.get_attribute("src")
            video_data = requests.get(video_src).content
                        with open(f'customer-videos/{video_src.split("/")[-1]}', 'wb') as handler:
                handler.write(video_data)
        product_description = driver.find_element_by_xpath("//div[@class='product-description']").text
        product_info = driver.find_element_by_xpath("//div[@class='product-info']").text
        about_this_product = driver.find_element_by_xpath("//div[@class='about-this-product']").text
        product_rating = driver.find_element_by_xpath("//span[@class='product-rating']").text
        product_rating_by_feature = {}
        rating_features = driver.find_elements_by_xpath("//div[@class='product-rating-by-feature']")
        for feature in rating_features:
            feature_name = feature.find_element_by_xpath(".//span[@class='feature-name']").text
            feature_rating = feature.find_element_by_xpath(".//span[@class='feature-rating']").text
            product_rating_by_feature[feature_name] = feature_rating
        customer_questions_answers = []
        questions = driver.find_elements_by_xpath("//div[@class='customer-question']")
        for question in questions:
            question_text = question.find_element_by_xpath(".//span[@class='question-text']").text
            answer_text = question.find_element_by_xpath(".//span[@class='answer-text']").text
            customer_questions_answers.append({'question': question_text, 'answer': answer_text})
        good_reviews = []
        review_elements = driver.find_elements_by_xpath("//div[@class='good-review']")
        for review in review_elements:
            if len(good_reviews) == 10:
                break
            review_text = review.find_element_by_xpath(".//span[@class='review-text']").text
            good_reviews.append(review_text)
        bad_reviews = []
        review_elements = driver.find_elements_by_xpath("//div[@class='bad-review']")
        for review in review_elements:
            if len(bad_reviews) == 10:
                break
            review_text = review.find_element_by_xpath(".//span[@class='review-text']").text
            bad_reviews.append(review_text)
        sql = "UPDATE products SET product_description = %s, product_info = %s, about_this_product = %s, product_rating = %s, product_rating_by_feature = %s, customer_questions_answers = %s, good_reviews = %s, bad_reviews = %s, done = 1 WHERE url = %s"
        val = (product_description, product_info, about_this_product, product_rating, product_rating_by_feature, customer_questions_answers, good_reviews, bad_reviews, url[0])
        mycursor.execute(sql, val)
        mydb.commit()
        driver.close()
        url_queue.task_done()

# Create and start the threads
for i in range(20):
    t = threading.Thread(target=process_url)
    t.daemon = True
    t.start()

# Wait for all the URLs to be processed
url_queue.join()

