import json
from turtle import pd
import requests

page_id = ''

access_token ='EAAXp64TErHYBO2KDw4CZCKWeSZB6dBiEsnVV3mvQftfZARqc5y6lnOYWK87ssnOQKbuyp32WAXD72i0g0vHcvGY92PoSAOpPsLtM3GOGZAvLTEunl00LuknD5IGphLTItnAkh04F7NZAqYHlnU9SsahQSlvSa4wv2mBPuHo221Tlzi7kNh4wEH2n47ZCiE6eGZC4MogiBFBva6aLYcZCb4ikFxdmD2doTtXr3ZBXy'

url = f'https://web.facebook.com/norwegianrefugeecouncil'

response = requests.request("GET",url)

data = json.loads(response.text)

def getComment(comment):
    return{
        'name': comment['from']['name'],
        'time': comment['created_time'],
        'message' : comment['message']
    }

excel_data = list(map(getComment,data['data']))
df=pd.DataFrame(excel_data)
df.to_excel('comments.xlsx',index = False)