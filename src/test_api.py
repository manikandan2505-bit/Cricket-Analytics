from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("CRICKET_API_KEY")

print("API Key Loaded:", API_KEY[:5] + "..." if API_KEY else "No key found")

url = f"https://api.cricketdata.org/v1/currentMatches?apikey={API_KEY}&offset=0"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Text:")
print(response.text[:500])