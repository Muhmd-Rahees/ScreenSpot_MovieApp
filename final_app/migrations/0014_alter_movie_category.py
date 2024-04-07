# Generated by Django 4.2.11 on 2024-04-06 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("final_app", "0013_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="final_app.category"
            ),
        ),
    ]
