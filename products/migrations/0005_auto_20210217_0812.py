# Generated by Django 3.1.5 on 2021-02-17 08:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210209_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='customization',
        ),
        migrations.AddField(
            model_name='product',
            name='customizable',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CustomDetailLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
                ('text', models.CharField(max_length=60)),
                ('y_pos', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2320), django.core.validators.MinValueValidator(25)])),
                ('font', models.CharField(choices=[("'Arial', sans-serif", "'Arial', sans-serif"), ("'Clicker Script', cursive", "'Clicker Script', cursive"), ("'Londrina Solid', cursive", "'Londrina Solid', cursive")], default="'Londrina Solid', cursive", max_length=60)),
                ('size', models.CharField(choices=[('18', '18'), ('24', '24'), ('32', '32'), ('40', '40'), ('48', '48'), ('60', '60'), ('72', '72'), ('96', '96')], default='40', max_length=2)),
                ('color', models.CharField(max_length=7)),
                ('stroke_fill', models.CharField(max_length=7)),
                ('stroke_width', models.CharField(choices=[('0px', 'no stroke'), ('1px', '1px'), ('2px', '2px'), ('4px', '4px')], default='0px', max_length=3)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customlines', to='products.product')),
            ],
        ),
    ]