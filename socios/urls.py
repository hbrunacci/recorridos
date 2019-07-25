from cruds_adminlte.urls import crud_for_app

app_name = 'socios'

urlpatterns = []

urlpatterns += crud_for_app(app_name)