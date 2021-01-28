from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
TYPE_CHOICES = (
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna"),
)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Nazwa kategorii")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=256, verbose_name="Nazwa instytucji")
    description = models.TextField(default='', verbose_name="Opis")
    type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="Typ")
    categories = models.ManyToManyField(Category, related_name="institution_categories", verbose_name="Kategorie")

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name="Ilość worków")
    categories = models.ManyToManyField(Category, related_name="donation_categories", verbose_name="Kategorie")
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    related_name="donation_institutions",
                                    verbose_name="Instytucja")
    address = models.CharField(max_length=512, verbose_name="Adres")
    phone_number = models.CharField(max_length=16, verbose_name="Numer telefonu")
    city = models.CharField(max_length=256, verbose_name="Miejscowość")
    zip_code = models.CharField(max_length=10, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(verbose_name="Data odbioru")
    pick_up_time = models.TimeField(verbose_name="Godzina odbioru")
    pick_up_comment = models.TextField(verbose_name="Komentarz dla kuriera")
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, verbose_name="Użytkownik")
    is_taken = models.BooleanField(default=False, verbose_name="Odebrane przez kuriera")

    class Meta:
        verbose_name = "Dar"
        verbose_name_plural = "Dary"

    def __str__(self):
        return '%s %s dla %s' % (self.user.first_name, self.user.last_name, self.institution.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profile'

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)