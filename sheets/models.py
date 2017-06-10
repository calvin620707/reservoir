from django.db import models
from django.urls import reverse
from django.utils import timezone


class CostRecord(models.Model):
    project = models.ForeignKey('accounts.Project', on_delete=models.CASCADE, db_index=True)
    payer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_index=True)
    calculated = models.BooleanField(default=False, db_index=True)
    name = models.CharField(max_length=30)
    cost = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)

    FOOD = 'FO'
    CLOTHING = 'CL'
    HOUSING = 'HO'
    TRANSPORTATION = 'TR'
    EDUCATION = 'ED'
    ENTERTAINMENT = 'EN'
    OTHERS = 'OT'
    CATEGORY_CHOICES = (
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (HOUSING, 'Housing'),
        (TRANSPORTATION, 'Transportation'),
        (EDUCATION, 'Education'),
        (ENTERTAINMENT, 'Entertainment'),
        (OTHERS, 'Others')
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=OTHERS, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['project', 'payer']),
            models.Index(fields=['project', 'payer', 'calculated']),
        ]

    def get_absolute_url(self):
        return reverse('sheets:cost-details', kwargs={'pk': self.pk})
