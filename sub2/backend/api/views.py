from .models import *
from .serializers import *
from api import models, serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from haversine import haversine
from django.core.serializers import serialize

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import jwt
from backend.settings import JWT_AUTH
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
import json
from django.utils import timezone

# add juheekim
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        queryset = (
            models.Store.objects.all().filter(store_name__contains=name).order_by("id")
        )
        return queryset

class AllStoreList(APIView):
    def get(self, request, format=None):
        queryset = Store.objects.all()[:10]
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchStore(APIView):

    def get_query(self,condition,keyword):
        try :
            if(condition == 'storeId'):
                return Store.objects.all().filter(id=keyword)
            elif(condition == 'storeName'):
                return Store.objects.all().filter(store_name__contains=keyword)
            elif(condition == 'storeAddress'):
                return Store.objects.all().filter(address__contains=keyword)
            else:
                raise Http404
        except :
            raise Http404
 
    def post(self, request):
        if 'condition' in request.POST.keys() and 'keyword' in request.POST.keys() and 'count' in request.POST.keys() and 'size' in request.POST.keys():
            condition = request.POST['condition']
            keyword = request.POST['keyword']
            count = int(request.POST['count'])
            size = int(request.POST['size'])
            queryset = self.get_query(condition,keyword)[(count*size):(count*size)+size]
        else :
            queryset = Store.objects.all()[:10]
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)

# autoComplete를 위한 REST
class SearchStroeforComplete(APIView):
 
    def post(self, request):
        
        for key in request.POST.keys():
            print(key, ":", request.POST[key])

        if 'keyword' in request.POST.keys():
            keyword = request.POST['keyword']
            queryset = Store.objects.all().filter(store_name__contains=keyword).values('store_name').distinct()[:10]
        else:
            queryset = []

        serializer = StoreNameSerializer(queryset, many=True)
        return Response(serializer.data)

# 상점Id를 이용해서 리뷰(와 결합된 유저포함)들을 검색합니다.
class SearchReviewbyStoreId(APIView):

    def post(self, request):
        if 'storeId' in request.POST.keys():
            storeId = request.POST['storeId']

            queryset = Review.objects.all().filter(store=storeId).select_related().order_by('-reg_time')
            serializer = ReviewUserSerializer(queryset, many = True)
            return Response(serializer.data)
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

# 상점Id를 이용해서 메뉴들을 검색합니다.
class SearchMenubyStoreId(APIView):
    def post(self, request):
        if 'storeId' in request.POST.keys():
            storeId = request.POST['storeId']

            queryset = Menu.objects.all().filter(store_id=storeId)
            serializer = MenuSerializer(queryset, many = True)
            return Response(serializer.data)
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

# 상점Id를 이용해서 상점 정보 검색
class SearchStorebyStoreId(APIView):
    def post(self, request):
        if 'storeId' in request.POST.keys():
            storeId = request.POST['storeId']

            queryset = Store.objects.all().filter(id=storeId)
            serializer = StoreSerializer(queryset, many = True)
            return Response(serializer.data)
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

# 리뷰 쓰기
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def writeReview(request,user=None):
    
    #token에서 user_id 추출하기
    token = request.headers['Authorization'][4:]
    payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
    id_user = payload['user_id']

    #id_user로 profile id 알아내기
    queryset = Profile.objects.all().filter(user_id=id_user)
    queryset_string = serialize('json', queryset)
    queryset_json = json.loads(queryset_string)
    user_id = queryset_json[0]['pk']

    #request.body
    total_score = request.POST['total_score']
    content = request.POST['content']
    store_id = request.POST['store_id']

    #
    data = Review(total_score=total_score,content=content,store_id=store_id,user_id=user_id)
    data.save()

    # print(request.POST)

    return Response({"ok" : payload['user_id'], })

