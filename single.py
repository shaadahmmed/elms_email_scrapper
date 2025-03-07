from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)
username = os.getenv("STU_ID")
password = os.getenv("PASS")
course_id = os.getenv("COURSE_ID")
login_url = "https://elms.uiu.ac.bd/login/index.php"
course_url = f"https://elms.uiu.ac.bd/user/index.php?page=0&perpage=5000&contextid=0&id={course_id}&newcourse"

if not course_id or not username or not password:
    print("Please enter necessary data in .env")
    exit()

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

response = session.get(login_url, headers=headers)

if response.status_code == 200:
    print("Fetched login page successfully.")
else:
    print("Failed to fetch login page.")
    exit()


soup = BeautifulSoup(response.text, "html.parser")
login_token = soup.find("input", {"name": "logintoken"})["value"]

payload = {
    "logintoken": login_token,
    "username": username,
    "password": password,
}

login_response = session.post(login_url, data=payload, headers=headers)

if "Dashboard" in login_response.text or "login" not in login_url:
    print("Login successful!")
    print("Session Started")
else:
    print("Login failed. Check your credentials.")
    exit()

course_response = session.get(course_url)

course_soup = BeautifulSoup(course_response.text, "lxml")

links = course_soup.find_all("a", class_="d-inline-block aabtn", href=True)
title = course_soup.find("h1", class_="h2").text
total_participant = course_soup.find("p", {"data-region": "participant-count"}).text
print(f"Course: {title}")
print(total_participant)

count = 0
if not os.path.exists("emails"):
    os.makedirs("emails")

with open(f"emails/{course_id}.txt", "w") as file:
    file.write(f"{title}\n\n")
    for link in links:
        profile_link = link["href"]
        profile_response = session.get(profile_link)
        profile_soup = BeautifulSoup(profile_response.text, "lxml")
        all_links = profile_soup.find_all("a", href=True)

        for single_link in all_links:
            if "mailto" in single_link["href"]:
                file.write(f"{single_link.text}\n")
                count = count + 1

print(f"Total Email Found: {count}")
