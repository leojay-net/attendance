# Generated by Django 3.2.18 on 2023-08-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='id',
            field=models.CharField(default='ce652283473e4c26b0cf907fb2290010', max_length=64, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='8c12003fb5bb4db8939afb8153e406eb', max_length=64, primary_key=True, serialize=False, unique=True),
        ),
    ]
