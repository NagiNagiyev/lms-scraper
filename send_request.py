import requests

# Specify the URL
url = "https://lms-scraper.onrender.com/scrape"

# Specify the data to be sent in the request
data = {
    "username": "nagi.nagiyev",
    "password": "Nagi2003",
    "semester": "Autumn"
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Request successful. Response:")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}.")
    print(response.text)