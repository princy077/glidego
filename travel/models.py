from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=[
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('historical', 'Historical'),
        ('city', 'City'),
        ('adventure', 'Adventure')
    ])
    latitude = models.FloatField(default=0.000)
    longitude = models.FloatField(default=0.000)
    map_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=100, choices=[
        ('boating', 'Boating'),
        ('kayaking', 'Kayaking'),
        ('trekking', 'Trekking'),
        ('sightseeing', 'Sightseeing'),
        ('camping', 'Camping'),
        ('adventure', 'Adventure'),
        ('hiking', 'Hiking'),
        ('diving', 'Diving')
    ])
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="activities")
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} at {self.destination.name}"

class ActivityBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], default='pending')

    def save(self, *args, **kwargs):
        # Calculate total price based on number of people
        self.total_price = self.number_of_people * self.activity.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.activity.name} on {self.date}"
    


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_categories = models.JSONField(default=list)  # Stores list of categories
    preferred_activities = models.JSONField(default=list)  # Stores list of activities

    def __str__(self):
        return f"Preferences of {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reviews")
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.destination.name}"


