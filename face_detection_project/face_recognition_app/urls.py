from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # path("upload/", views.upload_page, name="upload_page"),
    # path('upload/', views.match_faces, name='upload'),
   
    path('upload/', views.upload_page, name='upload_page'),
    # path('metadata/', views.metadata_display, name='metadata_display'),
    path('show_all_data/', views.show_all_data, name='show_all_data'),
    path('display_metadata/', views.display_metadata, name='display_metadata'),


] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)