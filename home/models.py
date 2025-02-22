from django.db import models


class NewsletterSubscriber(models.Model):
    """Model for newsletter subscribers and their interests."""

    INTEREST_CHOICES = [
        ("beer", "I'm a Beer Guy"),
        ("food", "I'm a Foodie"),
        ("merch", "Give Me Your Merch"),
    ]

    email = models.EmailField(unique=True)
    interests = models.CharField(
        max_length=255, blank=True
    )  # Store as "beer,food,merch"
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def interest_list(self):
        """Return a list of selected interests or 'General' if empty."""
        return self.interests.split(",") if self.interests else ["General"]

    def __str__(self):
        return (
            f"{self.email} - Interests: {self.interests or 'General'}"
        )
