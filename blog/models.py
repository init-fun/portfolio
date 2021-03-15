from django.db import models
from django.forms import widgets
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
import secrets, string


# taggin
from taggit.managers import TaggableManager

# our customer model manager, which will return all published post
# Post.published.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    post_img = models.ImageField(upload_to="post_images/")
    # taggins

    tags = TaggableManager()

    class Meta:
        ordering = ("-publish",)  # a tuple

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


def anon_username():
    random_string = string.ascii_letters + string.digits
    username = "".join(secrets.choice(random_string) for i in range(10))
    return username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    name = models.CharField(max_length=10, default=anon_username)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class WorkExp(models.Model):
    work_img = models.ImageField(upload_to="work_images/")
    from_year = models.DateField()
    to_year = models.DateField()
    position_held = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    summary = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Was {self.position_held} at {self.organization} from {self.from_year} to {self.to_year}"


class ProjectModel(models.Model):
    project_img = models.ImageField(upload_to="project_images/")
    name = models.CharField(max_length=100)
    summary = models.TextField()
    tech_used = models.TextField()
    project_url = models.URLField()
    github_link = models.URLField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"