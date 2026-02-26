import requests

url = "http://localhost:8000/analyze"
file_path = "data/TSLA-Q2-2025-Update.pdf"
query = "Analyze Tesla's performance in Q2 2025"

with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"query": query}
    response = requests.post(url, files=files, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
