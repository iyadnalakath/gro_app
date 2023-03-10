# Generated by Django 4.1.6 on 2023-03-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=60, unique=True, verbose_name="email"),
                ),
                ("username", models.CharField(max_length=60, unique=True)),
                ("is_active", models.BooleanField(blank=True, default=True, null=True)),
                ("is_staff", models.BooleanField(blank=True, default=False, null=True)),
                (
                    "is_superuser",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("phone", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[("customer", "customer"), ("admin", "admin")],
                        default="customer",
                        max_length=30,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
