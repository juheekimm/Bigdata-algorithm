from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from django.core.management.base import BaseCommand

class Command(BaseCommand):




    # ============================================
    # -- Get TFIDF
    # ============================================

    def _initialize(self):

        corpus = ['동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
                  '남산 위에 저 소나무 철갑을 두른 듯 바람서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
                  '가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편단심일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
                  '이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
                  '오 필승 코리아 오 필승 코리아 오 필승 코리아 오 오레 오레 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세']
        vectorizer = TfidfVectorizer()
        sp_matrix = vectorizer.fit_transform(corpus)

        word2id = defaultdict(lambda : 0)
        for idx, feature in enumerate(vectorizer.get_feature_names()):
            word2id[feature] = idx

        for i, sent in enumerate(corpus):
            print('====== document[%d] ======' % i)
            print( [ (token, sp_matrix[i, word2id[token]]) for token in sent.split() ] )




    def handle(self, *args, **kwargs):
        self._initialize()

