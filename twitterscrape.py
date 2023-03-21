from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time 

# Define the URL you want to scrape
url = 'https://twitter.com/TomCruise'

# Define the options for the Chrome webdriver to mimic a real page
options = Options()
options.add_argument('--headless')
options.add_argument("--incognito")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
options.add_argument("--enable-javascript")

# Create a new instance of the Chrome webdriver with the defined options
driver = webdriver.Chrome(options=options)

# Load the Twitter page in the webdriver
driver.get(url)

# Wait for tweets to populate the page
try:
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="tweet"]')))
except WebDriverException:
    print("Something happened. No tweets loaded")

# scroll a bit for more tweets to appear
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(10)

# Extract the HTML content of the page using BeautifulSoup
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

posts = soup.find_all(attrs={"data-testid": "tweetText"})

# Extract the text content of each post
post_content = [post.text for post in posts]

# Save the scraped data in a CSV file
data = pd.DataFrame({'post_content': post_content})
data.to_csv('twitter_posts.csv', index=False)

# Print the scraped data
print(data)

# Close the webdriver
driver.quit()
