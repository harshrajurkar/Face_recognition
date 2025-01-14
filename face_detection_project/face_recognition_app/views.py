import face_recognition
import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import time  
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def metadata_display(request):
    metadata_path = os.path.join(settings.BASE_DIR, 'face_recognition_app', 'static', 'metadata.json')
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
        return render(request, 'display_metadata.html', {'metadata': metadata})
    except FileNotFoundError:
        logger.error("Metadata file not found.")
        return HttpResponse("Metadata file not found.", status=404)

logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

def upload_page(request):
    context = {}
    if request.method == "POST":
        if "image" in request.FILES:
            uploaded_image = request.FILES["image"]
            logger.info(f"Received file: {uploaded_image.name}")
            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)
            file_path = fs.path(filename)
            logger.info(f"File saved at: {file_path}")

            try:
                image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    encoding = face_encodings[0]
                    context["message"] = "Image uploaded successfully! Faces detected."
                    context["uploaded_image"] = True
                    context["face_encoding"] = encoding.tolist()  # Convert numpy array to list for JSON compatibility
                    logger.info(f"Face encoding: {encoding}")

                    if "search_button" in request.POST:
                        time.sleep(2)  # Simulate a delay for comparison
                        logger.info("Starting face matching process...")
                        # Simulated results
                        context["results"] = [
                            {"name": "Person A", "similarity": 95},
                            {"name": "Person B", "similarity": 90},
                        ]
                        logger.info(f"Matching results: {context['results']}")
                else:
                    context["error_message"] = "No faces detected. Please upload a different image."
            except Exception as e:
                context["error_message"] = f"An error occurred: {str(e)}"
                logger.error(f"Error processing the image: {str(e)}")
        else:
            context["error_message"] = "No file uploaded. Please select an image and try again."

    return render(request, "upload.html", context)
def simulate_matching(encodings):
    """
    Simulates the face matching process.
    Replace this function with actual logic for matching with local images.
    """
    logger.info("Simulating face matching...")
    # Example result structure
    simulated_results = [
        {"name": "Person A", "image_url": "/media/person_a.jpg", "similarity": 95},
        {"name": "Person B", "image_url": "/media/person_b.jpg", "similarity": 90},
    ]
    return simulated_results
