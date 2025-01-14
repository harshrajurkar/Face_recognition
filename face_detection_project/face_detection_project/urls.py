"""
URL configuration for face_detection_project project.

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
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include

# from face_recognition_app import admin


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('face_recognition/', include('face_recognition_app.urls')),
# ]

# # Add this to serve media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from face_recognition_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('face_recognition/', include('face_recognition_app.urls')),
]
