# Generated by Django 2.2 on 2021-03-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='multiple',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]