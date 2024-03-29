# Generated by Django 5.0.3 on 2024-03-26 07:38

import django.core.validators
import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('description', models.CharField(help_text='Просто описание', max_length=255, verbose_name='описание')),
                ('content', models.TextField(verbose_name='контент')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='цена')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='рейтинг')),
                ('is_published', models.BooleanField(default=True, verbose_name='публичность')),
                ('category', models.ForeignKey(help_text='Выберите категорию', on_delete=django.db.models.deletion.PROTECT, to='core.category', verbose_name='категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
                ('tags', models.ManyToManyField(to='core.tag', verbose_name='теги')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('value', models.CharField(max_length=50, verbose_name='значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='core.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'атрибут товара',
                'verbose_name_plural': 'атрибуты товаров',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=90, scale=None, size=[1920, 1080], upload_to='product_images/', verbose_name='изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'изображение товара',
                'verbose_name_plural': 'изображении товаров',
                'ordering': ('-created_at',),
            },
        ),
    ]