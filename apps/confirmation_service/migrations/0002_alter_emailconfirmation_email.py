# Generated by Django 4.0.6 on 2022-10-11 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmation',
            name='email',
            field=models.EmailField(max_length=1024),
        ),
    ]