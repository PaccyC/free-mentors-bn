import pymongo
from django.conf import settings
from django.db import models
from users.models import User


def _next_id(collection_name: str) -> int:
    """Assign the next integer id for a MongoDB collection via PyMongo.

    Djongo's AutoField auto-increment is unreliable for new collections —
    it often inserts documents without an integer `id`. We query the max
    existing `id` and increment it ourselves before Django's INSERT runs.
    """
    client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'])
    try:
        db = client[settings.DATABASES['default']['NAME']]
        last = db[collection_name].find_one(
            {'id': {'$exists': True}},
            sort=[('id', pymongo.DESCENDING)],
        )
        return (last['id'] + 1) if last and last.get('id') else 1
    finally:
        client.close()


class MentorshipSession(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("DECLINED", "Declined"),
    )
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions_as_mentee")
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions_as_mentor")
    questions = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.id = _next_id('mentorship_sessions_mentorshipsession')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session: {self.mentee} -> {self.mentor} ({self.status})"


class Review(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    score = models.IntegerField()
    comment = models.TextField()
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.id = _next_id('mentorship_sessions_review')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review: {self.mentee} -> {self.mentor} ({self.score}/5)"
