from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.datetime_safe import date


class Project(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(verbose_name='Start date', blank=True, null=True, default=date.today)
    end_date = models.DateField(verbose_name='End date', blank=True, null=True, default=date.today)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMembership'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.created_at.strftime("%c"), self.name)


class ProjectMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{} {}".format(self.user, self.rate)


class User(AbstractUser):
    current_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
