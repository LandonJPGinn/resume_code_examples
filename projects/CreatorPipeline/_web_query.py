import requests
from bs4 import BeautifulSoup

params = {
    "q": "python",
    "hl": "en",  # language
    "gl": "us",  # country of the search, US -> USA
    "start": 0,  # number page by default up to 0
    "filter": 0,  # show all pages by default up to 10
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

page_num = 0

while True:
    page_num += 1
    print(f"{page_num} page:")

    html = requests.get(
        "https://www.google.com/search", params=params, headers=headers, timeout=30
    )
    soup = BeautifulSoup(html.text, "lxml")

    for result in soup.select(".tF2Cxc"):
        title = f'Title: {result.select_one("h3").text}'
        link = f'Link: {result.select_one("a")["href"]}'
        try:
            description = f'Description: {result.select_one(".VwiC3b").text}'
        except Exception as err:
            print(err)
            description = None

        print(title, link, description, sep="\n", end="\n\n")

    if soup.select_one(".d6cvqb a[id=pnnext]"):
        print("yes")
        params["start"] += 10
    else:
        break
