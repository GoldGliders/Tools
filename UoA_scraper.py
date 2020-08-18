import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://web-int.u-aizu.ac.jp/"
# SUFFIX = "course/alg1/"
# SUFFIX = "~yamagami/ns02exe2019.html"
SUFFIX = "~vkluev/courses/javaone/"
URL = BASE_URL + SUFFIX

ID = os.getenv("UoA_ID")
PASSWD = os.getenv("UoA_PASSWD")

response = requests.get(URL, auth=(ID, PASSWD))
response.encoding = response.apparent_encoding
contents = response.content
contents = contents.decode("shift-jis")
soup = BeautifulSoup(contents, "lxml")

for a in soup.find_all("a"):
    link = a.attrs
    if "href" not in link:
        continue

    if "pdf" in link["href"]:
        # link = URL + link["href"]
        # link = link["href"]
        pdf = requests.get(link, auth=(ID, PASSWD))
        name = link.split("/")[-1]
        print(link, name)
        with open(name, "wb") as f:
            f.write(pdf.content)
