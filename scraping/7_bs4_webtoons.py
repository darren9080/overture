import requests
from bs4 import BeautifulSoup # scraping tool

#user agent 확인
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)

res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

cartoons = soup.find_all("a", attrs = {'class':'title'})

for cartoon in cartoons:
    print(cartoon.get_text())


