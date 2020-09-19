import pandas as pd
import json

# json data to df

# business = pd.read_json("./data/10100-1035793-bundle-archive/yelp_academic_dataset_business.json")
# checkin = pd.read_json("./data/10100-1035793-bundle-archive/yelp_academic_dataset_checkin.json")
# review = pd.read_json("./data/10100-1035793-bundle-archive/yelp_academic_dataset_review.json")
# tip = pd.read_json("./data/10100-1035793-bundle-archive/yelp_academic_dataset_tip.json")
# user = pd.read_json("./data/10100-1035793-bundle-archive/yelp_academic_dataset_user.json")

'''
각 데이터 별로 100,000 row의 data만 불러옴
'''

business = []
with open('./data/10100-1035793-bundle-archive/yelp_academic_dataset_business.json') as fl:
    for i, line in enumerate(fl):
        business.append(json.loads(line))
        if i+1 >= 100000:
            break
business_df = pd.DataFrame(business)

review = []
with open('./data/10100-1035793-bundle-archive/yelp_academic_dataset_review.json') as fl:
    for i, line in enumerate(fl):
        review.append(json.loads(line))
        if i+1 >= 100000:
            break
review_df = pd.DataFrame(review)

user = []
with open('./data/10100-1035793-bundle-archive/yelp_academic_dataset_user.json') as fl:
    for i, line in enumerate(fl):
        user.append(json.loads(line))
        if i+1 >= 100000:
            break
user_df = pd.DataFrame(user)

# %% eda

business_df.columns
review_df.columns
user_df.columns