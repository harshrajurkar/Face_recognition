# from django.urls import path
# from . import views

# urlpatterns = [
#     path("upload/", views.upload_page, name="upload_page"),
#     path('display_metadata/', views.display_metadata, name='display_metadata'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_page, name="upload_page"),
    path('metadata/', views.metadata_display, name='metadata_display'),  # Add this URL pattern
]
