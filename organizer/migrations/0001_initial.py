# Generated by Django 3.1.2 on 2021-05-27 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ename', models.CharField(max_length=20)),
                ('edesc', models.CharField(max_length=100)),
                ('eguest', models.CharField(max_length=100)),
                ('eloc', models.CharField(max_length=15)),
                ('ecat', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'organizer',
            },
        ),
    ]
