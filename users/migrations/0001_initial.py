# Generated by Django 3.1.7 on 2021-03-26 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]