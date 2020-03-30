

from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include

from entradas.views import EventoCRUD, PedidoCRUD

from socios.views import SociosCRUD, FiltroCRUD, IndexView, DomiciliosCRUD

from django.apps import apps
from cruds_adminlte.urls import crud_for_model

from cruds_adminlte.urls import crud_for_app
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

sociosCRUD = SociosCRUD()
filtrosCRUD = FiltroCRUD()
domiciliosCRUD = DomiciliosCRUD()

eventoCRUD = EventoCRUD()
pedidoCRUD = PedidoCRUD()

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': '/'}),
    url(r'^login/$', IndexView.as_view()),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'', include(filtrosCRUD.get_urls())),
    re_path(r'', include(sociosCRUD.get_urls())),
    re_path(r'', include(domiciliosCRUD.get_urls())),
    re_path(r'', include(eventoCRUD.get_urls())),
    re_path(r'', include(pedidoCRUD.get_urls())),
    path('admin/', admin.site.urls),
]


urlpatterns += crud_for_app('auth', login_required=True, cruds_url='lte')


