import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://web-int.u-aizu.ac.jp/"
URL = input(">>>")

ID = os.getenv("UoA_ID")
PASSWD = os.getenv("UoA_PASSWD")

response = requests.get(URL, auth=(ID, PASSWD))
response.encoding = response.apparent_encoding
contents = response.content
soup = BeautifulSoup(contents, "lxml")


def downloader(url):
    note = requests.get(url, auth=(ID, PASSWD))
    name = url.split("/")[-1]
    print("Downloading {}".format(name))
    with open(name, "wb") as f:
        f.write(note.content)
