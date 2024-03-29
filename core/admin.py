from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from core.models import Tag, Category, ProductImage, ProductAttribute, Product
from ckeditor_uploader.widgets import CKEditorUploadingWidget


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class ProductImageStackedInline(admin.TabularInline):

    model = ProductImage
    extra = 1


class ProductAttributeStackedInline(admin.TabularInline):

    model = ProductAttribute
    extra = 1


class ProductAdminForm(forms.ModelForm):

    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_filter = ('category', 'tags', 'user', 'is_published',)
    search_fields = ('name', 'description', 'content',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    inlines = [ProductAttributeStackedInline, ProductImageStackedInline]
    form = ProductAdminForm

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="150px">')
        return '-'

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'


# Register your models here.
