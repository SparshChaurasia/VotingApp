# Generated by Django 4.1.7 on 2023-03-18 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vote", "0003_category_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="Voted",
            field=models.TextField(default="{}"),
        ),
    ]
