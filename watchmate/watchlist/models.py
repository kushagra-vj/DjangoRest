from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField("Movie is in theater or not", default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Review(models.Model):
    rating = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True, blank=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="review")
    active = models.BooleanField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + "--" + self.watchlist.title