import requests
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

url = "http://nadocoding.tistory.com"
res = requests.get(url, headers = headers)
# res = requests.get("https://")
print("응답코드 : ", res.status_code)
res.raise_for_status()

# if res.status_code == requests.codes.ok:
#     print("정상입니다")
# else:
#     print("문제가 생겼습니다. [에러코드]",res.status_code)
print("웹스크레이핑을 진행합니다")

print(len(res.text))

with open("nadocoding.html", "w",encoding='utf-8') as f:
    f.write(res.text)

''' <user agent>
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
'''