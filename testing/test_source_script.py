import requests

url = "http://localhost:8000/api/source"

#Testing Insert into sources (POST)
payload = {
    "source_name": "Bible in a Year: Day 8 God's Covenant with Abram",
    "source_type_id": 4,
    "series": 1,
    "creator_id": 1,
    "secondary_creator_id": 2,
    "source_description": "Episode 7 covering Genesis 12 and Job 1"
}

res = requests.post(url, json = payload)
print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

payload = {
    "source_name": "Bible in a Year: Day 12 The Sacrifice of Isaac",
    "source_type_id": 4,
    "series": 1,
    "creator_id": 1,
    "secondary_creator_id": None,
    "source_description": None
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

#Testing Get All Sources
res = requests.get(url,)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get a specific source
source_id = 2
url = f"http://localhost:8000/api/source/{source_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())