from django.db import models


class Tweet(models.Model):
    twt_id = models.BigIntegerField()
    username = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    created_at = models.TextField()
    text = models.TextField()
    retweet_count = models.IntegerField(null=True)
    favorite_count = models.IntegerField(null=True)
    popular = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.username
