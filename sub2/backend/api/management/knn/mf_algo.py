import pandas as pd
# import sklearn as sk
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sklearn.metrics.pairwise import cosine_similarity

#아이템 기반 협업 필터링
def query_MySqlDB(query):
    # sqlalchemy engine
    engine = create_engine(URL(
        drivername="mysql",
        username="root",
        password="ssafy",
        host="52.79.223.182",
        port="3306",
        database="django_test",
        query = {'charset': 'utf8mb4'}
    ))

    conn = engine.connect()

    generator_df = pd.read_sql(sql=query,  # mysql query
                            con=conn)
                            # chunksize = 3
                            # size you want to fetch each time

    # print(generator_df)
    return generator_df

user_data = query_MySqlDB("select id as user_id, gender, age from accounts_profile")
review_data = query_MySqlDB("select user_id, store_id, total_score from api_review")
store_data = query_MySqlDB("select id as store_id, store_name, address from api_store where address like '서울특별시 강남구%%'")

review_store_data = pd.merge(review_data, store_data, on="store_id")        #store 이름, 아이디, 주소 조인
user_review_rating = pd.merge(user_data, review_store_data, on="user_id")   #user_id, 성별, 나이, stroe 이름, 아이디, 주소 조인

# print("-----------")
# print(user_review_rating.head(2))

review_user_rating = user_review_rating.pivot_table("total_score", index="store_name", columns="user_id")
user_review_rating = user_review_rating.pivot_table("total_score", index="user_id", columns="store_name")

# print(user_review_rating.head(5))
# print(review_user_rating.head(5))

review_user_rating.fillna(0, inplace = True)
# print(review_user_rating.head(5))

item_based_collabor = cosine_similarity(review_user_rating) 

item_based_collabor = pd.DataFrame(data = item_based_collabor, index = review_user_rating.index, columns=review_user_rating.index)
# print(item_based_collabor.head())
print(item_based_collabor)

def get_item_based_collabor(store_name):
    return item_based_collabor[store_name].sort_values(ascending=False)[:6]

print(get_item_based_collabor('아비꼬'))