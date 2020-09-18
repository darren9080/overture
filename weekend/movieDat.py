import pandas as pd
import numpy as np
import re

# https://grouplens.org/datasets/movielens/

movies_col =['movie_id','movie_name','genre']
movies = pd.read_table('D:/PycharmProjects/overture/data/pfda/ml-1m/movies.dat',sep = '::',header= None,names = movies_col, engine = 'python')

ratings_col =['user_id','movie_id','rating','timestamp']
ratings = pd.read_table('D:/PycharmProjects/overture/data/pfda/ml-1m/ratings.dat',sep = '::',header= None,names = ratings_col, engine = 'python')

users_col = ['user_id','gender','age','occupation','zip_code']
users = pd.read_table('D:/PycharmProjects/overture/data/pfda/ml-1m/users.dat',sep = '::',header= None,names= users_col, engine = 'python')

mv_rt = pd.merge(movies, ratings, on = "movie_id", how = "left")

mv_rating = pd.merge(mv_rt, users, on = "user_id", how = 'left' )


occupation_dict = {0: "other"
,1: "academic/educator"
,2: "artist"
,3: "clerical/admin"
,4: "college/grad student"
,5: "customer service"
,6: "doctor/health care"
,7: "executive/managerial"
,8: "farmer"
,9: "homemaker"
,10: "K-12 student"
,11: "lawyer"
,12: "programmer"
,13: "retired"
,14: "sales/marketing"
,15: "scientist"
,16: "self-employed"
,17: "technician/engineer"
,18: "tradesman/craftsman"
,19: "unemployed"
,20: "writer"}

# occupation title merge
occupation_df = pd.DataFrame.from_dict(occupation_dict,orient='index', columns =["occupation_title"]).reset_index()
mv_rating = pd.merge(mv_rating, occupation_df, left_on = 'occupation' , right_on = 'index', how = 'left')


bins = [0,18,24,34,44,55,100]
labels = ['Under 18', '18-24', '25-34', '35-44', '45-55','56+']

mv_rating['age_range'] = pd.cut(x=mv_rating['age'], bins=bins,
                    labels= labels, include_lowest= True)

mv_rating[['age','age_range']]


#4 mv_rating의 영화 제목 컬럼에서 개봉 연도를 분리해서 추가 컬럼을 생성해 주세요.
# mv_rating["year"]

def split_it(year):
    return re.findall('\(.*?\)', year)


mv_rating["year"] = mv_rating.movie_name.apply(lambda x : re.findall('(?<=\()\d+', x)[0])

#5 전체 영화의 개수와 평균 평점, 평점 개수를 구해 출력해 주세요.

# 전체 영화 갯수
total_movie_num = mv_rating.movie_name.nunique()

#5
# 평균 평점
avg_rating = mv_rating.rating.mean()

# 평균 평점 갯수
avg_rating_by_mv = mv_rating["movie_name"].value_counts().mean()

print(f"총 영화 갯수 :{total_movie_num} \n 평균 평점 :{avg_rating:.2f} \n 영화 별 평균 평점 갯수: {avg_rating_by_mv:.2f}")


#6 영화별 평균 평점/ 평점 갯수 구하고 dataframe칼럼으로 추가
movies_info = pd.DataFrame()

func_list = ["size","mean"]



movies_info = mv_rating[["movie_name","rating"]].groupby(mv_rating["movie_name"]).agg(func_list)
movies_info.columns = movies_info.columns.droplevel(0)
movies_info.reset_index(inplace= True)

movies_info = movies_info.drop( columns = ["index"])
movies_info = movies_info.rename(columns = {'' : "movieName","size": "numberOfReviews", "mean":"averageRating"})

#7
movies_info.sort_values(by = ["averageRating","numberOfReviews"], ascending = False)
movies_info.sort_values(by = ["numberOfReviews"], ascending = False)


## userPreference
