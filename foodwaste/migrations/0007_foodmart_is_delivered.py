# Generated by Django 5.0.6 on 2024-07-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodwaste', '0006_remove_foodmart_image_foodmart_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodmart',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]
