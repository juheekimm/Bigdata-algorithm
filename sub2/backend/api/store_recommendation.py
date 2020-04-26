from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel





# ============================================
# -- Get TFIDF
# ============================================
#
# def _initialize(self):
#     # output=self.recommendation_category_region("참닭발","죽전")
#     print(self.query_MySqlDB("SELECT * FROM django_test.api_store_menu;"))
#     output=self.recommendation_category_menu_distance(371163,2)
#     print("--------------------------추천해줄 다른 음식점-------------------------")
#     print(output)

# 상점id를 받고 거리를 받아 반경 {dis}km안에 있는 메뉴 유사 음식점 추천
def recommendation_menu_distance(store_id, dis):
    print("[*] Loading store data...")
    query_store = "SELECT * FROM django_test.api_store_menu where id="+str(store_id)
    store = query_MySqlDB(query_store)
    print(store.iloc[0].store_name)
    store_name=store.iloc[0].store_name
    store_lat=str(store.iloc[0].latitude)
    store_lon=str(store.iloc[0].longitude)
    print(store.iloc[0].latitude)
    print(store.iloc[0].longitude)
    query_distance="SELECT *,(6371*acos(cos(radians("+store_lat+"))*cos(radians(latitude))*cos(radians(longitude) " \
                   "-radians("+store_lon+"))+sin(radians("+store_lat+"))*sin(radians(latitude)))) " \
                   "AS distance FROM api_store_menu HAVING distance <= "+str(dis)+" ORDER BY distance"
    data = query_MySqlDB(query_distance)
    print("-data--------------------------------------------------------------")
    print(data)
    tfidf = TfidfVectorizer()
    data['menu'] = data['menu'].fillna('')
    del data['distance']
    tfidf_matrix = tfidf.fit_transform(data['menu'])
    # 현재 데이터 매트릭스 size 출력
    print("비교할 데이터 사이즈")
    print(tfidf_matrix.shape)

    # 코사인 유사도 측정
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(data.index, index=data['store_name']).drop_duplicates()
    # print(indices.head())

    idx = indices[store_name]

    # 우선 쿼리로 가져온 모든 상점에 대한 유사도를 구한다.
    sim_scores = list(enumerate(cosine_sim[idx]))
    print("우선 쿼리로 가져온 모든 상점에 대한 유사도를 구한다.")
    # print(sim_scores)
    # 유사도에 따라 상점들을 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 상점을 받아온다.
    sim_scores = sim_scores[1:11]

    # 가장 유사한 10개의 상점의 인덱스를 받아온다.
    store_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 상점의 제목을 리턴한다.
    return data.iloc[store_indices]


# 상점id를 받고 거리를 받아 반경 {dis}km안에 있는 카테고리 유사 음식점 추천
def recommendation_category_distance(store_id, dis):
    print("[*] Loading store data...")
    query_store = "SELECT * FROM django_test.api_store where id="+str(store_id)
    store = query_MySqlDB(query_store)
    print(store.iloc[0].store_name)
    store_name=store.iloc[0].store_name
    store_lat=str(store.iloc[0].latitude)
    store_lon=str(store.iloc[0].longitude)
    print(store.iloc[0].latitude)
    print(store.iloc[0].longitude)
    query_distance="SELECT *,(6371*acos(cos(radians("+store_lat+"))*cos(radians(latitude))*cos(radians(longitude) " \
                   "-radians("+store_lon+"))+sin(radians("+store_lat+"))*sin(radians(latitude)))) " \
                   "AS distance FROM api_store HAVING distance <= "+str(dis)+" ORDER BY distance"
    data = query_MySqlDB(query_distance)
    print("-data--------------------------------------------------------------")
    print(data)
    tfidf = TfidfVectorizer()
    data['category'] = data['category'].fillna('')
    del data['distance']
    tfidf_matrix = tfidf.fit_transform(data['category'])
    # 현재 데이터 매트릭스 size 출력
    print("비교할 데이터 사이즈")
    print(tfidf_matrix.shape)

    # 코사인 유사도 측정
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(data.index, index=data['store_name']).drop_duplicates()
    # print(indices.head())

    idx = indices[store_name]

    # 우선 쿼리로 가져온 모든 상점에 대한 유사도를 구한다.
    sim_scores = list(enumerate(cosine_sim[idx]))
    # print("우선 쿼리로 가져온 모든 상점에 대한 유사도를 구한다.")
    # print(sim_scores)
    # 유사도에 따라 상점들을 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 상점을 받아온다.
    sim_scores = sim_scores[1:11]

    # 가장 유사한 10개의 상점의 인덱스를 받아온다.
    store_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 상점의 제목을 리턴한다.
    return data.iloc[store_indices]


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
    # engine = create_engine("mysql+mysqldb://root:ssafy@52.79.223.182/django_test",
    #                        encodeing='utf-8')
    conn = engine.connect()

    generator_df = pd.read_sql(sql=query,  # mysql query
                               con=conn)
    # chunksize = 3
    # size you want to fetch each time

    # for dataframe in generator_df:
    # for row in dataframe:
    #     pass
    # whatever you want to do

    # print(generator_df)
    return generator_df

    #
    #
    # def handle(self, *args, **kwargs):
    #     self._initialize()

