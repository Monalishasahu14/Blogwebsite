from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Technology'),
        ('LIFE', 'Lifestyle'),
        ('TRAVEL', 'Travel'),
        ('FOOD', 'Food'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', default='default_blog.jpg')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='OTHER')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            count = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{count}'
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
