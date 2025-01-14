from django.db import models
import json

class Person(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='persons/')
    face_encoding = models.TextField()  # Store the encoding as a string (JSON)
    address = models.CharField(max_length=255, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.face_encoding and not isinstance(self.face_encoding, list):
            raise ValueError("face_encoding must be a list.")
        self.face_encoding = json.dumps(self.face_encoding)
        super().save(*args, **kwargs)

