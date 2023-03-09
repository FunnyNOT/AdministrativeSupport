from django.db import models
from django.contrib.auth.models import User
from portals.models import Portal

# Create your models here.
class Announcement(models.Model):
    title = models.TextField(blank=False, null=False, max_length=100)
    body = models.TextField(blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False)
    visible_to_students = models.BooleanField(blank=False, null=False)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    

    class Meta:
            verbose_name_plural = "Announcements"
            db_table = "announcements"
            