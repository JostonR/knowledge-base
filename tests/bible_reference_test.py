import requests

url = "http://localhost:8000/api/bibleref"

#Testing Insert into bible_references (POST)
payload = {
    "insight_id": 1,
    "bible_book_id": 1,
    "chapter_start": 1,
    "verse_start": 1,
    "verse_end": 2
}

res = requests.post(url, json = payload)
print("Status:", res.status_code)
print("Raw response text:\n", res.text)

payload = {
    "insight_id": 2,
    "bible_book_id": 1,
    "chapter_start": 17,
    "verse_start": 5,
    "verse_end": 12,
    "note": "Lack of complete trust"
}

res = requests.post(url, json = payload)

print("Status:", res.status_code)
print("Raw response text:\n", res.text)


#Testing Get All Sources
res = requests.get(url,)
print("Status:", res.status_code)
print("Response:", res.json())

#Testing Get a specific source
bibleref_id = 1
url = f"{url}/{bibleref_id}"
res = requests.get(url)
print("Status:", res.status_code)
print("Response:", res.json())