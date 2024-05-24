from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Facebook page
page_url = 'https://www.facebook.com/norwegianrefugeecouncil'
driver.get(page_url)

# Allow some time for the page to load
time.sleep(5)

# Scroll down to load more posts
for _ in range(10):  # Adjust the range for more scrolling
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)

# Locate and extract post elements
posts = driver.find_elements(By.XPATH, '//div[@role="article"]')

# List to store post data
post_data = []

for index, post in enumerate(posts):
    try:
        print(f"Processing post {index + 1}/{len(posts)}")

        # Extracting post text
        try:
            post_text = post.find_element(By.XPATH, './/div[@data-ad-preview="message"]').text
        except Exception as e:
            post_text = ""
            print(f"Error extracting post text: {e}")

        # Extracting post time
        try:
            post_time = post.find_element(By.XPATH, './/abbr').text
        except Exception as e:
            post_time = ""
            print(f"Error extracting post time: {e}")

        post_data.append({
            'post_text': post_text,
            'post_time': post_time,
            'comments': []  # Initialize comments as an empty list
        })

        print(f"Post {index + 1} processed successfully: Text - {post_text[:30]}, Time - {post_time}")

    except Exception as e:
        print(f"Error processing post {index + 1}: {e}")

# Close the browser
driver.quit()

# Print the post_data for debugging
print("Post data:")
for i, post in enumerate(post_data):
    print(f"Post {i}: {post}")

# Convert post data to DataFrame
df_posts = pd.DataFrame(post_data)

# Debug: Print DataFrame columns and head
print("DataFrame columns:", df_posts.columns)
print("DataFrame head:", df_posts.head())

# Ensure 'comments' column is present
if 'comments' in df_posts.columns:
    # Expand comments into separate rows
    comments_expanded = df_posts.explode('comments')
    comments_expanded = comments_expanded.reset_index(drop=True)

    # Debug: Check if comments_expanded is not empty
    if not comments_expanded.empty:
        # Normalize comments dictionary
        comments_df = pd.json_normalize(comments_expanded['comments']).add_prefix('comment_')

        # Merge posts and comments
        final_df = pd.concat([comments_expanded.drop(columns=['comments']), comments_df], axis=1)

        # Save to Excel
        final_df.to_excel('facebook_posts_comments.xlsx', index=False)
        print("Comments successfully saved to comments.xlsx")
    else:
        print("Error: No comments to expand in comments_expanded")
else:
    print("Error: 'comments' column is missing from df_posts")

# Debug: Check if final_df is defined and print its head
try:
    print("Final DataFrame:")
    print(final_df.head())
except NameError:
    print("final_df is not defined.")
