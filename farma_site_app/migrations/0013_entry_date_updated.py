# Generated by Django 4.0.6 on 2022-09-22 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farma_site_app', '0012_alter_entry_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
    ]