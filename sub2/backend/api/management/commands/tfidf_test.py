from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
from backend import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Command(BaseCommand):




    # ============================================
    # -- Get TFIDF
    # ============================================
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = DATA_DIR / "movies_metadata.csv"

    def _load_dataframes(self):
        try:
            data_to_return = pd.read_csv(Command.DATA_FILE,low_memory=False)

        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data_to_return

    def _get_recommendations(self, title, cosine_sim, indices, data):
        idx = indices[title]

        # 모든 영화에 대해서 해당 영화의 유사도를 구한다.
        sim_scores = list(enumerate(cosine_sim[idx]))

        # 유사도에 따라 영화들을 정렬한다.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 가장 유사한 10개의 영화를 받아온다.
        sim_scores = sim_scores[1:11]

        # 가장 유사한 10개의 영화의 인덱스를 받아온다.
        movie_indices = [i[0] for i in sim_scores]

        # 가장 유사한 10개의 영화의 제목을 리턴한다.
        return data['title'].iloc[movie_indices]

    def _initialize(self):

        print("[*] Loading movie_data...")

        data = self._load_dataframes()
        data=data.head(20000)
        print("-data--------------------------------------------------------------")
        print(data['overview'])
        tfidf = TfidfVectorizer(stop_words='english')
        data['overview'] = data['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(data['overview'])
        #현재 데이터 매트릭스 size 출력
        print(tfidf_matrix.shape)

        # 코사인 유사도 측정
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        print("코사인 유사도")
        print(cosine_sim)

        indices = pd.Series(data.index, index=data['title']).drop_duplicates()
        print(indices.head())

        #영화 타이틀의 인덱스를 출력해준다.
        # idx = indices['Father of the Bride Part II']
        # # print("idx: "+idx)

        output=self._get_recommendations('The Dark Knight Rises',cosine_sim, indices, data)

        print(output)

    def handle(self, *args, **kwargs):
        self._initialize()

