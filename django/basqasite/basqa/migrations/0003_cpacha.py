# Generated by Django 5.0.2 on 2024-02-20 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basqa', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpacha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('content', models.CharField(verbose_name='Контент')),
            ],
        ),
    ]