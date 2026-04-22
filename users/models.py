from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ("USER", "User"),
        ("MENTOR", "Mentor"),
        ("ADMIN", "Admin"),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    bio = models.TextField(blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    occupation = models.CharField(max_length=100, blank=True, default='')
    expertise = models.CharField(max_length=100, blank=True, default='')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
