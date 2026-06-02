from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('authentification.urls', namespace='authentification')),
    path('admin-app/', include('administrateur.urls', namespace='administrateur')),
    path('app/', include('utilisateurs.urls', namespace='utilisateurs'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