# 리뷰 수정
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def updateReview(request,user=None):
    
    #token에서 user_id 추출하기
    token = request.headers['Authorization'][4:]
    payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
    id_token = int(payload['user_id'])

    total_score = request.POST['total_score']
    content = request.POST['content']
    store_id = request.POST['store_id']
    review_id = request.POST['reviewId']
    id_user = int(request.POST['userId'])

    # print(total_score+" | "+content+" | "+store_id)
    # print(id_token," | ",id_user)
    #리뷰 아이디와 tokenId가 같은지 확인
    
    if(id_user == id_token):
        ## id_user로 profile Id 찾기
        queryset = Profile.objects.all().filter(user_id=id_user)
        queryset_string = serialize('json', queryset)
        queryset_json = json.loads(queryset_string)
        user_id = queryset_json[0]['pk']

        data = Review.objects.get(id=review_id)

        #리뷰쓴 사람과 토큰 보낸 사람이 같은지 다시한번 확인
        if(int(user_id) != int(data.user_id)):
            return Response({"state" : "fail", "message" : "수정 가능한 아이디가 아닙니다.", })

        #리뷰 업데이트
        data.content = content
        data.total_score = total_score
        data.reg_time = timezone.now()
        # print(timezone.now())

        data.save()

        return Response({"state" : "success", "message" : "수정에 성공했습니다."})
    else:
        return Response({"state" : "fail", "message" : "수정 가능한 아이디가 아닙니다.", })

# 리뷰 삭제
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def deleteReview(request,user=None):
    
    #token에서 user_id 추출하기
    token = request.headers['Authorization'][4:]
    payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
    id_token = int(payload['user_id'])

    #parm
    review_id = request.POST['reviewId']

    #profileUserId(token)와 리뷰글쓴이ID가 같으지 확인 해야 함.
    queryset = Review.objects.get(id=review_id)
    ReviewUserId = int(queryset.user_id)
    queryset = Profile.objects.get(id=ReviewUserId)
    profileUserId = int(queryset.user_id)

    # tokonid와 reivew 글쓴이의 id가 같다.
    if(id_token == profileUserId):
        print("ddd")
        instance = Review.objects.get(id=review_id)
        instance.delete()
        return Response({"state" : "success", "message" : "삭제에 성공했습니다.", })
    else:
        return Response({"state" : "fail", "message" : "삭제권한이 없습니다.", })

# 위치(경도,위도)를 이용해서 근처(distance) 상점 찾아보기
class searchNearbyStore(APIView):
    def post(self, request):

        ## session의 값과 userId값이 같으지 확인해야함^^^^^^^^
        if ('latitude' in request.POST.keys()) and ('longitude' in request.POST.keys()) and ('distance' in request.POST.keys()):
            curla = request.POST['latitude']
            curlo = request.POST['longitude']
            distance = request.POST['distance']

            mile = float(distance) * 0.621371
            
            # queryset = Store.objects.all().filter(self.calculateMeter(curla,curlo,latitude,longitude.distance))
            # queryset = Store.objects.all().filter(id=149)
            queryset = Store.objects.raw("SELECT *, ( 3959 * acos( cos( radians("
                + str(curla) +") ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians("
                + str(curlo) +") ) + sin( radians("
                + str(curla) +") ) * sin( radians( latitude ) ) ) ) as distance from api_store Having distance <"
                + str(mile) +";")
            serializer = serializer = StoreSerializer(queryset, many = True)

            return Response(serializer.data)
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})
            
    def calculateMeter(self,curx,cury,x,y,distance):

        curPosition = (curx,cury)
        position = (x,y)

        meter = haversine(curPosition,position)

        if(meter <= distance):
            return True
        else:
            return False

# 토큰을 이용해 유저 정보 가져오기
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def UserbyToken(request,user=None):
    
    #token에서 user_id 추출하기
    token = request.headers['Authorization'][4:]
    payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
    id_token = int(payload['user_id'])

    #user_id로 프로필정보 뽑아내기
    queryset = Profile.objects.all().filter(user_id=id_token)
    serializer = ProfileSerializer(queryset, many = True)

    return Response(serializer.data)


# 토큰을 이용해 유저가 쓴 리뷰들 가져오기
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def UserReviewbyToken(request,user=None):
    
    #token에서 user_id 추출하기
    token = request.headers['Authorization'][4:]
    payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
    id_token = int(payload['user_id'])

    #user_id로 프로필id 뽑아내기
    queryset = Profile.objects.get(user_id=id_token)
    profileId = queryset.id

    #프로필id로 review찾기
    queryset = Review.objects.all().filter(user_id=profileId).select_related().order_by('-reg_time')
    serializer = ReviewStoreSerializer(queryset, many = True)

    return Response(serializer.data)

