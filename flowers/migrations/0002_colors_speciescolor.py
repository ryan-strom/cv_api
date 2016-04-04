# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpeciesColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.ForeignKey(to='flowers.Colors')),
                ('species', models.ForeignKey(to='flowers.Species')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
