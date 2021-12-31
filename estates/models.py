from django.db import models


class ImageList(models.Model):
    src = models.CharField(max_length=500)

    def __str__(self):
        return self.src


class Estate(models.Model):
    url = models.CharField(max_length=350, blank=True, null=True, unique=True)
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
    store = models.BooleanField(blank=True, null=True, default=False)
    elevator = models.BooleanField(blank=True, null=True, default=False)
    image_url = models.CharField(blank=True, null=True, max_length=120)

    balcon = models.BooleanField(blank=True, null=True, default=False)
    floor = models.CharField(max_length=50, blank=True, null=True)
    direction = models.CharField(max_length=20, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    owner = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    equipments = models.CharField(max_length=350, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        if self.owner:
            return self.title + " - " + self.owner
        return self.title

