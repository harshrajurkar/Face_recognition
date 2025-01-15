import face_recognition
import json
import os
from django.conf import settings

def get_metadata_path():
    return os.path.join(settings.BASE_DIR, 'face_recognition_app/static/metadata.json')

def load_metadata():
    metadata_path = get_metadata_path()
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Return an empty list if JSON is malformed
    return []

def save_metadata(metadata):
    metadata_path = get_metadata_path()
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def parse_metadata_from_filename(filename):
    """
    Parses metadata from a filename formatted as 'name_address_gender.ext'.
    Example: 'JohnDoe_123MainStreet_Male.jpg'
    """
    name, address, gender = "Unknown", "Unknown", "Unknown"
    parts = os.path.splitext(filename)[0].split("_")
    
    if len(parts) >= 3:
        name = parts[0]  # First part is the name
        address = parts[1]  # Second part is the address
        gender = parts[2]  # Third part is the gender

    return name, address, gender

def store_dataset_encodings(dataset_folder):
    """
    Reads all images in `dataset_folder`, processes face encodings,
    and updates the metadata file in static/metadata.json.
    """
    metadata = load_metadata()
    existing_files = {entry["filename"] for entry in metadata}

    for file in os.listdir(dataset_folder):
        if file.endswith(('.jpg', '.jpeg', '.png')) and file not in existing_files:
            image_path = os.path.join(dataset_folder, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                encoding = encodings[0]
                name, address, gender = parse_metadata_from_filename(file)
                metadata.append({
                    "filename": file,
                    "name": name,
                    "address": address,
                    "gender": gender,
                    "encoding": encoding.tolist()
                })

    # Save updated metadata
    save_metadata(metadata)
