# Generated by Django 4.2.11 on 2024-04-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("final_app", "0005_alter_rating_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="rating",
            name="review_text",
            field=models.TextField(default=121),
            preserve_default=False,
        ),
    ]