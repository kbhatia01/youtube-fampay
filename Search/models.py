from django.db import models


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField()
    publishedAt = models.DateTimeField(blank=False, null=False, db_index=True)
    channelTitle = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"
