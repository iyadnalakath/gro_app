# Generated by Django 4.1.6 on 2023-03-03 06:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_cart_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="user",
            new_name="account",
        ),
    ]