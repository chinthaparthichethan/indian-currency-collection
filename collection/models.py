# collection/models.py
from django.db import models
from django.urls import reverse

class CurrencyItem(models.Model):
    ITEM_TYPES = [
        ('coin', 'Coin'),
        ('note', 'Currency Note'),
    ]
    
    title = models.CharField(max_length=200)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    year = models.IntegerField()
    denomination = models.CharField(max_length=50)
    material = models.CharField(max_length=100, blank=True, null=True)
    issuing_authority = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    
    # Make these fields nullable temporarily
    front_image = models.ImageField(
        upload_to='currency_items/front/', 
        null=True, 
        blank=True, 
        help_text="Front view of the currency item"
    )
    back_image = models.ImageField(
        upload_to='currency_items/back/', 
        null=True, 
        blank=True, 
        help_text="Back view of the currency item"
    )
    
    # Keep the old image field for backward compatibility
    image = models.ImageField(upload_to='currency_items/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'denomination']
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})
    
    @property
    def primary_image(self):
        """Return the primary image to display (front image or legacy image)"""
        return self.front_image if self.front_image else self.image
