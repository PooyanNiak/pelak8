from django.db import models


class ImageList(models.Model):
    src = models.CharField(max_length=500)

    def __str__(self):
        return self.src


class Estate(models.Model):
    # Todo : change EstateType to TextChoices
    # class EstateType(models.TextChoices):
    #     APA = "Apartement"
    #     HOU = "House"
    #     COM = "Commercial"
    #     VIL = "Villa"

    title = models.CharField(max_length=120)
    price = models.PositiveIntegerField(blank=True, null=True)
    region = models.CharField(max_length=320, blank=True, null=True)
    area = models.PositiveIntegerField(blank=True, null=True)
    estate_type = models.CharField(max_length=50, null=True)
    use_type = models.CharField(max_length=50, null=True)
    ppm = models.PositiveIntegerField(blank=True, null=True)
    rooms = models.PositiveIntegerField(blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    parking = models.BooleanField(blank=True, null=True)
    store = models.BooleanField(blank=True, null=True)
    elevator = models.BooleanField(blank=True, null=True)
    image_url = models.CharField(blank=True, null=True, max_length=120)

    def __str__(self):
        return self.title

