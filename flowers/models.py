from django.db import models
from django.utils import timezone
# Create your models here.

class Species(models.Model):
    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    usda_symbol = models.CharField(max_length=20)
    created_date = models.DateTimeField(
            default=timezone.now)

# Information Models
class States(models.Model):
    name = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=2)
class Counties(models.Model):
    name = models.CharField(max_length=80)
    state_id = models.ForeignKey(States, on_delete=models.CASCADE)
class SpeciesCounty(models.Model):
    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
    county_id = models.ForeignKey(Counties, on_delete=models.CASCADE)



# Features Models
class Colors(models.Model):
    color = models.CharField(max_length=40)
class SpeciesColor(models.Model):
    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
    color_id = models.ForeignKey(Colors, on_delete=models.CASCADE)

class Shapes(models.Model):
    shape = models.CharField(max_length=40)
class SpeciesShape(models.Model):
    species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
    shape_id = models.ForeignKey(Shapes, on_delete=models.CASCADE)