from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import inlineformset_factory, modelform_factory

from core.models import Product, ProductImage, ProductAttribute

ProductImageFormSet = inlineformset_factory(Product, ProductImage, fields='__all__', extra=2, widgets={
    'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
})

ProductAttributeFormSet = inlineformset_factory(Product, ProductAttribute, fields='__all__', extra=2, widgets={
    'name': forms.TextInput(attrs={'class': 'form-control'}),
    'value': forms.TextInput(attrs={'class': 'form-control'}),
})

ProductForm = modelform_factory(Product, exclude=('user', 'rating'), widgets={
    'name': forms.TextInput(attrs={'class': 'form-control'}),
    'content': CKEditorUploadingWidget(),
    'description': forms.Textarea(attrs={'class': 'form-control'}),
    'category': forms.Select(attrs={'class': 'form-select'}),
    'tags': forms.CheckboxSelectMultiple(),
    'price': forms.NumberInput(attrs={'class': 'form-control'}),
})
