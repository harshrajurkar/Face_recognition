
# Face Recognition Project

## Project Description
This is a face recognition project built using Python and Django. The system allows users to upload an image and checks for matching faces in the pre-existing dataset. The following outcomes are possible:
1. If the uploaded image matches one or more persons in the dataset, it displays the matching results along with their details (e.g., name, address, gender, similarity percentage, and image).
2. If the uploaded image does not match anyone in the dataset, it shows "No matching found."

---

## Features
- Face recognition using a pre-trained dataset.
- Displays results with similarity percentages for matches.
- User-friendly interface to upload images.
- Clear indication if no matches are found in the database.

---

## How to Use

### 1. Clone the Repository
Pull the project from the repository using the following command:
```bash
git clone <repository-link>
cd <repository-folder>
```

### 2. Set Up Virtual Environment
Create a virtual environment using Python 3.10.12:
```bash
python3 -m venv venv
```

Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install the required dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
Apply the necessary migrations for Django:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Project
Start the Django development server:
```bash
python manage.py runserver
```

Navigate to the following URL to use the application:  
[http://127.0.0.1:8000/face_recognition/upload/](http://127.0.0.1:8000/face_recognition/upload/)

---

## Additional Notes
- Ensure that the `requirements.txt` file is up-to-date and contains all necessary dependencies for the project.
- The dataset for face recognition should be preloaded and structured correctly for the application to work as expected.
- For any issues, ensure the virtual environment is activated and all dependencies are installed.
