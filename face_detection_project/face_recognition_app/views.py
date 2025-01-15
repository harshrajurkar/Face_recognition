import face_recognition
import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import numpy as np
from face_recognition_app.utils import load_metadata, store_dataset_encodings
from .models import Person


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_page(request):
    context = {}
    dataset_folder = os.path.join(settings.BASE_DIR, 'face_recognition_app/static/images')
    store_dataset_encodings(dataset_folder)  # Preprocess dataset images on program run

    try:
        if request.method == "POST" and "image" in request.FILES:
            uploaded_image = request.FILES["image"]
            logger.info(f"Received file: {uploaded_image.name}")
            
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Save to MEDIA_ROOT
            filename = fs.save(uploaded_image.name, uploaded_image)
            file_path = fs.path(filename)
            
            logger.info(f"File saved at: {file_path}")
            image = face_recognition.load_image_file(file_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                encoding = face_encodings[0]
                metadata = load_metadata()
                results = []

                for entry in metadata:
                    stored_encoding = np.array(entry["encoding"])
                    match = face_recognition.compare_faces([stored_encoding], encoding)
                    similarity = face_recognition.face_distance([stored_encoding], encoding)[0]

                    if match[0]:
                        similarity_percentage = (1 - similarity) * 100  # Convert to percentage
                        
                        # Add filename path relative to MEDIA_URL
                        results.append({
    "name": entry["name"],
    "address": entry["address"],
    "gender": entry["gender"],
    "filename": f"{settings.STATIC_URL}images/{entry['filename']}",
    "similarity": round(similarity_percentage, 2)
})
                if results:
                  context["results"] = sorted(results, key=lambda x: x["similarity"], reverse=True)
                else:
                    context["error_message"] = "No matching faces found in the dataset."


            else:
                context["error_message"] = "No faces detected. Please upload a valid image."
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        context["error_message"] = "An unexpected error occurred. Please try again later."

    return render(request, "upload.html", context)

def metadata_display(request):
    metadata_path = os.path.join(settings.BASE_DIR, 'face_recognition_app', 'static', 'metadata.json')
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        metadata = []  # If the file does not exist, return an empty list
    except json.JSONDecodeError:
        metadata = []  # If the file is empty or malformed, return an empty list

    return render(request, 'metadata_display.html', {'metadata': metadata})