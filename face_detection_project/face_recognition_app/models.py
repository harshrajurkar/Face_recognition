from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)  # Name of the person
    address = models.TextField()  # Address of the person
    gender = models.CharField(max_length=10)  # Gender (Male/Female/Other)
    image = models.ImageField(upload_to="faces/")  # Path to uploaded image
    face_encoding = models.BinaryField(blank=True, null=True)  # For face encoding data

    def __str__(self):
        return self.name
