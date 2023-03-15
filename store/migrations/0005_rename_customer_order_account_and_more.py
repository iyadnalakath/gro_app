# Generated by Django 4.1.6 on 2023-03-15 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_alter_cartitem_product"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="customer",
            new_name="account",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="product",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="quantity",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="cart",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items_order",
                to="store.cart",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[("P", "Pending"), ("C", "Complete"), ("F", "Failed")],
                default="P",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orderitems",
                to="store.order",
            ),
        ),
    ]