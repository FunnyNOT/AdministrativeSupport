from django.db import models
from django.contrib.auth.models import User, Group

from portals.models import Portal


class Member(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    is_registered = models.BooleanField(blank=False, null=False, default=0)
    created_at = models.DateTimeField(blank=False, null=False)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, blank=False, null=False, default=1)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, null=False, default=1)


    class Meta:
            verbose_name_plural = "Members"
            db_table = "members"
            indexes = [models.Index(fields=['auth_user', 
                                            'is_registered', 'created_at', 'portal', 'group' ]),]

class AllowMemberRegistration(models.Model):

    username = models.EmailField(max_length=254)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, null=False, default=3)
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, blank=False, null=False, default=1)
    is_registered = models.BooleanField(blank=False, null=False)
    created_date = models.DateTimeField(blank=False, null=False)
    last_updated_date = models.DateTimeField(blank=True, null=True)
    invitation_counter = models.IntegerField(blank=False, null=False)

    class Meta:
            verbose_name_plural = "Members Registration"
            db_table = "allow_member_registration"
            indexes = [models.Index(fields=['username', 'group_id', 'is_registered', ]),]

class AnalyticsMembers(models.Model):

    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=False, null=False)
    event_type = models.CharField(max_length=100, blank=False, null=False)
    auth_user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    portal = models.ForeignKey(Portal, blank=False, null=False, on_delete=models.CASCADE)
    session_hash_number = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Analytics Members"
        db_table = "analytics_members"
        indexes = [models.Index(fields=['timestamp', 'event_type', 'auth_user', ]),
                   models.Index(fields=['session_hash_number', 'event_type', 'auth_user', ]), ]