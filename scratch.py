# %% import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import sweetviz as sv
# %% Data Visualization
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 1000)

# import matplotlib.font_manager as fm
# font_path = 'data/font/NanumGothic.ttf'
# fontprop = fm.FontProperties(fname=font_path,size= 12)

#%% import data
# google_analytics_event.csv: 웹 서비스에서 발생한 GA 이벤트 데이터
event = pd.read_csv('data/google_analytics_event.csv', sep = ',', low_memory=False)
'''
eventData
● date: 이벤트가 발생한 일자 (yyyy-mm-dd 형식).
● path: 서비스 영역 페이지 주소. banksalad.com 이하 주소 string 값.
● category: 페이지 내 위치 string 값
● action: 발생한 이벤트 종류에 따른 의미 string 값.
● card_id: 카드 id.
● card_name: 카드사 이름.
● rank_in_list: 여러 카드가 결과리스트에 나오는 경우 카드가 노출된 순위.
● total: 이벤트 발생수.
'''
# google_analytics_pageview.csv: 웹 서비스의 페이지 별 조회수 데이터
pageview = pd.read_csv('data/google_analytics_pageview.csv', sep = ',', low_memory=False)
'''
● date: 페이지 조회가 발생한 일자 (yyyy-mm-dd 형식).
● path: 서비스 영역 페이지 주소. banksalad.com 이하 주소 string 값.
● total: 페이지 조회수.
'''
event_cleaned = event.copy()
pageview_cleaned = pageview.copy()

# %% data cleaning
### event
# 1. path에 '/'로 시작하지 않는 path 찾아서 앞에 '/' + path
# '/' + pageview_cleaned[~pageview_cleaned.path.apply(lambda x: x.startswith('/'))].path
event_cleaned.path.value_counts()
event_cleaned.loc[~event_cleaned['path'].apply(lambda x : x.startswith('/'))].path
# update 'path'
for idx, path in enumerate(event_cleaned.path):
    if not path.startswith('/'):
        event_cleaned['path'][idx]=  f'/{path}'
# check if there are paths that does not start with '/'
event_cleaned.loc[~event_cleaned['path'].apply(lambda x : x.startswith('/'))].path
# 2. 히어로, 고정_신청, 카드랭킹 앞에 '카드:' 추가
event_cleaned.category.value_counts()
error_entry = ["히어로","고정_신청","카드랭킹"]
for error in error_entry:
    #print(index,error)
    for idx, category in enumerate(event_cleaned['category']):
         if category == error:
            event_cleaned['category'][idx] = f'카드:{error}'
# 3. convert date(str) column to datetime type
event_cleaned['date'] = pd.to_datetime(event_cleaned['date'], format = '%Y/%m/%d')
pageview_cleaned['date'] = pd.to_datetime(pageview_cleaned['date'], format = '%Y/%m/%d')

pd.options.display.float_format = '{:.0f}'.format

#카드사 별 카드
# {카드사_카드번호}
event_cleaned['card'] = event_cleaned['card_name'] + '_' + event_cleaned['card_id'].astype(str)
event_cleaned.groupby(['card_name','card']).size().reset_index()

### pageview
# 1. path에 '/'로 시작하지 않는 path 찾아서 앞에 '/' + path
pageview_cleaned.loc[~pageview_cleaned['path'].apply(lambda x : x.startswith('/'))].path
# [path for path in event_cleaned.path if not path.startswith('/')]
for idx, path in enumerate(pageview_cleaned.path):
    if not path.startswith('/'):
        pageview_cleaned['path'][idx]=  f'/{path}'
pageview_cleaned.loc[~pageview_cleaned['path'].apply(lambda x : x.startswith('/'))].path
# @todo : /cards/aaa'></issue 해결하기
# 해당 페이지뷰가 얼마나 자주 나왔는지 카운트
PV = pageview_cleaned.groupby(['path']).sum().reset_index()

# 카드사 별 카드 count
event_cleaned.groupby(['card_name','card_id']).size()
cardNameList = event_cleaned.card_name.unique()

############################################
############# CLEANING DONE ################
############################################
# %% pandas profiling EDA, sweetviz EDA
pr1=event_cleaned.profile_report()
pr2=pageview_cleaned.profile_report()
pr1.to_file('./event_report.html')
pr2.to_file('./pageview_report.html')

