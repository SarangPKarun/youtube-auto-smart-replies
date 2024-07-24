from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time


# Set the path for ChromeDriver
chrome_driver_path = '/usr/local/bin/chromedriver'


# Create a Service object with the ChromeDriver path
service = Service(chrome_driver_path)

# Initialize the WebDriver with the Service and Options
driver = webdriver.Chrome(service=service)


# Open a website
driver.get("https://www.youtube.com/watch?v=TbuAvyyjxyM")
time.sleep(5)  # Wait for comments to load

comments = []


# Function to scroll down the page to load more comments
def scroll_down():
    # Scroll down the page in steps until no more comments are loaded
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # Wait to load page
        time.sleep(2)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll down to load all comments
scroll_down()


# Locate all comment elements
comment_elements = driver.find_elements(By.CSS_SELECTOR, 'ytd-comment-thread-renderer')

# Iterate through each comment element and extract the text
for comment_element in comment_elements:
    # Locate the element that contains the comment text
    comment_text_element = comment_element.find_element(By.CSS_SELECTOR, '.yt-core-attributed-string.yt-core-attributed-string--white-space-pre-wrap')

    # Get the text of the comment
    comment_text = comment_text_element.text
    comments.append(comment_text)


driver.quit()

# Function to save comments to a CSV file
def save_comments_to_csv(comments, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])
        for comment in comments:
            writer.writerow([comment])

save_comments_to_csv(comments, 'comments.csv')