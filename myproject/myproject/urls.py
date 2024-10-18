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
from django.contrib import admin
from django.urls import path,include
from myapp.views import  home
from myapp.views import  form_part2
from myapp.views import  login
from myapp.views import  search_province
from myapp.acceuil_views import acceuil
from myapp.views import mdp_oubliee
from myapp.acceuil_views import acceuilCte
from myapp.views import D_authentification



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('form-part2/', form_part2, name='form_part2'),
    path('login/', login, name='login'),
    path('search_province/', search_province, name='search_province'),
    path('acceuil/', acceuil, name='acceuil'),
    path('mdp_oubliee/', mdp_oubliee, name='mdp_oubliee'),
    path('acceuilCte/', acceuilCte, name='acceuilCte'),
    path('D_authentification/', D_authentification, name='D_authentification'),
    

]
