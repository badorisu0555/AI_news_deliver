import requests

url = "http://3.113.24.208:80/predict?query=乃木坂46&tweet_cnt=10"

res = requests.get(url)
#print(res.status_code)

if res.status_code == 200:
    answer = res.json()
    print(answer)
else :
    print(f"Error:{res.status_code}")
    print(res.text())