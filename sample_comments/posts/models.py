from django.conf import settings
from django.db import models

from genericcomments.models import CommentBuilder

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=150)
    
    content = models.TextField(null=False, blank=True)
    
    
class PostComment(CommentBuilder(Post, fieldname="post")):
    pass