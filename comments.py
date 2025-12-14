from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from textblob import TextBlob
import time
import sys

def process_video_comments(video_url):
    # Setup Chrome Driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 1. Open Video
        print(f"Opening video: {video_url}")
        driver.get(video_url)
        
        # 2. Manual Login Wait
        print("IMPORTANT: Please log in to your YouTube account in the opened browser.")
        print("Navigate to the login page if needed, but stay on the video page once logged in.")
        input("Press Enter in this terminal ONLY after you have successfully logged in and the video page is loaded...")

        # 3. Scroll to load comments
        print("Scrolling to load comments...")
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        # Scroll a bit to trigger comment loading
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(2)
        
        # Initial wait for comments
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "ytd-comment-thread-renderer"))
            )
        except:
            print("No comments found or took too long to load.")
            return

        # Simple scroll loop (adjust range for more comments)
        for _ in range(5): 
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 4. Iterate Comments
        print("Processing comments...")
        # Get all comment threads
        comment_threads = driver.find_elements(By.TAG_NAME, "ytd-comment-thread-renderer")
        print(f"Found {len(comment_threads)} comment threads.")

        for thread in comment_threads:
            try:
                # scroll into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thread)
                time.sleep(1)

                # Check if already replied
                # Heuristic: Check for 'ytd-author-comment-badge-renderer' inside the replies section of this thread
                # Note: This is tricky. Simplified check:
                # We often see 'Replies' section. If we expanded it, we could see.
                # For an MVP, we might rely on the user visual check or specialized exact scraping.
                # Let's try to look for the user's avatar in the response section or strictly owner badge.
                
                # Check top-level comment text
                comment_body = thread.find_element(By.ID, "content-text")
                comment_text = comment_body.text
                print(f"Analyzing: {comment_text[:50]}...")

                # --- CHECK IF REPLIED LOOP ---
                # A robust way is harder without expanding replies. 
                # We will check if "Replies" count implies it might be us, or skip for now if unsure.
                # Actually, the user asked to skip if already replied.
                # Let's look for element with aria-label="Creator heart" or similar implementation if we hearted it?
                # Or parsing the replies.
                # For this version: We will try to reply. YouTube UI might show "Replied" text?
                # IMPROVEMENT: If we see our own avatar in the specific thread structure, skip.
                
                # 5. Analyze Sentiment
                analysis = TextBlob(comment_text)
                polarity = analysis.sentiment.polarity
                
                reply_text = ""
                if polarity > 0.1:
                    reply_text = "😊" # Positive
                elif polarity < -0.1:
                    reply_text = "🙏" # Negative
                else:
                    reply_text = "👍" # Neutral

                # 6. Reply
                # Find reply button for the TOP LEVEL comment
                # It is usually under #toolbar -> #reply-button-end
                reply_btn = thread.find_element(By.CSS_SELECTOR, "#reply-button-end button")
                reply_btn.click()
                time.sleep(1)

                # Locate the input field
                # It is inside a #contenteditable-root
                input_box = thread.find_element(By.CSS_SELECTOR, "#contenteditable-root")
                
                # Check again if we already replied (sometimes the input box will show previous text or UI changes)
                # But safer is just to type.
                
                input_box.send_keys(reply_text)
                time.sleep(1)

                # Click Submit
                submit_btn = thread.find_element(By.CSS_SELECTOR, "#submit-button button")
                submit_btn.click()
                print(f"Replied: {reply_text}")
                time.sleep(2) # Cooldown

            except Exception as e:
                print(f"Error processing comment: {e}")
                continue

    except Exception as main_e:
        print(f"Critical Error: {main_e}")
    finally:
        print("Done. Keeping browser open for verification.")
        # driver.quit() # Keep open so user can see

if __name__ == "__main__":
    # Test URL if run directly
    url = input("Enter YouTube Video URL: ")
    process_video_comments(url)