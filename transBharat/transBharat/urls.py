"""
URL configuration for transBharat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularAPIView,
    SpectacularRedocView,
)
from transBharat.core.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", jwt_views.TokenObtainPairView.as_view(), name="get_token_pair"),
    path("api/logout/", jwt_views.TokenBlacklistView.as_view(), name="logout"),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refesh"
    ),
    path("api/", include("transBharat.translation.urls"), name="translation_api"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("auth/", include("djoser.urls"), name="djoser_auth"),
    path("auth/", include("djoser.urls.jwt"), name="djoser_auth_jwt"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
