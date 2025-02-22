from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
username = os.getenv("username")
password = os.getenv("password")
login_url = "https://elms.uiu.ac.bd/login/index.php"


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
dashboard_soup = ""

if "Dashboard" in login_response.text or login_response.url != login_url:
    dashboard_soup = BeautifulSoup(login_response.text, "lxml")
    print("Login successful!")
    print("Session Started")
else:
    print("Login failed. Check your credentials.")
    exit()

script_tags = dashboard_soup.find_all("script")
sesskey = ""

for script in script_tags:
    if script.string:
        match = re.search(r'"sesskey":"(.*?)"', script.string)
        if match:
            sesskey = match.group(1)
            break

course_payload = [
    {
        "index": 0,
        "methodname": "core_course_get_enrolled_courses_by_timeline_classification",
        "args": {
            "offset": 0,
            "limit": 24,
            "classification": "all",
            "sort": "fullname",
            "customfieldname": "",
            "customfieldvalue": "",
            "requiredfields": [
                "id",
                "fullname",
                "shortname",
                "showcoursecategory",
                "showshortname",
                "visible",
                "enddate",
            ],
        },
    }
]

all_courses_url = f"https://elms.uiu.ac.bd/lib/ajax/service.php?sesskey={sesskey}&info=core_course_get_enrolled_courses_by_timeline_classification"
courses_data = session.post(
    all_courses_url, json=course_payload, headers=headers
).json()

if courses_data[0]["error"]:
    print("No Course Found")
    exit()

course_ids = []
course_list = courses_data[0]["data"]["courses"]


for course in course_list:
    course_url = f"https://elms.uiu.ac.bd/user/index.php?page=0&perpage=5000&contextid=0&id={course['id']}&newcourse"
    course_response = session.get(course_url)

    course_soup = BeautifulSoup(course_response.text, "lxml")
    links = course_soup.find_all("a", class_="d-inline-block aabtn", href=True)
    total_participant = course_soup.find("p", {"data-region": "participant-count"}).text
    print(f"Course: {course['fullname']}")
    print(total_participant)

    emails = []
    count = 0

    for link in links:
        profile_link = link["href"]
        profile_response = session.get(profile_link)
        profile_soup = BeautifulSoup(profile_response.text, "lxml")
        all_links = profile_soup.find_all("a", href=True)

        for single_link in all_links:
            if "malito" in single_link["href"]:
                emails.append(single_link.text)
                count = count + 1

    with open(f"{course['id']}.txt", "w") as file:
        file.write(course["fullname"])
        for email in emails:
            file.write(email + "\n")

    print(f"Total Email Found: {count}")
    print(f"Emails in: {course['id']}.txt")
