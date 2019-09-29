
"""recorridos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url, include
from socios.views import SociosCRUD, FiltroCRUD, IndexView, DomiciliosCRUD
from django.apps import apps
from cruds_adminlte.urls import crud_for_model

from cruds_adminlte.urls import crud_for_app
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

sociosCRUD = SociosCRUD()
filtrosCRUD = FiltroCRUD()
domiciliosCRUD = DomiciliosCRUD()

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    path('admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'}),
    re_path(r'', include(filtrosCRUD.get_urls())),
    re_path(r'', include(sociosCRUD.get_urls())),
    re_path(r'', include(domiciliosCRUD.get_urls())),
]


urlpatterns += crud_for_app('auth', login_required=True, cruds_url='lte')


