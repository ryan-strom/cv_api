from django.db import models
from django.utils import timezone
import json
# Create your models here.


# Information Models
class State(models.Model):
    name = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class County(models.Model):
    county = models.CharField(max_length=80)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.county

    def __str__(self):
        return self.county
# class SpeciesCounty(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     county_id = models.ForeignKey(Counties, on_delete=models.CASCADE)


# Features Models
class Color(models.Model):
    color = models.CharField(max_length=40)

    def __str__(self):
        return self.color
# class SpeciesFlowerColor(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     color_id = models.ForeignKey(Colors, on_delete=models.CASCADE)
# class SpeciesFoilageColor(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     color_id = models.ForeignKey(Colors, on_delete=models.CASCADE)

class Shape(models.Model):
    shape = models.CharField(max_length=40)

    def __str__(self):
        return self.shape
# class SpeciesShape(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     shape_id = models.ForeignKey(Shapes, on_delete=models.CASCADE)

# Descriptive Models
class Category(models.Model):
    category = models.CharField(max_length=40)

    def __str__(self):
        return self.category
# class SpeciesCategory(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

class ActiveGrowthPeriod(models.Model):
    active_growth_period = models.CharField(max_length=40)

    def __str__(self):
        return self.active_growth_period


class Duration(models.Model):
    duration = models.CharField(max_length=40)

    def __str__(self):
        return self.duration
# class SpeciesDuration(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     duration_id = models.ForeignKey(Durations, on_delete=models.CASCADE)

class GrowthHabit(models.Model):
    growth_habit = models.CharField(max_length=80)

    def __str__(self):
        return self.growth_habit
# class SpeciesGrowthHabit(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     growth_habit_id = models.ForeignKey(GrowthHabits, on_delete=models.CASCADE)

class GrowthForm(models.Model):
    growth_form = models.CharField(max_length=80)

    def __str__(self):
        return self.growth_form
# class SpeciesGrowthForm(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     growth_form_id = models.ForeignKey(GrowthForms, on_delete=models.CASCADE)

class GrowthRate(models.Model):
    growth_rate = models.CharField(max_length=80)

    def __str__(self):
        return self.growth_rate
# class SpeciesGrowthRate(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     growth_form_id = models.ForeignKey(GrowthRates, on_delete=models.CASCADE)

class Lifespan(models.Model):
    lifespan = models.CharField(max_length=40)

    def __str__(self):
        return self.lifespan
# class SpeciesLifespan(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     lifespan_id = models.ForeignKey(Lifespans, on_delete=models.CASCADE)

class Toxicity(models.Model):
    toxicity = models.CharField(max_length=40)

    def __str__(self):
        return self.toxicity
# class SpeciesToxicity(models.Model):
#     species_id = models.ForeignKey(Species, on_delete=models.CASCADE)
#     toxicity_id = models.ForeignKey(Toxicities, on_delete=models.CASCADE)


#main species model

class Species(models.Model):
    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    usda_symbol = models.CharField(max_length=20)
    created_date = models.DateTimeField(
            default=timezone.now)

    #features
    county = models.ManyToManyField(County)
    flower_color = models.ManyToManyField(Color)
    shape = models.ManyToManyField(Shape)
    category = models.ManyToManyField(Category)
    duration = models.ManyToManyField(Duration)
    active_growth_period = models.ManyToManyField(ActiveGrowthPeriod)
    growth_habit = models.ManyToManyField(GrowthHabit)
    growth_form = models.ManyToManyField(GrowthForm)
    growth_rate = models.ManyToManyField(GrowthRate)
    lifespan = models.ManyToManyField(Lifespan)
    toxicity = models.ManyToManyField(Toxicity)


    base_age_height = models.FloatField(null=True)
    mature_height = models.FloatField(null=True)

    #booleans
    fire_resistant = models.NullBooleanField()
    flower_conspicuous = models.NullBooleanField()
    allelopathic = models.NullBooleanField()
    leaf_retentive = models.NullBooleanField()
    resproutable = models.NullBooleanField()

    def as_dict(self):
        return {
            "id":self.id,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
        }

    def as_extended_dict(self):

        return {
            "id":self.id,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
            "location":{
                "counties":list(self.county.all().values_list('county', flat=True))
            },
            "flower_color": self.flower_color.all()[0].__str__() if self.flower_color.all() else None,
            "shape": self.shape.all()[0].__str__() if self.shape.all() else None,
            "category":self.category.all()[0].__str__() if self.category.all() else None,
            "duration":self.duration.all()[0].__str__() if self.duration.all() else None,
            "active_growth_periods":list(self.active_growth_period.all().values_list('active_growth_period', flat=True)),
            "growth_habit":self.growth_habit.all()[0].__str__() if self.growth_habit.all() else None,
            "growth_form":self.growth_form.all()[0].__str__() if self.growth_form.all() else None,
            "growth_rate":self.growth_rate.all()[0].__str__() if self.growth_rate.all() else None,
            "lifespan":self.lifespan.all()[0].__str__() if self.lifespan.all() else None,
            "toxicity":self.toxicity.all()[0].__str__() if self.toxicity.all() else None,
            "fire_resistant":self.fire_resistant,
            "flower_conspicuous":self.flower_conspicuous,
            "allelopathic":self.allelopathic,
            "leaf_retentive":self.leaf_retentive,
            "resproutable":self.resproutable,
        }


