import requests

res = requests.get("http://google.com")
# res = requests.get("https://")
print("응답코드 : ", res.status_code)
res.raise_for_status()

# if res.status_code == requests.codes.ok:
#     print("정상입니다")
# else:
#     print("문제가 생겼습니다. [에러코드]",res.status_code)
print("웹스크레이핑을 진행합니다")

print(len(res.text))

with open("mygoogle.html", "w",encoding='utf-8') as f:
    f.write(res.text)


