# Generated by Django 4.2.8 on 2024-04-13 18:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="stream_key",
        ),
    ]
