# Generated by Django 3.2.16 on 2023-07-19 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('danger', models.FloatField()),
                ('sensor', models.CharField(max_length=50)),
                ('sensortype', models.CharField(max_length=25)),
            ],
        ),
    ]