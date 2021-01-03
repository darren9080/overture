import requests
from bs4 import BeautifulSoup
import csv

# 코스피 시가 총액 순위
#32

url = f"https://finance.naver.com/sise/sise_market_sum.nhn?&page="
filename = "scraping/naver_finance/시가총액1-200.csv"
f = open(filename, "w",encoding="utf8",newline="")
# 파일이 깨질 경우 인코딩을 'utf-8-sig'
writer = csv.writer(f)

title ="N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE	토론실".split("\t")
writer.writerow(title)


for page in range(1,5):
    res = requests.get(url + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")
    data_rows = soup.find("table",attrs= {"class":"type_2"}).find("tbody").find_all("tr")

    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1:
            continue
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data)

