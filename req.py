import requests
import re

def extract(inp):
    match = re.search(r'\d+', inp)
    if match:
        num = match.group()
    
    return num

kw = "all"


res = []
n = 1
while True:
    resp = requests.get(f"https://jsonmock.hackerrank.com/api/weather/search?name={kw}&page={n}")
    raw_data = resp.json()
    for row in raw_data['data']:
        wind = extract(row['status'][0])
        hum = extract(row['status'][1])
        # print(wind, hum)
        res.append(row['name']+","+row['weather'].split()[0]+","+wind+","+hum)

    if raw_data["page"] >= raw_data["total_pages"]:
        break
    n+=1

print(res)