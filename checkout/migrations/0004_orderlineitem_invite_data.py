# Generated by Django 3.1.5 on 2021-02-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='invite_data',
            field=models.TextField(blank=True, default=''),
        ),
    ]