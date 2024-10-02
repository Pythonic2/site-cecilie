# Generated by Django 5.1.1 on 2024-10-02 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(default='descreva a peça', max_length=255)),
                ('disponivel', models.BooleanField(default=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('imagem', models.ImageField(blank=True, default=None, null=True, upload_to='produtos')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.categoria')),
            ],
        ),
    ]
