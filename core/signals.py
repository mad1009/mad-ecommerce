from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Product, ProductVariant


@receiver(post_save, sender=Product)
def create_product_variants(sender, instance, created, **kwargs):
    if created:
        # Optionally create variants here if needed on initial product creation
        pass


@receiver(m2m_changed, sender=Product.attributes.through)
def create_product_variants_on_attribute_change(sender, instance, action, **kwargs):
    if action == 'post_add':
        # Create product variants when attributes are added to the product
        attributes = instance.attributes.all()
        if attributes.exists():
            from itertools import product

            attribute_values = [attr.values.all() for attr in attributes]
            combinations = product(*attribute_values)

            # Clear existing variants before creating new ones
            instance.variants.all().delete()  # Optional: Clear existing variants

            for combination in combinations:
                # Generate a SKU for the variant
                sku = f"{instance.slug}-{'-'.join([str(attr.value) for attr in combination])}"

                # Create the product variant
                p = ProductVariant.objects.create(
                    product=instance,
                    sku=sku,
                    stock=0,  # or any default value
                    buy_price=0.00,  # or any default value
                    sell_price=instance.price,  # or any default value
                )

                p.attributes.set(combination)
