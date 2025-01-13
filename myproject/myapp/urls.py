# myapp/urls.py
from django.urls import path
from .views_mobile import GenreListAPIView , SitMatrimListAPIView,FokontanyViewList,inscription,login,send_code,validate_code,TransactionListAPI,api_transaction_details,api_profil,modifier_mot_de_passe_api

urlpatterns = [
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
    path('situations-matrimoniales/', SitMatrimListAPIView.as_view(), name='sitmatrim-list'),
    path('list_fokontany/', FokontanyViewList.as_view(), name='list_fokontany'),
    path('inscription/', inscription, name='inscription'),
    path('login/', login, name='login'),
    path('send_code/', send_code, name='send_code'),
    path('validate_code/', validate_code, name='validate_code'),
    path('transactions/', TransactionListAPI.as_view(), name='api_transactions'),
    path('api_transaction_details/<str:n_quit>/', api_transaction_details, name='api_transaction_details'),
    path('api_profil', api_profil, name='api_profil'),
    path('modifier_mot_de_passe_api', modifier_mot_de_passe_api, name='modifier_mot_de_passe_api')
]
