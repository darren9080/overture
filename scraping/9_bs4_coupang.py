import requests
from bs4 import BeautifulSoup # scraping tool
import re


url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1&rocketAll=false&searchIndexingToken=1=4&backgroundColor="
#user agent 확인
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
res = requests.get(url,headers = headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
print(res.text)

condition = "^search-product"

items = soup.find_all("li", attrs={"class" : re.compile(condition)})
print(items[0].find("div",attrs = {"class":"name"}).get_text())

for item in items:
    # 광고 제외 하기

    ad_badge = item.find("span",attrs={"class":"ad-badge-text"})

    if ad_badge:
        print("<광고 제품 제외>")
        continue

    name = item.find("div",attrs = {"class":"name"}).get_text()

    # 애플 제품 제외
    if "Apple" in name:
        print("애플 상품 제외")
        continue

    price = item.find("strong",attrs = {"class":"price-value"}).get_text()

    rate = item.find("em",attrs = {"class":"rating"})

    # 리뷰 및 리뷰 수에 대한 조건
    # 평점 > 4.5, 리뷰 수 >100

    if rate:
        rate = rate.get_text()
    else:
        print("<평점 없는 상품 제외>")
        continue

    rate_cnt = item.find("span",attrs = {"class":"rating-total-count"})
    if rate_cnt:
        rate_cnt = rate_cnt.get_text()
        rate_cnt = rate_cnt[1:-1]

    else:
        print("<평점 수 없는 상품 제외>")
        continue

    if float(rate) >= 4.5 and int(rate_cnt) >=100:
        print(name, price, rate, rate_cnt)







