# Generated by Django 4.0.6 on 2022-08-30 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farma_site_app', '0005_remove_servico_summary_alter_servico_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='text',
            field=models.TextField(max_length=200),
        ),
    ]
