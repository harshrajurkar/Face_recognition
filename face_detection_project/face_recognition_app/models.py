from django.db import models
import json

class Person(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='persons/')
    face_encoding = models.TextField()  # Store the encoding as a string (JSON)

    def save(self, *args, **kwargs):
        # Automatically encode the face encoding as a JSON string before saving
        if isinstance(self.face_encoding, list):
            self.face_encoding = json.dumps(self.face_encoding)
        super().save(*args, **kwargs)
