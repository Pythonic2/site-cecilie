# Generated by Django 5.1.1 on 2024-10-07 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_produto_destaque_alter_produto_imagem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='promo',
            field=models.BooleanField(default=False),
        ),
    ]
