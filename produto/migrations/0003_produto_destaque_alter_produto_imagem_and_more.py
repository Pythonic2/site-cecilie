# Generated by Django 5.1.1 on 2024-10-07 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_produto_tamanho'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='destaque',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(upload_to='produtos'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tamanho',
            field=models.CharField(max_length=3),
        ),
    ]
