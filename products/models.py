from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=100)
    abv = models.FloatField(
        blank=True, null=True, 
        help_text="Alcohol By Volume in percentage (e.g., 5.2). Leave blank for non-beverage products."
    )
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products"
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def update_rating(self):
        """Calculate and update the product's average rating based on reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = sum(review.rating for review in reviews) / reviews.count()
        else:
            self.rating = None
        self.save()

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model for user-submitted product reviews."""
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"