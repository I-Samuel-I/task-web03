
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account.views import UserView

router = DefaultRouter()
router.register(r'users', UserView, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('account.urls')),
    path('api/v1/', include(router.urls)),
]
