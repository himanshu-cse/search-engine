import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

headers = {
    'User-Agent': 'Mozilla/5.0' 
}

response = requests.get(url, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.prettify())

# now we can hardcode multiple urls to scrape or use a crawler to scrape all html links of one page and then so on 
# or we can use wikipedia api -> "https://pypi.org/project/Wikipedia-API/"

