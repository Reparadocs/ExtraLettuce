# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160117_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='scheduled_days_left',
            field=models.IntegerField(default=1),
        ),
    ]
