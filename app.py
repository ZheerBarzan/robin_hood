import json
import requests
import pandas as pd

access_token = 'EAAXp64TErHYBO2KDw4CZCKWeSZB6dBiEsnVV3mvQftfZARqc5y6lnOYWK87ssnOQKbuyp32WAXD72i0g0vHcvGY92PoSAOpPsLtM3GOGZAvLTEunl00LuknD5IGphLTItnAkh04F7NZAqYHlnU9SsahQSlvSa4wv2mBPuHo221Tlzi7kNh4wEH2n47ZCiE6eGZC4MogiBFBva6aLYcZCb4ikFxdmD2doTtXr3ZBXy'

page_id = 'norwegianrefugeecouncil'
url = f'https://graph.facebook.com/v11.0/{page_id}/posts?access_token={access_token}'

response = requests.get(url)
if response.status_code != 200:
    print(f"Error fetching posts: {response.status_code}")
    print(response.text)
    exit()

data = response.json()


def getComment(comment):
    return {
        'name': comment['from']['name'],
        'time': comment['created_time'],
        'message': comment['message']
    }


comments = []
for post in data.get('data', []):
    post_id = post['id']
    comments_url = f'https://graph.facebook.com/v11.0/{post_id}/comments?access_token={access_token}'

    comments_response = requests.get(comments_url)
    if comments_response.status_code != 200:
        print(f"Error fetching comments for post {post_id}: {comments_response.status_code}")
        print(comments_response.text)
        continue

    comments_data = comments_response.json()

    if 'data' in comments_data:
        comments.extend([getComment(comment) for comment in comments_data['data']])
    else:
        print(f"No comments found for post {post_id}")

if comments:
    df = pd.DataFrame(comments)
    df.to_excel('comments.xlsx', index=False)
    print("Comments successfully saved to comments.xlsx")
else:
    print("No comments found to save.")
