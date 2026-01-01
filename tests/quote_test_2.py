import requests

url = "http://localhost:8000/api/quote"

#Testing Insert into quote (POST)
payload = {
    "quote_text": "Test text from posting a new quote",
    "source_id": 1,
    "book_ref_id": 1,
}

res = requests.post(url, json = payload)
print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

payload = {
    "quote_text": "God is with us",
    "source_id": 2,
    "book_ref_id": None,
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)
#print("Response:", res.json())

#Testing Get All Quotes
res = requests.get(url,)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get all quotes by source
source_id = 1
url = f"http://localhost:8000/api/quote/{source_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())

quote_id = 1
url = f"http://localhost:8000/api/quote/{quote_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())

quote_id = 1
url = f"http://localhost:8000/api/quote/{quote_id}"
res = requests.delete(url)
print("Status:", res.status_code)