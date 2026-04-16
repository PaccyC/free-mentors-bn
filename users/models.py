from django.db import models

# Create your models here.

class User(models.Model):
    
    ROLE_CHOICES= (
        ("USER", "User"),
        ("MENTOR", "Mentor"),
        ("ADMIN", "Admin"),
    )
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    bio=models.TextField()
    address=models.CharField(max_length=255)
    occupation=models.CharField(max_length=100)
    expertise=models.CharField(max_length=100)
    role=models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
    