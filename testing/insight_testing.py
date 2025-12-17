import requests
BASE_URL = "http://localhost:8000/api/insight"
url = BASE_URL

#Testing Insert into insights (POST)
payload = {
    "source_id": 1,
    "insight_creator_id": 2,
    "insight_content": "The finding Lord Jesus in the temple is a prefigurement for "
    "the resurrection. The despair for three days for Mother Mary and Joseph is "
    "replaced by the joy of finding him"
}

res = requests.post(url, json = payload)
print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

payload = {
    "source_id": 2,
    "insight_content": "Testing insight content without a insigh creator"
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

#Testing Get All Insights
res = requests.get(url,)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get a specific source
insight_id = 2
url = f"{BASE_URL}/{insight_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get all insights for a particular source
source_id = 2
url = f"{BASE_URL}/source/{source_id}"
res = requests.get(url, )
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get all insights for a particular series
series_id = 1
url = f"{BASE_URL}/series/{series_id}"
res = requests.get(url, )
print("Status:", res.status_code)
print("Response:", res.json())