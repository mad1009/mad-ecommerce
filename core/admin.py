from django.contrib import admin
from .models import (
    ProductType, Product, Attribute, AttributeValue,
    ProductVariant, Category, ProductImage
)
from django.utils.html import format_html


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ('name', 'is_filterable')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}  # Automatically generate slug
    search_fields = ('name',)
    list_filter = ('parent',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    readonly_fields = ('sku', 'attributes')
    fields = ('sku', 'stock', 'buy_price', 'sell_price', 'is_active')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image_preview', 'image', 'alt_text')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />'.format(obj.thumbnail.url))
        return "No Image"

    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVariantInline]
    list_display = ('thumbnail_preview', 'name', 'product_type', 'price', 'featured', 'created_at')
    list_filter = ('product_type', 'category', 'featured', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}  # Automatically generate slug

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />'.format(obj.thumbnail.url))
        else:
            return format_html('<img src="/static/global/imgs/default-product.png" style="width: 100px; height: auto;" />')
    thumbnail_preview.short_description = 'Thumbnail'


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'stock', 'buy_price', 'sell_price', 'is_active')
    search_fields = ('sku', 'product__name')
    list_filter = ('is_active', 'product__product_type')
