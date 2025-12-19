import requests

url = "http://localhost:8000/api/creator"

#Testing Insert into creators (POST)
payload = {
    "full_name": "J.K Rowling",
    "title": "Author",
}

res = requests.post(url, json = payload)
print("Status:", res.status_code)
print("Headers:", res.headers.get("content-type"))
print("Raw response text:\n", res.text)

payload = {
    "full_name": "Bishop Robert Barron",
    "title": "Bishop",
    "notes": "Bishop, Priest, author, evangelist, founder of new religious order"
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Raw response text:\n", res.text)

payload = {
    "full_name": "Joston Rodrigues"
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Raw response text:\n", res.text)


#Testing Get All Sources
res = requests.get(url,)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get a specific source
creator_id = 1
url = f"http://localhost:8000/api/source/{creator_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())