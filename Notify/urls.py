from django.contrib import admin
from django.urls import path, include
from university_lectures import urls, views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include(urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.CustomAuthToken.as_view())
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)