from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from models import Species, Color, County, Shape, Category, Duration, ActiveGrowthPeriod, GrowthHabit, GrowthForm, GrowthRate, Lifespan, Toxicity
from django.core import serializers
import csv
import json
import re
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from flower_detection.views import colorShapeFromImg


# Create your views here.

def getAllSpecies(request):
    species = Species.objects.all()
    species_serialized= serializers.serialize('json', species)
    return JsonResponse(species_serialized, safe=False)

def findSpecies(request):
    colorShape = colorShapeFromImg(request)
    flower_color = colorShape['color']
    petal_count = int(colorShape['shape'])
    category = getCategory(petal_count)

    colorObj = Color.objects.get(color=flower_color)
    categoryObj = Category.objects.get(category=category)
    species = Species.objects.filter(flower_color=colorObj, category=categoryObj).values()

    response = [entry for entry in species]

    return JsonResponse(response, safe=False)



@csrf_exempt #disable csrf
def postSpecies(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        common_name = body['common_name']
        newSpecies = Species(common_name=common_name)
        newSpecies.save()

        if body.has_key("flower_color"):
            flower_color = Color.objects.get(color="yellow-green")
            newSpecies.flower_color.add(flower_color)
            newSpecies.save()

        species_serialized = json.dumps(newSpecies.as_dict())
        return HttpResponse(species_serialized)
    return HttpResponse("No body")

def deleteAllSpecies(request):
    Species.objects.all().delete()

def getSpecies(request, id):
    species = Species.objects.get(id=id)
    return JsonResponse(species.as_extended_dict(), safe=False)

@csrf_exempt #disable csrf
def csvToDB(request):

    if request.method == 'POST':
        file = request.FILES['file']
        reader = csv.DictReader(file)
        result = []
        for row in reader:

            newSpecies = Species(
                common_name=row['Common Name'],
                scientific_name=row['Scientific Name'],
                usda_symbol=row['Symbol'],
                base_age_height=strToFloat(row['Height at Base Age, Maximum (feet)']),
                mature_height=strToFloat(row['Height, Mature (feet)']),
                fire_resistant=yesNoToBool(row['Fire Resistance']),
                flower_conspicuous=yesNoToBool(row['Flower Conspicuous']),
                allelopathic=yesNoToBool(row['Known Allelopath']),
                leaf_retentive=yesNoToBool(row['Leaf Retention']),
                resproutable=yesNoToBool(row['Resprout Ability']),
            )
            newSpecies.save()

            if row['County']:
                counties = row['County'].split(", ")
                for county in counties:
                    newCounty = County.objects.get(county=county)
                    newSpecies.county.add(newCounty)

            if row['Flower Color']:
                newFlowerColor = Color.objects.get(color= row['Flower Color'].lower())
                newSpecies.flower_color.add(newFlowerColor)

            if row['Shape and Orientation']:

                newShape = Shape.objects.get(shape=row['Shape and Orientation'].lower())
                newSpecies.shape.add(newShape)

            if row['Category']:
                newCategory = Category.objects.get(category=row['Category'].lower())
                newSpecies.category.add(newCategory)

            if row['Duration']:
                durations = row['Duration'].split(", ")
                for duration in durations:
                    newDuration = Duration.objects.get(duration=duration.lower())
                    newSpecies.duration.add(newDuration)

            if row['Active Growth Period']:
                if(row['Active Growth Period'] == "Year Round"):
                    row['Active Growth Period'] = "Spring, Summer, Fall, Winter"
                replaced = row['Active Growth Period'].replace(" and ", ", ")
                growth_periods = replaced.split(", ")

                for growth_period in growth_periods:
                    newActiveGrowthPeriod = ActiveGrowthPeriod.objects.get(active_growth_period=growth_period.lower())
                    newSpecies.active_growth_period.add(newActiveGrowthPeriod)

            if row['Growth Habit']:
                growth_habits = row['Growth Habit'].split(", ")
                if 'and' in row['Growth Habit']:
                    growth_habits = row['Growth Habit'].split(" and ")

                for growth_habit in growth_habits:
                    newGrowthHabit = GrowthHabit.objects.get(growth_habit=growth_habit.lower())
                    newSpecies.growth_habit.add(newGrowthHabit)

            if row['Growth Form']:
                newGrowthForm = GrowthForm.objects.get(growth_form=row['Growth Form'].lower())
                newSpecies.growth_form.add(newGrowthForm)

            if row['Growth Rate']:
                newGrothRate = GrowthRate.objects.get(growth_rate=row['Growth Rate'].lower())
                newSpecies.growth_rate.add(newGrothRate)

            if row['Lifespan']:
                newLifespan = Lifespan.objects.get(lifespan=row['Lifespan'].lower())
                newSpecies.lifespan.add(newLifespan)

            if row['Toxicity']:
                newToxicity = Toxicity.objects.get(toxicity=row['Toxicity'].lower())
                newSpecies.toxicity.add(newToxicity)

            newSpecies.save()

            result.append(newSpecies)
        return JsonResponse(result, safe=False)

def yesNoToBool(string):
    string = string.lower()
    if(string == 'yes'):
        return True
    if(string == 'no'):
        return False
    return None

def strToFloat(string):
    if not string:
        return None
    return float(string)

def isMonocot(petal_count):
    return petal_count % 3 == 0


def isDicot(petal_count):
    return petal_count % 4 == 0 or petal_count % 5 == 0


def getCategory(petal_count):
    if isMonocot(petal_count):
        return "monocot"
    if isDicot(petal_count):
        return "dicot"
    return None
