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
from .models import Person


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

            # Store the file path in the session for later use
            request.session["uploaded_image_path"] = file_path

            try:
                image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    encoding = face_encodings[0]
                    context["message"] = "Image uploaded successfully! Faces detected."
                    context["uploaded_image"] = True
                    context["face_encoding"] = encoding.tolist()  # Convert numpy array to list for JSON compatibility
                    logger.info(f"Face encoding: {encoding}")

                else:
                    context["error_message"] = "No faces detected. Please upload a different image."
            except Exception as e:
                context["error_message"] = f"An error occurred: {str(e)}"
                logger.error(f"Error processing the image: {str(e)}")
        elif "search_button" in request.POST:
            # When the search button is clicked, check if image path exists in the session
            file_path = request.session.get("uploaded_image_path", None)
            if file_path:
                try:
                    # Proceed with face matching
                    image = face_recognition.load_image_file(file_path)
                    face_encodings = face_recognition.face_encodings(image)

                    if face_encodings:
                        encoding = face_encodings[0]
                        context["message"] = "Image uploaded successfully! Faces detected."
                        context["uploaded_image"] = True
                        context["face_encoding"] = encoding.tolist()

                        time.sleep(2)  # Simulate a delay for comparison
                        logger.info("Starting face matching process...")

                        # Retrieve all persons from the database
                        persons = Person.objects.all()
                        results = []

                        for person in persons:
                            stored_encoding = json.loads(person.face_encoding)
                            match = face_recognition.compare_faces([stored_encoding], encoding)
                            similarity = face_recognition.face_distance([stored_encoding], encoding)[0]

                            if match[0]:
                                similarity_percentage = (1 - similarity) * 100  # Convert to percentage
                                if similarity_percentage > 70:  # Only include matches above 70%
                                    results.append({
                                        "name": person.name,
                                        "similarity": round(similarity_percentage, 2),
                                        "image_url": person.image.url
                                    })

                        context["results"] = results
                        logger.info(f"Matching results: {context['results']}")
                    else:
                        context["error_message"] = "No faces detected in the uploaded image."
                except Exception as e:
                    context["error_message"] = f"An error occurred: {str(e)}"
                    logger.error(f"Error processing the image: {str(e)}")
            else:
                context["error_message"] = "No image uploaded. Please upload an image first."

    return render(request, "upload.html", context)

# def simulate_matching(encodings):
#     """
#     Simulates the face matching process.
#     Replace this function with actual logic for matching with local images.
#     """
#     logger.info("Simulating face matching...")
#     # Example result structure
#     simulated_results = [
#         {"name": "Person A", "image_url": "/media/person_a.jpg", "similarity": 95},
#         {"name": "Person B", "image_url": "/media/person_b.jpg", "similarity": 90},
#     ]
#     return simulated_results
