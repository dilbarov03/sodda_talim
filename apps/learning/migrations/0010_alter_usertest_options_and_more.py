# Generated by Django 4.2.5 on 2023-10-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0009_userlesson_status_alter_usertest_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="usertest",
            options={
                "ordering": ("id",),
                "verbose_name": "User Test",
                "verbose_name_plural": "User Tests",
            },
        ),
        migrations.RemoveField(
            model_name="entrancequestion",
            name="wrong_option",
        ),
        migrations.AddField(
            model_name="entrancequestion",
            name="wrong_option1",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Wrong Option 1"
            ),
        ),
        migrations.AddField(
            model_name="entrancequestion",
            name="wrong_option2",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Wrong Option 2"
            ),
        ),
    ]