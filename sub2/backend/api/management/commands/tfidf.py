from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from django.core.management.base import BaseCommand

class Command(BaseCommand):




    # ============================================
    # -- Get TFIDF
    # ============================================

    def _initialize(self):

        # corpus = ['동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
        #           '남산 위에 저 소나무 철갑을 두른 듯 바람서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
        #           '가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편단심일세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
        #           '이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세',
        #           '오 필승 코리아 오 필승 코리아 오 필승 코리아 오 오레 오레 무궁화 삼천리 화려 강산 대한사람 대한으로 길이 보전하세']
        corpus =['로이킴 : 봄 봄 봄 봄이 왔네요. 우리가 처음 만났던 그때의 향기 그대로. 그대여 너를 처음 본 순간 나는 바로 알았지',
                  '장범준 : 그대여 그대여 그대여 그대여. 봄바람 휘날리며 흩날리는 벚꽃 잎이. 울려 퍼질 이 거리를',
                '아이유 : 봄 사랑 벚꽃 말고 봄 사랑 벚꽃 말고']

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

