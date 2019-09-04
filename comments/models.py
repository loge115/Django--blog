from django.db import models
from user.models import Post

# Create your models here.
class Comment(models.Model):
    class Meta:
        db_table='comment'
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]