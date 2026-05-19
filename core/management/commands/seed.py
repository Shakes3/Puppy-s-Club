from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SiteSettings, Service, Testimonial


class Command(BaseCommand):
    help = 'Seeds the database with demo data for PawsInn'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding PawsInn demo data...')

        # Site Settings
        s, _ = SiteSettings.objects.get_or_create(pk=1)
        s.hero_title = "A Home Away From Home For Your Dog"
        s.hero_subtitle = "Premium boarding, grooming, and daycare for your beloved furry family member."
        s.about_title = "About PawsInn"
        s.about_text = (
            "Founded in 2014, PawsInn was born out of a love for dogs and a desire to provide "
            "a genuinely caring environment when owners need to be away. Our team of certified "
            "pet care specialists treats every dog as their own, with personalised attention, "
            "safe play spaces, and lots of love."
        )
        s.phone = "+1 (555) 123-4567"
        s.email = "hello@pawsinn.com"
        s.address = "123 Paw Street, Dog Town, CA 90210"
        s.years_experience = 10
        s.dogs_hosted = 5000
        s.happy_families = 1200
        s.staff_count = 15
        s.save()
        self.stdout.write('  [OK] Site settings saved')

        # Services
        services_data = [
            ('\U0001f3e0', 'Dog Boarding', 'Cozy, climate-controlled suites for overnight stays.', 25.00, 'per night'),
            ('\U0001f6c1', 'Grooming', 'Full grooming service including bath, trim and nail clipping.', 40.00, 'per session'),
            ('\U0001f31e', 'Dog Daycare', 'Supervised play and socialisation during the day.', 18.00, 'per day'),
            ('\U0001f3c3', 'Dog Walking', 'Group or solo walks with our trained handlers.', 15.00, 'per walk'),
            ('\U0001f3be', 'Puppy Playgroups', 'Structured play sessions for puppies under 12 months.', 12.00, 'per session'),
            ('\U0001f48a', 'Medical Boarding', 'Specialised care for dogs needing medication or post-op rest.', 45.00, 'per night'),
        ]
        for icon, name, desc, price, label in services_data:
            obj, _ = Service.objects.get_or_create(name=name)
            obj.icon = icon
            obj.short_description = desc
            obj.price_from = price
            obj.price_label = label
            obj.featured = True
            obj.active = True
            obj.save()
        self.stdout.write(f'  [OK] {len(services_data)} services created')

        # Testimonials
        testimonials_data = [
            ('Sarah M.', 'Buddy', 5, 'PawsInn is absolutely wonderful! Buddy was so happy and well cared for. The daily photos really put my mind at ease.'),
            ('James T.', 'Luna', 5, 'We were nervous leaving Luna for the first time, but the team were so reassuring. She came home tail wagging!'),
            ('Priya K.', 'Mango', 5, 'The grooming service is top-notch. Mango always comes back looking like a superstar!'),
            ('Carlos R.', 'Rex', 4, 'Great facilities and caring staff. Rex absolutely loves the daycare sessions.'),
            ('Emma W.', 'Daisy', 5, 'I travel frequently for work and PawsInn has been a lifesaver. Daisy is always in the best hands.'),
            ('Tom H.', 'Bruno', 5, 'Fantastic service from start to finish. Highly recommend to any dog owner!'),
        ]
        for name, dog, rating, body in testimonials_data:
            obj, _ = Testimonial.objects.get_or_create(author_name=name, dog_name=dog)
            obj.rating = rating
            obj.body = body
            obj.approved = True
            obj.save()
        self.stdout.write(f'  [OK] {len(testimonials_data)} testimonials created')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@pawsinn.com', 'admin123')
            self.stdout.write('  [OK] Superuser: admin / admin123')
        else:
            self.stdout.write('  [INFO] Admin user already exists')

        self.stdout.write(self.style.SUCCESS('\nDone! Visit http://127.0.0.1:8000/'))
        self.stdout.write(self.style.SUCCESS('Admin: http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.WARNING('IMPORTANT: Change admin password in production!'))
