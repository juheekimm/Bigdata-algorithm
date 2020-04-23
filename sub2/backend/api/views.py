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
import json

from django.utils import timezone


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

class SearchStorebyStoreId(APIView):
    def post(self, request):
        if 'storeId' in request.POST.keys():
            storeId = request.POST['storeId']

            queryset = Store.objects.all().filter(id=storeId)
            serializer = StoreSerializer(queryset, many = True)
            return Response(serializer.data)
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})

# 리뷰쓰기
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

    #profileID(token)와 리뷰글쓴이ID가 같으지 확인 해야 함.

    queryset = Profile.objects.get(user_id=id_token)
    queryset_string = serialize('json', queryset)
    # queryset_json = json.loads(queryset_string)
    # user_id = queryset_json['pk']

    print(queryset_json)

    # data = Review.objects.get(id=review_id)

    # print(review_id+" sdfsdlfjsdklfjsdkljfklsdjfklsdjf")
    # #리뷰 아이디와 tokenId가 같은지 확인
    
    # if(id_user == id_token):
    #     ## id_user로 profile Id 찾기
        

    #     #리뷰쓴 사람과 토큰 보낸 사람이 같은지 다시한번 확인
    #     if(int(user_id) != int(data.user_id)):
    #         return Response({"state" : "fail", "message" : "수정 가능한 아이디가 아닙니다.", })

    #     #리뷰 업데이트
    #     data.content = content
    #     data.total_score = total_score
    #     print(timezone.now())
    #     data.reg_time = timezone.now()

    #     data.save()

    #     return Response({"state" : "success", "message" : "수정에 성공했습니다."})
    # else:
    #     return Response({"state" : "fail", "message" : "수정 가능한 아이디가 아닙니다.", })

#CRUD 
class reviewCRUD(APIView):

    #Create
    def post(self, request):
        ## session의 값과 userId값이 같으지 확인해야함^^^^^^^^
        if ('user' in request.POST.keys()) and ('store' in request.POST.keys()) and ('content' in request.POST.keys()):
            user = request.POST['user']
            store = request.POST['store']
            content = request.POST['content']
            
            store = Store.objects.get(store=store)

            data = Review(user=user,content=content)
            data.store = store
            data.save()
            stat=status.HTTP_200_OK
        else :
            stat=status.HTTP_400_BAD_REQUEST
            
        return Response({'status': stat})

    #Read store, user 에 따라 읽는다.
    def get(self, request):
        if 'condition' in request.POST.keys() and 'keyword' in request.POST.keys():
            condition = request.POST['condition']
            keyword = request.POST['keyword']
            if(condition == "store"):
                queryset = Review.objects.all().filter(store=keyword).select_related()
            elif(condition == "user"):
                queryset = Review.objects.all().filter(user=keyword).select_related()
            serializer = StoreReviewSerializer(queryset, many=True)
            return Response({'status': status.HTTP_200_OK})
        else :
            return Response({'status': status.HTTP_400_BAD_REQUEST})
    
    #Update 
    def put(self,request):
        ## session 확인
        try:
            if 'content' in request.POST.keys() and 'id' in request.POST.keys():
                id = request.POST["id"]
                content = request.POST["content"]
                data =  Review.objects.get(id=id)
                data.content = content
                # print("*****************"+id+" "+content)
                data.save()
                return Response({'status': status.HTTP_200_OK})
        except:
            return Response({'status': status.HTTP_400_BAD_REQUEST})

    #Delete review Id
    def delete(self, request):
        ## sessionId와 들어오는 아이디가 같은지 확인해야함.*******
        try :
            id = request.POST['id']
            data = Review.objects.get(id=id)
            data.save()
            return Response({'status': status.HTTP_200_OK})
        except :
            return Response({'status': status.HTTP_400_BAD_REQUEST})


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

