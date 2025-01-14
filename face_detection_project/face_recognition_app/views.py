from django.http import HttpResponse
from django.shortcuts import render
import os
import json
from django.conf import settings


# # i have Created my views here.
# def upload_page(request):
#     if request.method == "POST":
#         # Placeholder for file handling (backend comes later)
#         return render(request, "results.html", {"matches": []})  # No matches yet
#     return render(request, "upload.html")

# Load metadata from the JSON file
import os
from django.conf import settings

from .models import Person  # Correct relative import


def metadata_display(request):
    metadata_path = os.path.join(settings.BASE_DIR, 'face_recognition_app', 'static', 'metadata.json')
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
        return render(request, 'display_metadata.html', {'metadata': metadata})
    except FileNotFoundError:
        return HttpResponse("Metadata file not found.", status=404)
def upload_page(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Handle the image processing here (e.g., saving the image, running face detection, etc.)
        # You can also redirect to another page or show the result based on your requirements.
        return render(request, 'upload.html', {'message': 'Image uploaded successfully!'})
    
    return render(request, 'upload.html')  # Return the upload page
