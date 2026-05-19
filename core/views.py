from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Service, Post, GalleryImage, Testimonial, SiteSettings
from .forms import ContactForm


def home(request):
    settings = SiteSettings.get_settings()
    featured_services = Service.objects.filter(featured=True, active=True)[:6]
    latest_posts = Post.objects.filter(status=Post.STATUS_PUBLISHED)[:3]
    testimonials = Testimonial.objects.filter(approved=True)[:6]
    gallery_preview = GalleryImage.objects.filter(active=True)[:8]
    return render(request, 'home.html', {
        'settings': settings,
        'featured_services': featured_services,
        'latest_posts': latest_posts,
        'testimonials': testimonials,
        'gallery_preview': gallery_preview,
        'page': 'home',
    })


def services(request):
    settings = SiteSettings.get_settings()
    all_services = Service.objects.filter(active=True)
    return render(request, 'services.html', {
        'settings': settings,
        'services': all_services,
        'page': 'services',
    })


def blog_list(request):
    settings = SiteSettings.get_settings()
    post_list = Post.objects.filter(status=Post.STATUS_PUBLISHED)
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/list.html', {
        'settings': settings,
        'posts': posts,
        'page': 'blog',
    })


def post_detail(request, slug):
    settings = SiteSettings.get_settings()
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    recent_posts = Post.objects.filter(
        status=Post.STATUS_PUBLISHED
    ).exclude(pk=post.pk)[:3]
    return render(request, 'blog/detail.html', {
        'settings': settings,
        'post': post,
        'recent_posts': recent_posts,
        'page': 'blog',
    })


def gallery(request):
    settings = SiteSettings.get_settings()
    tag_filter = request.GET.get('tag', '')
    images = GalleryImage.objects.filter(active=True)
    if tag_filter:
        images = images.filter(tag=tag_filter)
    tags = GalleryImage.objects.filter(active=True).values_list('tag', flat=True).distinct().exclude(tag='')
    return render(request, 'gallery.html', {
        'settings': settings,
        'images': images,
        'tags': tags,
        'active_tag': tag_filter,
        'page': 'gallery',
    })


def about(request):
    settings = SiteSettings.get_settings()
    testimonials = Testimonial.objects.filter(approved=True)[:8]
    return render(request, 'about.html', {
        'settings': settings,
        'testimonials': testimonials,
        'page': 'about',
    })


def contact(request):
    settings = SiteSettings.get_settings()
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            from .models import ContactMessage
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                subject=form.cleaned_data.get('subject', ''),
                message=form.cleaned_data['message'],
            )
            messages.success(request, "Thank you! Your message has been sent. We'll be in touch soon. 🐾")
            return redirect('core:contact')
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'contact.html', {
        'settings': settings,
        'form': form,
        'page': 'contact',
    })
