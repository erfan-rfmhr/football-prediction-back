from django.urls import include, path

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),

    path('competitions/', include('apps.competitions.urls')),
    path('accounts/', include('apps.accounts.urls')),
]
