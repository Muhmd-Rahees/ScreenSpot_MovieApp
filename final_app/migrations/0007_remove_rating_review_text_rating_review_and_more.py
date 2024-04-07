# Generated by Django 4.2.11 on 2024-04-03 14:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("final_app", "0006_rating_review_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rating",
            name="review_text",
        ),
        migrations.AddField(
            model_name="rating",
            name="review",
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="rating",
            name="subject",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="rating",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.FloatField(),
        ),
    ]
