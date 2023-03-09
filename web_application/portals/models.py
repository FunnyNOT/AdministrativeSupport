from django.db import models

# Create your models here.
class Portal(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    users = models.IntegerField(blank=False, null=False, default=0)
    is_active = models.BooleanField(blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False)

    class Meta:
            verbose_name_plural = "Portals"
            db_table = "portals"
            indexes = [models.Index(fields=['name', 'is_active', ]),]