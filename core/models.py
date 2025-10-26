from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    location = models.CharField(max_length=100, verbose_name=_("Ville/Pays"), blank=True)
    content = models.TextField(verbose_name=_("Commentaire"))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Note (1-5 étoiles)"),
        default=5
    )
    vehicle_rented = models.CharField(max_length=100, verbose_name=_("Véhicule loué"), blank=True)
    active = models.BooleanField(default=False, verbose_name=_("Publié"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Dernière modification"))

    class Meta:
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}⭐ ({'Publié' if self.active else 'En attente'})"

    def get_stars_display(self):
        """Return stars for display"""
        return "⭐" * self.rating + "☆" * (5 - self.rating)
