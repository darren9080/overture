import requests
from bs4 import BeautifulSoup # scraping tool
import lxml # parser

#user agent 확인
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)

res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

soup.title
soup.title.get_text()
soup.a.attrs
print(soup.a["href"])

# soup.find("a", attrs= {"class":"Nbtn_upload"})
# print(soup.find("li",attrs = {"class" : "rank01"}))

# rank1 = soup.find("li",attrs = {"class":"rank01"})
# soup.find("li",attrs = {"class" : "rank01"}).next_sibling
# rank2 = rank1.next_sibling.next_sibling
# rank3 = rank2.next_sibling.next_sibling
# rank1.a.get_text()
# rank3.a.get_text()
#
# rank1.parent
#
# rank1.find_next_sibling("li")

# print(rank1.find_next_siblings("li"))


webtoon = soup.find("a", text ='맘마미안-75화')
print(webtoon)
