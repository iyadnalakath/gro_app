# Generated by Django 4.1.6 on 2023-03-15 06:41

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_rename_customer_order_account_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0"), max_digits=6
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveSmallIntegerField(
                default=1, validators=[django.core.validators.MinValueValidator(1)]
            ),
            preserve_default=False,
        ),
    ]
