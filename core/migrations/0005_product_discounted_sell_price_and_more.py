# Generated by Django 5.1.2 on 2024-10-22 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_attribute_is_filterable_attributevalue_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discounted_sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='discounted_sell_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
