from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ManyToManyField, DateTimeField, CharField, ForeignKey, SET_NULL, TextField, \
    DateField
from django.utils.datetime_safe import date


class Project(Model):
    name = CharField(max_length=50, db_index=True)
    description = TextField(blank=True, null=True)
    start_date = DateField(verbose_name='Start date', blank=True, null=True, default=date.today)
    end_date = DateField(verbose_name='End date', blank=True, null=True, default=date.today)
    members = ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.created_at.strftime("%c"), self.name)


class User(AbstractUser):
    current_project = ForeignKey(Project, on_delete=SET_NULL, null=True)
