"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from myapp.views import  home
from myapp.views import  form_part2
from myapp.views import  login
from myapp.acceuil_views import  acceuils

from myapp.views import  deconnexion
from myapp.views import  search_province
from myapp.views import  modifier_contribuable
from myapp.acceuil_views import acceuil
from myapp.acceuil_views import dashboard

from myapp.views import mdp_oubliee
from myapp.acceuil_views import acceuilCte
# from myapp.acceuil_views import test_acceuil
from myapp.acceuil_views import home1
from myapp.acceuil_views import chart
from myapp.acceuil_views import discussion_admin
from myapp.acceuil_views import view_message
from myapp.acceuil_views import IS_calcul
from myapp.acceuil_views import IR_calcul
from myapp.acceuil_views import IRSA_calcul
from myapp.acceuil_views import list_transaction
from myapp.acceuil_views import profil
from myapp.acceuil_views import chart_line
from myapp.acceuil_views import discussion
from myapp.acceuil_views import notification
from myapp.acceuil_views import get_transaction_details
from myapp.acceuil_views import export_transaction_pdf
from myapp.acceuil_views import filtre_list_transaction
from myapp.acceuil_views import filtre_detail_transaction
# from myapp.acceuil_views import dashboard
from myapp.views import get_all_operateurs

from myapp.views import D_authentification



urlpatterns = [
    path('admin/', admin.site.urls),
    path('acceuils/', acceuils, name='acceuils'),
    path('home/', home, name='home'),
    path('form-part2/', form_part2, name='form_part2'),
    path('login/', login, name='login'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('search_province/', search_province, name='search_province'),
    path('acceuil/', acceuil, name='acceuil'),
    # path('test_acceuil/', test_acceuil, name='test_acceuil'),
    path('mdp_oubliee/', mdp_oubliee, name='mdp_oubliee'),
    path('acceuilCte/', acceuilCte, name='acceuilCte'),
    path('D_authentification/', D_authentification, name='D_authentification'),
    path('home1/', home1, name='home1'),
    path('profil/', profil, name='profil'),
    path('chart/', chart, name='chart'),
    path('chart_line/', chart_line, name='chart_line'),
    path('discussion_admin/', discussion_admin, name='discussion_admin'),
    path('view_message/<int:message_id>/', view_message, name='view_message'),
    path('discussion/', discussion, name='discussion'),
    path('notification/', notification, name='notification'),
    path('modifier_contribuable/', modifier_contribuable, name='modifier_contribuable'),
    path('dashboard/', dashboard, name='dashboard'),
    path('IS_calcul/', IS_calcul, name='IS_calcul'),
    path('IR_calcul/', IR_calcul, name='IR_calcul'),
    path('IRSA_calcul/', IRSA_calcul, name='IRSA_calcul'),
    path('get_all_operateurs/',get_all_operateurs, name='get_all_operateurs'),
    path('list_transaction/', list_transaction, name='list_transaction'),
    path('transaction_detail/<str:n_quit>/',get_transaction_details, name='transaction_detail'),
    path('export_transaction_pdf/<str:n_quit>/',export_transaction_pdf, name='export_transaction_pdf'),
    path('filtre_list_transaction/',filtre_list_transaction, name='filtre_list_transaction'),
    path('transaction_detail/<str:n_quit>/filtre_detail_transaction', filtre_detail_transaction, name='filtre_detail_transaction'),
    
]

if settings.DEBUG:  # Seulement en mode développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)