from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('insertItems',views.IntblItemsAPI.as_view(),name='intblitemsinsertAPI'),


]
