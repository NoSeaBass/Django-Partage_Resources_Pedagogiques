from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('authentification.urls', namespace='authentification')),
    path('admin-app/', include('administrateur.urls', namespace='administrateur')),
    path('app/', include('utilisateurs.urls', namespace='utilisateurs'))
]
