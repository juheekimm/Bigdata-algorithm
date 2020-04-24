from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from api import models

class Command(BaseCommand):


    def _initialize(self):
        # models.Store_menu.objects.all().delete()

        query_store="SELECT * FROM django_test.api_store where id="
        # query_menu="SELECT * FROM django_test.api_menu where id between 1 and 50000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 50001 and 100000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 100001 and 150000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 150001 and 200000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 200001 and 250000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 250001 and 300000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 300001 and 400000;"
        # query_menu="SELECT * FROM django_test.api_menu where id between 400001 and 550000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 550001 and 700000"
        # query_menu="SELECT * FROM django_test.api_menu where id between 700001 and 1000000"

        # query_menu="SELECT * FROM django_test.api_menu where id between 1000001 and 1200000"

        # query_menu="SELECT * FROM django_test.api_menu where id between 1200001 and 1500000"

        query_menu="SELECT * FROM django_test.api_menu where id between 1500001 and 1651857"


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

        print("[*] loading menus...")
        menus = pd.read_sql(sql=query_menu,  # mysql query
                                   con=conn)
        print(menus)
        # menus= menus.head(10)
        print("[*] Initializing store_menus...")

        Store_menus_bulk = []
        tmp_store_id=menus.iloc[0].store_id
        print("temp store id: "+ str(tmp_store_id))
        store = pd.read_sql(sql=query_store + str(tmp_store_id),  # mysql query
                             con=conn)
        print(store.iloc[0].id)
        #일단 1번째 인덱스의 store 정보 부터 가져온다.

        temp=""
        for menu in menus.itertuples():
            now_store_id = menu.store_id
            if tmp_store_id != now_store_id: # 저장시작
                Store_menus_bulk.append(
                    models.Store_menu(
                    id=store.iloc[0].id,
                    store_name=store.iloc[0].store_name,
                    branch=store.iloc[0].branch,
                    area=store.iloc[0].area,
                    tel=store.iloc[0].tel,
                    address=store.iloc[0].address,
                    latitude=store.iloc[0].latitude,
                    longitude=store.iloc[0].longitude,
                    category=store.iloc[0].category,
                    menu = temp+"|"+store.iloc[0].category
                    )
                )
                tmp_store_id=now_store_id
                temp=""
                temp+=menu.menu_name
                store = pd.read_sql(sql=query_store + str(tmp_store_id),  # mysql query
                                    con=conn)
            else : #상점번호가 같다면 temp란 str에 메뉴이름을 계속 추가한다.
                temp +="|"+menu.menu_name


        models.Store_menu.objects.bulk_create(Store_menus_bulk)
        print("[*] query ["+query_menu+"] is completed")
    def handle(self, *args, **kwargs):
        self._initialize()

