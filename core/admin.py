from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    SiteSettings, Service, Post, GalleryImage,
    Testimonial, ContactMessage, ServiceCategory
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image'),
        }),
        ('About Section', {
            'fields': ('about_title', 'about_text', 'about_image'),
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address'),
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
        }),
        ('Stats', {
            'fields': ('years_experience', 'dogs_hosted', 'happy_families', 'staff_count'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'price_from', 'price_label', 'featured', 'active', 'order')
    list_editable = ('featured', 'active', 'order')
    list_filter = ('featured', 'active')
    search_fields = ('name', 'short_description')
    fieldsets = (
        (None, {
            'fields': ('name', 'icon', 'short_description', 'description'),
        }),
        ('Pricing', {
            'fields': ('price_from', 'price_label'),
        }),
        ('Display', {
            'fields': ('featured', 'active', 'order'),
        }),
    )


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)
    list_display = ('title', 'author', 'status', 'featured', 'created_at', 'published_at')
    list_filter = ('status', 'featured', 'created_at')
    list_editable = ('status', 'featured')
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status', 'featured'),
        }),
        ('Content', {
            'fields': ('cover_image', 'excerpt', 'body'),
        }),
        ('Dates', {
            'fields': ('published_at',),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tag', 'order', 'active', 'created_at')
    list_editable = ('order', 'active', 'tag')
    list_filter = ('active', 'tag')
    search_fields = ('caption', 'tag')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'dog_name', 'rating', 'approved', 'created_at')
    list_editable = ('approved',)
    list_filter = ('approved', 'rating')
    search_fields = ('author_name', 'dog_name', 'body')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'read', 'replied', 'created_at')
    list_editable = ('read', 'replied')
    list_filter = ('read', 'replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    fieldsets = (
        ('Sender Info', {
            'fields': ('name', 'email', 'phone', 'created_at'),
        }),
        ('Message', {
            'fields': ('subject', 'message'),
        }),
        ('Status', {
            'fields': ('read', 'replied'),
        }),
    )
