# Generated by Django 2.2.28 on 2023-07-31 16:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('generatorApp', '0004_auto_20230731_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]