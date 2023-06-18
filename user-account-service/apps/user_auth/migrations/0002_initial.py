# Generated by Django 4.2.1 on 2023-06-17 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user_auth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="refreshtoken",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="refresh_token",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]