pr1Report = sv.analyze(event_cleaned)
pr2Report = sv.analyze(pageview_cleaned)
pr1Report.show_html('./sweetviz_eventEda.html')
pr2Report.show_html('./sweetviz_pageviewEda.html')
# %% visual
pageview_cleaned.columns
pageview_cleaned.groupby(["path","date"]).count()['total'].plot()
plt.show()

# 2020년 3월 29일부터 2020년 6월 28일
pageview_cleaned.date.sort_values(ascending = False)
event_cleaned.date.sort_values(ascending  = False)

print("분석 대상 기간 : "+ str(len(event_cleaned.date.unique())))
# 전체 기간(2020년 3월 29일부터 2020년 6월 28일) CTR (신청/ 상품노출)*100
totalCTR = (event_cleaned.action.value_counts()[1]/event_cleaned.action.value_counts()[0]) *100
print("전체 CTR : " + str(totalCTR)+"%")

# 일별 ctr 구하고 각 이벤트/카드사/ 카드상품 별 ctr 계산해서 daily ctr 이하인 항목만 subset하고 추가 eda
# dailyCTR = event_cleaned.groupby(['date','action']).size()

# categorical plot
#
# sns.catplot(x="card_name", kind = 'point', data= event_cleaned)
# plt.show()
#
# sns.catplot(x = 'date', y ='card_id', kind = 'point', data = event_cleaned)
# plt.show()
#
#
# # method2
# fig, ax = plt.subplots()
# for key,data in event_cleaned.groupby('card_name'):
#   data.plot(x='date',y = 'total', ax= ax, label=key)
#
# plt.ylabel('card_name')
# plt.show()

#####

# event_cleaned.columns
# event_cleaned.groupby(['date','action','card_name','card_id']).size()
#
# plt.plot(event_cleaned.groupby(['date']), event_cleaned['card_id'])
# xlab = 'pa'
# ylab = 'date'
# title = 'Pageview Per Day'
#
# plt.show()


'''
3.
'''

'''
그래프 내용
1. daily pageview 그래프
2. total ctr, daily ctr 들어간 그래프
3. event별 daily ctr
4. 카드사/카드 별 daily ctr
5.
'''


#%% 현황 분석

# 각 서비스, 카드 콘텐츠별 카드 신청 현황 분석
event_cleaned.action.value_counts()
cardEventList = event_cleaned.category.unique()

event_cleaned.groupby(['category']).size().sort_values(ascending=False)

# 카드사/ 카드 상품 별
cardRegStatus = event_cleaned.loc[event_cleaned.action == '신청']
cardRegStatus.groupby(['card_name','date']).size().reset_index()

cardRegStatus.groupby(['category','card_name']).size().sort_values(ascending = False)

fig, ax = plt.subplots(figsize = (15,7))
cardRegStatus.groupby(['card_name','date']).size().plot(ax=ax)
plt.show()

#fig, ax = plt.subplots(figsize=(15,7))
#data.groupby(['date','type']).count()['amount'].plot(ax=ax)



# .agg()로 날짜별 cnt 구현

# for path in event_cleaned.path:
#    if ('/questions' or '/profits') in path:
#        event_cleaned['service'] = 'Best 카드 찾기 서비스'
#    elif ('/ranking') in path:
#        event_cleaned['service'] = '인기카드 추천 서비스'
#    elif ('/promotion/annual-fee') in path:
#        event_cleaned['service'] = '연회비 지원 카드추천 서비스'

##################################################### SERVICES ##################################################


# %% action == '신청' df 생성 MERGE on = ["path","date"]
# 서비스 네가지
'''
서비스 3가지 + 테마별 추천의 카드사/ 카드별 신청 현황
'''
issueReq = event_cleaned.loc[event_cleaned.action == '신청']
#Merge Event and Pageview
issueReqPV = pd.merge(issueReq,pageview_cleaned, on = ["path","date"], how= 'left',suffixes=('_event', '_pv'))
serviceList = ['Best 카드 찾기 서비스','인기카드 추천 서비스','테마별 카드추천','연회비 지원카드 추천 서비스']
# (신청/상품노출)*100 이 가장 낮은 서비스 파악

# %% subset by 상품노출
nonReq = event_cleaned.loc[event_cleaned.action == '상품노출']
nonReq.groupby(nonReq['card_id']).size()
# nonReq.groupby(['card_name','card_id'])

