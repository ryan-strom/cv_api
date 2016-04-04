# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0002_colors_speciescolor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shapes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shape', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpeciesShape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shape_id', models.ForeignKey(to='flowers.Shapes')),
                ('species_id', models.ForeignKey(to='flowers.Species')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='speciescolor',
            old_name='color',
            new_name='color_id',
        ),
        migrations.RenameField(
            model_name='speciescolor',
            old_name='species',
            new_name='species_id',
        ),
    ]
