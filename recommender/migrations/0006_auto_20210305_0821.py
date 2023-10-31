# Generated by Django 3.0.7 on 2021-03-05 08:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_auto_20210305_0816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyrecommendedevents',
            old_name='event',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='historyrecommendedevents',
            name='latest_update',
            field=models.DateField(default=datetime.datetime(2021, 3, 5, 8, 21, 16, 156289, tzinfo=utc)),
        ),
    ]
