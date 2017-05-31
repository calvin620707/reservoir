from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ManyToManyField, DateTimeField, CharField, ForeignKey, SET_NULL


class Project(Model):
    name = CharField(max_length=50, db_index=True)
    members = ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = DateTimeField(auto_now_add=True)


class User(AbstractUser):
    current_project = ForeignKey(Project, on_delete=SET_NULL, null=True)
