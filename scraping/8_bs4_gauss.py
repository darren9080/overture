import requests
from bs4 import BeautifulSoup # scraping tool

#user agent 확인
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

url = "https://comic.naver.com/webtoon/list.nhn?titleId=675554"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")


cartoons = soup.find_all("td",attrs = {'class':'title'})

title = cartoons[1].a.get_text()
print(title)

link = cartoons[0].a["href"]
print("https://comic.naver.com"+ link)

domain = "https://comic.naver.com"


# 제목과 링크 가져오기
for cartoon in cartoons:
    title = cartoon.a.get_text()
    link = domain + cartoon.a['href']
    print(title, link)


# 평점 가져오기

total_rate = 0

cartoons = soup.find_all("div", attrs={'class':'rating_type'})
for cartoon in cartoons:
    rate = cartoon.find('strong').get_text()
    print(rate)
    total_rate += float(rate)
print("전체 점수 : ", total_rate)
print("평균 점수 : ",total_rate/len(cartoons))




