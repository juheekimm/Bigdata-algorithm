import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def query_MySqlDB(query):
    # sqlalchemy engine
    engine = create_engine(URL(
        drivername="mysql",
        username="root",
        password="ssafy",
        host="52.79.223.182",
        port="3306",
        database="django_test"
    ))

    conn = engine.connect()

    generator_df = pd.read_sql(sql=query,  # mysql query
                            con=conn)
                            # chunksize = 3
                            # size you want to fetch each time

    # for dataframe in generator_df:
        # for row in dataframe:
        #     pass
        # whatever you want to do

    print(generator_df)
    return generator_df

query_MySqlDB("select id, total_score from api_review")