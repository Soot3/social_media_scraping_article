from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
# Define the URL you want to scrape
url = 'https://www.facebook.com/officialtomcruise/'

# Define the options for the Chrome webdriver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

# Create a new instance of the Chrome webdriver with the defined options
driver = webdriver.Chrome(options=options)

# Load the Facebook page in the webdriver
driver.get(url)

# Extract the HTML content of the page using BeautifulSoup
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

posts = soup.find_all('div', class_='x1l90r2v') 

# Extract the text content of each post
post_content = [post.text for post in posts]

# Save the scraped data in a CSV file
data = pd.DataFrame({'post_content': post_content})
data.to_csv('facebook_posts.csv', index=False)

# Print the scraped data
print(data)


# Close the webdriver
driver.quit()
