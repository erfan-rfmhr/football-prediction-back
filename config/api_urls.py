from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),

    path('competitions/', include('apps.competitions.urls')),
]
