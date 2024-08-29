"""
URL configuration for root project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.messages import api
from django.urls import path, include

from root import settings
from root.custom_token import CustomToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from root.custom_obtain_view import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('texnomart-uz/', include('texnomart.urls')),
    path('texnomart-uz/token-auth/',CustomToken.as_view()),
    path('texnomart-uz/api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('texnomart-uz/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
