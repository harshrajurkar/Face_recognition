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

def upload_page(request):
    context = {}
    try:
        if request.method == "POST":
            # Handle image upload
            if "image" in request.FILES:
                uploaded_image = request.FILES["image"]
                logger.info(f"Received file: {uploaded_image.name}")
                fs = FileSystemStorage()
                filename = fs.save(uploaded_image.name, uploaded_image)
                file_path = fs.path(filename)
                logger.info(f"File saved at: {file_path}")

                # Load and process the uploaded image
                image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    encoding = face_encodings[0]
                    context["message"] = "Image uploaded successfully! Faces detected."
                    context["uploaded_image"] = True
                    context["face_encoding"] = encoding.tolist()  # Convert to list for JSON compatibility

                    # Log face encoding
                    logger.info(f"Face encoding: {encoding}")

                    # Prepare metadata
                    metadata_path = os.path.join(settings.BASE_DIR, 'face_recognition_app', 'static', 'metadata.json')

                    # Load existing data and append the new entry
                    try:
                        with open(metadata_path, 'r+') as f:
                            try:
                                data = json.load(f)
                            except json.JSONDecodeError:
                                data = []  # Handle case where the file is empty or malformed

                            # Create a new entry
                            new_entry = {
                                "filename": uploaded_image.name,
                                "name": "John Doe",  # Replace with actual details if available
                                "address": "123 Example Street",
                                "gender": "Male",
                                "encoding": encoding.tolist()
                            }

                            # Log data being written to metadata
                            logger.info(f"Data being written to metadata: {new_entry}")

                            # Append the new entry
                            data.append(new_entry)

                            # Write updated data back to the file
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            logger.info(f"Updated metadata: {data}")

                    except Exception as e:
                        logger.error(f"Error writing to metadata file: {e}")
                        context["error_message"] = "An error occurred while saving face encoding."
                else:
                    context["error_message"] = "No faces detected. Please upload a different image."

            # Handle face matching
            elif "search_button" in request.POST:
                # Check if the image path exists in the session
                file_path = request.session.get("uploaded_image_path", None)
                if file_path:
                    try:
                        # Load and process the uploaded image
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
                                if person.face_encoding is None:
                                    logger.warning(f"Person {person.id} has no face encoding. Skipping.")
                                    continue

                                try:
                                    stored_encoding = json.loads(person.face_encoding)
                                    match = face_recognition.compare_faces([stored_encoding], encoding)
                                    similarity = face_recognition.face_distance([stored_encoding], encoding)[0]

                                    if match[0]:
                                        similarity_percentage = (1 - similarity) * 100  # Convert to percentage
                                        if similarity_percentage > (settings.FACE_SIMILARITY_THRESHOLD * 100):
                                            results.append({
                                                "name": person.name,
                                                "similarity": round(similarity_percentage, 2),
                                                "image_url": person.image.url
                                            })
                                except json.JSONDecodeError as e:
                                    logger.error(f"Error decoding face encoding for person {person.id}: {str(e)}")

                            context["results"] = results
                            logger.info(f"Matching results: {context['results']}")
                        else:
                            context["error_message"] = "No faces detected in the uploaded image."
                    except Exception as e:
                        logger.error(f"Error processing the image: {str(e)}", exc_info=True)
                        context["error_message"] = "An internal error occurred. Please try again later."
                else:
                    context["error_message"] = "No image uploaded. Please upload an image first."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
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