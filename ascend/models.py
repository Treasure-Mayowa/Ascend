from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    school = models.TextField(blank=True)

class YoutubeContent(models.Model):
    CATEGORY_CHOICES = [
        ("Classroom Management", "Classroom Management"),
        ("Technology Integration", "Technology Integration"),
        ("Assessment and Feedback", "Assessment and Feedback"),
        ("Parents Engagement", "Parents Engagement"),
        ("Students Engagement", "Students Engagement"),
        ("Inclusion", "Inclusion"),
        ("Real-world skills", "Real-world skills"),
        ("General Tips", "General Tips")
    ]

    title = models.TextField()  
    embed_code = models.TextField()
    source = models.TextField()
    category = models.TextField(choices=CATEGORY_CHOICES, null=True)
    takeaways = models.TextField(default="")

class Resources(models.Model):
    image_url = models.URLField()
    name = models.TextField()
    description = models.TextField()
    url = models.URLField()
    
class Courses(models.Model):
    image_url = models.URLField()
    source = models.TextField()
    name = models.TextField()
    description = models.TextField()
    url = models.URLField()
    topic = models.TextField(null=True)

    def __str__(self):
        return f"{self.name} from {self.source}"        