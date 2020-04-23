from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path

# router = DefaultRouter(trailing_slash=False)
# router.register(r"stores", views.StoreViewSet, basename="stores")

# urlpatterns = router.urls

urlpatterns = [
    url('searchAllStore', views.AllStoreList.as_view(), name="searchAllStore"),
    url('searchStore',views.SearchStore.as_view(),name="SearchStore"),
    url('SearchStoreforComplete',views.SearchStroeforComplete.as_view(),name="SearchStroeforComplete"),
    url('SearchReviewbyStoreId',views.SearchReviewbyStoreId.as_view(),name="SearchReviewbyStoreId"),
    url('SearchMenubyStoreId',views.SearchMenubyStoreId.as_view(),name="SearchMenubyStoreId"),
    url('SearchStorebyStoreId',views.SearchStorebyStoreId.as_view(),name="SearchStorebyStoreId"),
    url('SearchNearbyStore',views.searchNearbyStore.as_view(),name="searchNearbyStore"),
    url('writeReview',views.writeReview),
    url('updateReview',views.updateReview),
    url('deleteReview',views.deleteReview),
    # path('searchName/', views.search_storeName.as_view(), name="store"),
    # path('searchStore/', views.serachStore.as_view(), name="store"),
    # path('review/',views.reviewCRUD.as_view(),name="review")
    
]