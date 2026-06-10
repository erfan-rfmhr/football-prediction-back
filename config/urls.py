from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include('djoser.urls.jwt')),
    re_path(r'^api/', include('djoser.urls')),
    path('api/', include('tournaments.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
