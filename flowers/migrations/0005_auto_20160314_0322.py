# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0004_auto_20160314_0237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counties',
            old_name='county',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='states',
            old_name='state',
            new_name='name',
        ),
        migrations.AddField(
            model_name='states',
            name='abbreviation',
            field=models.CharField(default=' ', max_length=2),
            preserve_default=False,
        ),
    ]
