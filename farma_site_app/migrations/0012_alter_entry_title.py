# Generated by Django 4.0.6 on 2022-09-22 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farma_site_app', '0011_alter_entry_image_alter_servico_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
