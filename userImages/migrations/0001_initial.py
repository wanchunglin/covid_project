<<<<<<< HEAD
# Generated by Django 3.1.7 on 2021-04-13 07:07
=======
# Generated by Django 3.2 on 2021-05-03 08:04
>>>>>>> 34e8920 (add temperture function)

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('users', '0001_initial'),
=======
        ('users', '0002_user_verified'),
>>>>>>> 34e8920 (add temperture function)
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('info', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('imagefile', models.ImageField(upload_to='images/', verbose_name='')),
<<<<<<< HEAD
=======
                ('faceEmbedding', models.BinaryField()),
>>>>>>> 34e8920 (add temperture function)
            ],
        ),
    ]