'''
Best 카드 찾기 서비스
1. 카드 소비 패턴 입력(/cards/questions)
2. 추천 카드 리스트 조회(/cards/profits)
3. 카드 상세 정보 페이지(/cards/{card_id})
-> (/cards/questions),(/cards/profits), service = 'Best 카드 찾기 서비스'
banksalad 홈페이지 접속 -> 상단 "카드"탭아래나 메인화면의 "나의 BEST 카드 찾기" 선택 -> 소비패턴 입력(/cards/questions)
-> 사용자의 소비 패턴에 맞는 카드 리스트 노출 (랭킹) (/cards/profits) -> 원하는 조건의 카드 클릭 -> 신청 선택 
'''

bestCardExposure = nonReq[nonReq['path'].str.contains('/questions')]
bestCardReg = issueReqPV[issueReqPV['path'].str.contains('/profits')]
bestCardExposure.groupby(['category','card_name','card_id']).size()

bestCardExposure.groupby('action').size()
bestCardReg.groupby('category').size()

len(bestCardReg)
bestCardExposure.groupby(['category']).size()

'''
인기카드 추천 서비스
1. 인기 카드 추천 리스트 조회(/cards/ranking)
2. 카드 상세 정보 페이지(/cards/{card_id})
=> (/cards/ranking), service = '인기카드 추천 서비스'
banksalad 홈페이지 접속 -> 상단 "카드"탭 아래 "인기카드 top10" 선택 ->
-> 6개월간 인기 많은카드 리스트 top10 노출 -> 상세보기-> 카드신청
                                    -> 카드신청
홈페이지 상 ranking은 top10 만 노출
실제로는?
'''

# 신청/ 상품노출 둘다 존재
popularCard = event_cleaned[event_cleaned['path'].str.contains('/ranking')]
popularCvr = popularCard.groupby(['action']).size()[1]/popularCard.groupby(['action']).size()[0]*100

popularCardExposure = popularCard[popularCard['action'].str.contains('상품노출')]
popularCardReg = popularCard[popularCard['action'].str.contains('신청')]

# 신청이기 때문에 rank 정보 없음
# popularCardReg.groupby(['rank_in_list']).size().sort_values(ascending=False)

popularCardExposure.groupby(['card_name','rank_in_list','card_id']).size().sort_values(ascending=False)
# rank_in_list
event_cleaned.loc[event_cleaned.category == '카드:결과리스트'].rank_in_list
event_cleaned.category.value_counts()
event_cleaned.loc[event_cleaned.category == '카드:카드랭킹'].rank_in_list

'''
연회비 지원카드 추천 서비스
1. 연회비지원 카드리스트 조회(/cards/promotion/annual-fee)
2. 카드 상세 정보 페이지(/cards/{card_id})
=> path에 /cards/promotion/annual-fee 가 있으면 service = "연회비 지원 카드추천 서비스"
banksalad 홈페이지 접속 -> 상단 "카드"탭 아래 "연회비 지원 상품" 선택 ->
-> 연회비 지원 카드 리스트 노출 -> 상세보기-> 카드신청
                                   -> 카드신청
'''
annualfeeCard = event_cleaned[event_cleaned['path'].str.contains('/annual-fee')]
annualfeeCard.groupby(['action']).size()[1]/annualfeeCard.groupby(['action']).size()[0]*100

annualfeeCardPV = pd.merge(annualfeeCard, pageview_cleaned, on = ['date','path'],how = 'right')
annualfeeCardPV.groupby(['card_name','card_id']).size()

annualfeeCardPV.groupby(['card_name','card_id']).size()
annualfeeCard.columns
pageview_cleaned.groupby(['date']).size()

# %% THEMES (/cards/themes/)
# subset path that startswith('/cards/themes/')
themeCard = event_cleaned[event_cleaned['path'].str.contains('/themes')]
themeCard.groupby(themeCard['action']).size()
themeCard[['theme']] = themeCard['path'].str[14:].copy()

themeCard.groupby(['path']).size()

# Merge with PV
themeCard = pd.merge(themeCard,PV, on = ["path"], how= 'left',suffixes=('_event', '_pv'))


# theme ranking by pv
themeRanking = themeCard.groupby(['theme'])[['theme','total_pv']].size().sort_values(ascending=False)

themeCardReg = themeCard[themeCard['action'].str.contains('신청')]
themeCardExposure = themeCard[themeCard['action'].str.contains('상품노출')]

