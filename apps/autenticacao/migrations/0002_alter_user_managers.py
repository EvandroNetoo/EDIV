# Generated by Django 4.2.1 on 2023-05-16 18:34

import autenticacao.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', autenticacao.models.UserManager()),
            ],
        ),
    ]