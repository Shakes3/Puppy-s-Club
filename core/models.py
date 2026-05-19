from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class SiteSettings(models.Model):
    """Singleton model for global site settings."""
    hero_title = models.CharField(max_length=200, default="A Home Away From Home For Your Dog")
    hero_subtitle = models.CharField(max_length=300, default="Premium boarding, grooming, and daycare for your beloved furry family member.")
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    about_title = models.CharField(max_length=200, default="About PawsInn")
    about_text = models.TextField(default="We are a premium dog hostel dedicated to the comfort and happiness of your furry family members.")
    about_image = models.ImageField(upload_to='site/', blank=True, null=True)
    phone = models.CharField(max_length=30, default="+1 (555) 123-4567")
    email = models.EmailField(default="hello@pawsinn.com")
    address = models.CharField(max_length=300, default="123 Paw Street, Dog Town, CA 90210")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    years_experience = models.PositiveIntegerField(default=10)
    dogs_hosted = models.PositiveIntegerField(default=5000)
    happy_families = models.PositiveIntegerField(default=1200)
    staff_count = models.PositiveIntegerField(default=15)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    ICON_CHOICES = [
        ('🏠', 'House (Boarding)'),
        ('🛁', 'Bath (Grooming)'),
        ('🌞', 'Sun (Daycare)'),
        ('🏃', 'Running (Exercise)'),
        ('🍖', 'Bone (Feeding)'),
        ('💊', 'Pill (Medical)'),
        ('🎾', 'Ball (Play)'),
        ('✂️', 'Scissors (Trimming)'),
    ]
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=10, choices=ICON_CHOICES, default='🏠')
    short_description = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price_from = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_label = models.CharField(max_length=50, default="per night", help_text='e.g. "per night", "per session"')
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, max_length=260)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField(max_length=350, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:post_detail', kwargs={'slug': self.slug})


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    tag = models.CharField(max_length=50, blank=True, help_text='e.g. boarding, grooming, playtime')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.caption or f"Gallery Image {self.pk}"


class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    dog_name = models.CharField(max_length=100, blank=True)
    author_photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} ({self.dog_name})"

    @property
    def stars(self):
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} — {self.created_at.strftime('%d %b %Y')}"
