# Generated by Django 5.1.1 on 2024-11-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_produto_mais_vendido'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='premium',
            field=models.BooleanField(default=False),
        ),
    ]
