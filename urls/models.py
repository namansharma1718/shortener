from django.db import models

# Create your models here.

class URL(models.Model):
    original_url = models.URLField(unique=True)
    short_code = models.CharField(max_length=10, unique=True)
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_code