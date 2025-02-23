# UIU eLMS Mail Scrapper

Helps you to extract the mails of  the course participants.

All you need is your eLMS `username` and `password`

---

### Features

1. Single Course Scrape  `use single.py`
2. All course email scrape `use bulk.py`

---

### Requirements

* Python Installed
* Some Patience

---

### Get Started

> **Make sure your PC has python installed**

##### Install the requirement

```
pip3 install -r requirements.txt
```

##### Set up the environment

Open `.env` and edit the

`STU_ID` enter your UIU student ID

`PASS` enter your eLMS password

`COURSE_ID` if you are extracting single course then you need it otherwise leave it blank

you can find the `COURSE_ID` by

1. Open any browser
2. Login to eLMS
3. Go to the course that you want to scrape
4. Look at the `url` the url will look like this `https://elms.uiu.ac.bd/course/view.php?id=1769`
5. You need to copy the `id` Here in this case it's 1769. Make sure it's in quotation

Have fun.
