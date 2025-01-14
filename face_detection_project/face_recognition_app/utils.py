import face_recognition
import json
import os
from django.conf import settings

def store_face_encoding(image_path, filename, name, address, gender):
    # Load image
    image = face_recognition.load_image_file(image_path)
    # Extract face encoding
    encodings = face_recognition.face_encodings(image)
    
    if encodings:
        encoding = encodings[0]
        
        # Prepare metadata
        new_data = {
            "filename": filename,
            "name": name,
            "address": address,
            "gender": gender,
            "encoding": encoding.tolist()  # Convert numpy array to list for JSON
        }
        
        # Read existing metadata
        metadata_path = os.path.join(settings.BASE_DIR, 'face_recognition_app/static/metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = []
        
        # Append new data
        metadata.append(new_data)
        
        # Save metadata back to the file
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

    else:
        print("No face found in the image.")
