from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=30)
    languages = models.ManyToManyField(Language, blank=True)

    def __str__(self):
        return self.name
