# Generated by Django 3.1.5 on 2021-02-24 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210224_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreviews',
            name='comment',
            field=models.TextField(max_length=250),
        ),
    ]