themeCardReg_df = themeCardReg.groupby(['theme']).size().reset_index()
themeCardExposure_df = themeCardExposure.groupby(['theme'])['theme','total_pv'].sum().reset_index()

themeCVR = pd.merge(themeCardReg_df,themeCardExposure_df, on  =['theme'],how = 'left')
themeCVR['CVR'] =  (themeCVR[0]/themeCVR['total_pv'])*100
themeCVR.sort_values(by= ['CVR'], ascending= False)

# 가장 인기 많은 theme
themeCard.groupby(['path']).size().sort_values(ascending=False)

# theme 별 신청자 수
themeCard.groupby(['action','path','card_name','card_id']).size()

# %% pageview plot
#################################################################################################################
plt.plot(pageview_cleaned.groupby(['date']).size())
xlab = 'pageviews'
ylab = 'date'
title = 'Pageview Per Day'

plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(title)

degrees = 70
# pgv_plot.xticks(rotation=degrees)

plt.show()

#%% 카드 시청 수 높이기 윈한 전략 수립
'''
실험 설계
1. 가설
ㅁㅁ 항목에서 카드 신청 수 부진의 이유는 ㅁㅁ이다.
2. ㅁㅁ의 이유로 신청 수가 부진하므로 ㅁㅁ 향상을 위한 방안 모색
3. ㅇㅇ를 하면 카드 신청 수가 늘어날 것이다. 를 증명하기 위해서는 ㅁㅁ을 하지 않았을 경우 신청자 수가 늘어나지 않는 것을 증명해야함.
5. Conclusion
ㅁㅁ 하지 않았을 경우 신청자수가 늘어나지 않고 적용했을 경우
신청자 수가 늘어나는 것을 확인 할 수 있으므로
ㅁㅁ을 집행하면 ㅁㅁ 항목에서의 카드 신청자수 부진을 해결할 수 있다.
ㅁㅁ을 집행하기 위해서 드는 비용은 ㅁㅁ이다.
'''
# Status Quo



# 카드 신청 수를 높이기 위한 방안을 1개 이상 제시
# 데이터 분석하여 취약한 카드 가입경로 분석

# 경로 별 cvr
# 노출 rank 별 cvr


# mainpage 접속
pageview.loc[pageview_cleaned.path == '/']

########################################################

#%% Visualization
# 월/일 별 데이터 정리
# 카드 종류별

'''
5. DataCleaning + Join
primary key
path column구성
'''

print("분석 대상 카드 수 : " + str(len(event_cleaned.card_id.unique())))
# 해당 과제의 목표는 데이터셋에 있는 366개의 카드들의 신청 수를 최대치로 만들기 위함.
print("분석 대상 카드사 수 : " + str(len(event_cleaned.card_name.unique())))


# CVR (카드 신청 전환)

# page path 분석


'''
현재 카드 신청수가 가장 많은 날은 ㅁ일이고 당일 banksalad 홈패이지 접속자수는 ㅁ 명이다.
접속자 수 ㅁ명 중 ㅁㅁ 경로를 통하여 카드 정보를 얻은 사람은 ㅁㅁ 명이고
이중 ㅁㅁ 명이 신청을 하였다.
신청자 수가 가장 적은 경로는 ㅁㅁ 경로이고 이탈률은 ㅁㅁ이다. 이탈이 일어난 이유가 ㅁㅁ이라고 가정했을때,
ㅁㅁㅁㅁ를 ㅁㅁ하여 실험을 설계하였다.
실험 과정은 다음을 따른다.
그러므로 ㅁㅁ 이벤트에서 ㅁㅁ을 진행하여 카드 information page에서의 이탈률이 줄어들게하여 카드 신청자 수를 늘릴 수 있다.
'''


'''
각 영역별 카드 신청 현황 파악을 위한 지표를 계산할 수 있고, 현황에 대해 올바르게 분석함.
'''




# Assumption -> Hypothesis -> Analysis -> Conclusion -> Validation
# 가정 : 좌측/ 상단에 가까이 노출 될수록 클릭 수가 높다
# hypothesis : 좌측 상단에 노출되는 항목이 conversion rate이
# conversion rate이 높은 ㅁㅁㅁ 서비스, ㅁㅁㅁ 테마를 상단에 노출 시킨다
# 실험 기간 :
# 실험 비용 :
