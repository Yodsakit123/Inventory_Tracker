from django.db import models

class Part(models.Model):
    STATUS_CHOICES = [
        ("In Stock", "In Stock"),
        ("Low", "Low"),
    ]
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="In Stock")

    def __str__(self):
        return self.name
