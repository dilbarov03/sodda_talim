# Generated by Django 5.0 on 2023-12-16 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0012_language_alter_lesson_order_lesson_language_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="entrancequestion",
            name="language",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="learning.language",
                verbose_name="Language",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="entrancequestion",
            unique_together={("language", "order")},
        ),
    ]