# add juheekim
def conn_create():
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
    return conn

def query_MySqlDB(query):
    # sqlalchemy engine
    # engine = create_engine(URL(
    #     drivername="mysql",
    #     username="root",
    #     password="ssafy",
    #     host="52.79.223.182",
    #     port="3306",
    #     database="django_test",
    #     query = {'charset': 'utf8mb4'}
    # ))

    # conn = engine.connect()
    conn = conn_create()
    result = conn.execute(query)
    print(result)

    return result


def queryPandas(query) :
    conn = conn_create()
    generator_df = pd.read_sql(sql=query, con=conn)
                    
    return generator_df

# 사용자의 연령, 성별 정보를 이용하여 추천음식점 검색
# 같은 연령대, 성별을 가진 사람들이 높게 평가한 음식점 리스트를 반환
class storeRecobyUserInfo(APIView):
    def post(self, request):
        req = json.loads(request.body)
        keys = req.keys()
        print('age' in keys)
        if ('age' in keys and 'gender' in keys):
        
            age = int((timezone.now().year - int(req['age']) + 1) / 10) * 10
            print(age)
            gender = req['gender']

            return Response(query_MySqlDB("select count(store_id) count, avg(total_score) avg, store_id"
                + " from api_review r"
                + " join accounts_profile p"
                + " on r.user_id = p.id" 
                    + " and p.age <= (year(now()) - " + str(int(age)) + ")"
                    + " and p.age > (year(now()) - " + str(int(age) + 9) + ")"
                    + " and p.gender = '" + str(gender) + "'"
                + " group by store_id"
                + " having count(store_id) >= 2"
                    + " and avg(total_score) >= 4.5"
                + " order by count desc, avg desc"
                + " limit 5;"))
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

class matrixFactorization(APIView):
    def post(self, request):
        req = json.loads(request.body)
        keys = req.keys()
        if ('address' in keys and 'store_id' in keys):
            address = req['address']
            store_id = req['store_id']
            print(type(store_id))

            user_data = queryPandas("select id as user_id, gender, age from accounts_profile")
            review_data = queryPandas("select user_id, store_id, total_score from api_review")
            store_data = queryPandas("select id as store_id, address from api_store where address like '" + address + "%%'")

            review_store_data = pd.merge(review_data, store_data, on="store_id")        #store 이름, 아이디, 주소 조인
            user_review_rating = pd.merge(user_data, review_store_data, on="user_id")   #user_id, 성별, 나이, stroe 이름, 아이디, 주소 조인

            review_user_rating = user_review_rating.pivot_table("total_score", index="store_id", columns="user_id")
            user_review_rating = user_review_rating.pivot_table("total_score", index="user_id", columns="store_id")
            review_user_rating.fillna(0, inplace = True)

            item_based_collabor = cosine_similarity(review_user_rating) 
            item_based_collabor = pd.DataFrame(data = item_based_collabor, index = review_user_rating.index, columns=review_user_rating.index)
           
            # 이거 int로 안해주면 계속 오류남..ㅜㅜ
            print(item_based_collabor[int(store_id)].sort_values(ascending=False)[1:6])
            return Response(item_based_collabor[int(store_id)].sort_values(ascending=False)[1:6].reset_index()["store_id"])

        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
# def confirmUpdateReview(request,user=None):
    
#     #token에서 user_id 추출하기
#     token = request.headers['Authorization'][4:]
#     payload = jwt.decode(token, JWT_AUTH['JWT_SECRET_KEY'], JWT_AUTH['JWT_ALGORITHM'])
#     id_token = payload['user_id']

#     total_score = request.POST['total_score']
#     content = request.POST['content']
#     store_id = request.POST['store_id']

#     print(total_score+" | "+content+" | "+store_id)
#     #리뷰 아이디와 tokenId가 같은지 확인
#     id_user = request.POST['id']
#     if(id_user == id_token):
#         return Response({"ok" : "수정가능", })
#     else:
#         return Response({"ok" : '수정불가', })