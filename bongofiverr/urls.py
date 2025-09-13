from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Bongo Fiverr API",
        default_version="v1",
        description="API documentation for Bongo Fiverr Platform",
        contact=openapi.Contact(email="support@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

@api_view(['GET'])
def api_root(request):
    return Response({
        "users": "/api/users/",
        "services": "/api/services/",
        "swagger": "/swagger/",
    })

urlpatterns = [
    path('', lambda request: redirect('schema-swagger-ui')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/', api_root, name='api-root'),
    path('api/users/', include('users.urls')),       
    path('api/services/', include('market.urls')),   
]