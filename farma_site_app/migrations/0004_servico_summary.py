# Generated by Django 4.0.6 on 2022-08-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farma_site_app', '0003_rename_entrada_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='summary',
            field=models.TextField(default='texto', max_length=200),
            preserve_default=False,
        ),
    ]