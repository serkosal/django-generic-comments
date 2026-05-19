from django.conf import settings
from django.db import models


# Create your models here.
class Comment(models.Model):
    """Contain logic for all kind of Comments.

    Usage:
    1.  Add `genericcomments` application into the installed apps section of 
        settings.py 
    2.  Inherit your model from value returned by CommentBuilder helper
    3.  You could specify desired `fieldname`, `on_delete` and other foreign
        key field arguments. 

    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    content = models.TextField(null=False, blank=True)

    class Meta:
        abstract = True


def CommentBuilder(
    target: models.Model, fieldname: str = "target", on_delete=models.PROTECT,
    **kwargs
):
    newClass = Comment
    newClass.add_to_class(fieldname, models.ForeignKey(target, on_delete=on_delete, **kwargs))

    return newClass
