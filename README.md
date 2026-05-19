# django-comments-app
my implementation of the comments app

Usage:
1.  Add 'genericcomments' application into the installed apps section of 
    settings.py 
2.  Inherit your model from value returned by CommentBuilder helper, like this:
    ```python
    class PostComment(CommentBuilder(Post, fieldname="post")):
        pass
    ```
3.  You could specify desired fieldname, on_delete and other foreign key field
    arguments.

# sql result

for the following models in app `posts`:
```python
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=150)
    
    content = models.TextField(null=False, blank=True)
    
    
class PostComment(CommentBuilder(Post, fieldname="post")):
    pass
```

genericcomments will create the folowing SQL commands:
```sql
BEGIN;
--
-- Create model Post
--
CREATE TABLE "posts_post" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "title" varchar(150) NOT NULL, 
    "content" text NOT NULL, 
    "author_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model PostComment
--
CREATE TABLE "posts_postcomment" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "content" text NOT NULL, 
    "author_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "post_id" bigint NOT NULL REFERENCES "posts_post" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "posts_post_author_id_fe5487bf" ON "posts_post" ("author_id");
CREATE INDEX "posts_postcomment_author_id_8b8e69a3" ON "posts_postcomment" ("author_id");
CREATE INDEX "posts_postcomment_post_id_5b40467f" ON "posts_postcomment" ("post_id");
COMMIT;
```

# how does it works
1.  There is base abstract (in terms of Django) `Post` model class. 
2.  `CommentBuilder` helper function builds from the `Post` class a new class with 
    injected foreign key with specified target model.
3.  Value returned from `CommentBuilder` is used to create a concrete child model,
    with optional ability to extend with additional fields.      