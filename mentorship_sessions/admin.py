from django.contrib import admin
from .models import MentorshipSession, Review

# Register your models here.

@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass