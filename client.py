import requests

url = "http://13.231.248.173:8001"

res = requests.get(url)
#print(res.status_code)

if res.status_code == 200:
    answer = res.json()
    print(answer)
else :
    print(f"Error:{res.status_code}")
    print(res.text)