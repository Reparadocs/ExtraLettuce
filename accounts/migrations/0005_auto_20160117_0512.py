# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='bank_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='bank_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
