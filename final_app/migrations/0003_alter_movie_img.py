# Generated by Django 4.2.8 on 2024-04-01 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("final_app", "0002_alter_movie_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="img",
            field=models.ImageField(blank=True, null=True, upload_to="gallery"),
        ),
    ]
