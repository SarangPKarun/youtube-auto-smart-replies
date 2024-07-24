import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set the path for ChromeDriver
chrome_driver_path = '/usr/local/bin/chromedriver'

# Function to get comments from a YouTube video
def get_comments(video_url):
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for efficiency
    
    # Create a Service object with the ChromeDriver path
    service = Service(chrome_driver_path)

    # Initialize the WebDriver with the Service and Options
    driver = webdriver.Chrome(service=service)
    
    driver.get(video_url)
    time.sleep(5)  # Wait for the page to load

    comments = []

    while True:
        # Scroll to load more comments
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)  # Wait for comments to load

        # Find and extract comments
        comment_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]/span/text()')
        for element in comment_elements:
            comments.append(element.text)
        
        # Check if we've reached the end of comments (no more "Show more" buttons)
        try:
            show_more_button = driver.find_element(By.CSS_SELECTOR, 'paper-button#more')
            if show_more_button.is_displayed():
                show_more_button.click()
                time.sleep(5)  # Wait for more comments to load
            else:
                break
        except Exception as e:
            print("No more comments to load or error occurred:", e)
            break

    driver.quit()
    return comments

# Function to save comments to a CSV file
def save_comments_to_csv(comments, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])
        for comment in comments:
            writer.writerow([comment])

# Main function
def main():
    video_url = input("Enter the YouTube video URL: ")
    
    comments = get_comments(video_url)
    save_comments_to_csv(comments, 'comments.csv')
    
    print(f"Downloaded {len(comments)} comments.")
    print("Comments saved to comments.csv")

if __name__ == "__main__":
    main()
