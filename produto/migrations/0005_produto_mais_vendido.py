# Generated by Django 5.1.1 on 2024-10-08 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_produto_promo'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='mais_vendido',
            field=models.BooleanField(default=False),
        ),
    ]
