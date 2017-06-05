from django.db import models
from django.utils import timezone


class CostRecord(models.Model):
    project = models.ForeignKey('accounts.Project', on_delete=models.CASCADE, db_index=True)
    payer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_index=True)
    calculated = models.BooleanField(default=False, db_index=True)
    name = models.CharField(max_length=30)
    cost = models.FloatField(blank=False, null=False)
    datetime = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'payer']),
            models.Index(fields=['project', 'payer', 'calculated']),
        ]
