# Generated by Django 4.1.6 on 2023-03-16 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0014_alter_orderitem_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]